"""Build aging curves from the staged Transfermarkt data.

Scaffold only — the real fitting logic gets filled in once we have data. The
function signatures below sketch the intended pipeline so the structure is
clear from day one.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config


def load_raw() -> dict[str, pd.DataFrame]:
    """Load the core CSV tables staged by data_collection.

    Returns a dict keyed by the names in ``config.TABLES`` (players,
    appearances, valuations, games, competitions).
    """
    tables: dict[str, pd.DataFrame] = {}
    for key, filename in config.TABLES.items():
        path = config.DATA_RAW / filename
        if not path.exists():
            raise FileNotFoundError(
                f"{path} not found. Run `python -m src.data_collection` first."
            )
        tables[key] = pd.read_csv(path)
    return tables


def build_player_seasons(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Aggregate per-game appearances into an analysis-ready player-season table.

    Mirrors the scoping funnel validated in ``notebooks/01_exploration.ipynb``
    section 6-8:
      1. join appearances -> games to attach `season`; restrict to
         `config.COMPETITIONS` / `config.SEASONS`.
      2. sum goals/assists/minutes (+ appearance count) per (player_id, season).
      3. filter to `config.MIN_MINUTES`.
      4. join `players` for date_of_birth/position (+ a few extra attributes
         useful for later clustering: height, foot, international caps).
      5. compute age-in-season (reference date = Jan 1 of the season's second
         calendar year, e.g. season 2022 -> 2022/23 -> ref date 2023-01-01 --
         same approximation used in 01_exploration so results are consistent);
         filter to `config.AGE_MIN`/`config.AGE_MAX`.
      6. map raw `position` -> `config.POSITION_GROUPS`; drop the ~1% of
         players with an unmapped/"Missing" position (documented in PLAN.md M2).
      7. compute per-90 metrics (goals_per_90, assists_per_90), guarding
         against division by zero even though MIN_MINUTES already rules out
         minutes_played == 0 in practice.

    Returns one row per (player_id, season) that passes every filter above.
    """
    appearances = tables["appearances"]
    games = tables["games"]
    players = tables["players"]

    # --- Clean the appearances table -----------------------------------
    # Defensive de-dup: 01_exploration found none, but don't rely on silence.
    apps = appearances.drop_duplicates(subset="appearance_id").copy()
    apps = apps.drop_duplicates(subset=["player_id", "game_id"])
    for col in ("goals", "assists", "minutes_played"):
        apps[col] = apps[col].fillna(0)
    apps = apps[apps["minutes_played"] >= 0]

    # --- Step 1: attach season, restrict to target leagues/seasons ------
    games_slim = games[["game_id", "season"]]
    merged = apps.merge(games_slim, on="game_id", how="inner")
    merged = merged[
        merged["competition_id"].isin(config.COMPETITIONS)
        & merged["season"].isin(config.SEASONS)
    ]

    # --- Step 2: aggregate to player-season -----------------------------
    player_season = (
        merged.groupby(["player_id", "season"])
        .agg(
            minutes_played=("minutes_played", "sum"),
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            n_appearances=("appearance_id", "count"),
        )
        .reset_index()
    )

    # --- Step 3: MIN_MINUTES filter --------------------------------------
    player_season = player_season[player_season["minutes_played"] >= config.MIN_MINUTES].copy()

    # --- Step 4: join players for bio/position (+ extra attributes) -----
    players_slim = players[
        [
            "player_id",
            "date_of_birth",
            "position",
            "height_in_cm",
            "foot",
            "country_of_citizenship",
            "international_caps",
            "international_goals",
        ]
    ].copy()
    players_slim["date_of_birth"] = pd.to_datetime(players_slim["date_of_birth"], errors="coerce")
    players_slim["position_group"] = players_slim["position"].map(config.POSITION_GROUPS)

    ps = player_season.merge(players_slim, on="player_id", how="left")

    # Drop rows with no usable date_of_birth -- can't compute age.
    ps = ps[ps["date_of_birth"].notna()].copy()

    # --- Step 5: age-in-season, then AGE_MIN..AGE_MAX filter ------------
    season_ref_date = pd.to_datetime(ps["season"].astype(str) + "-01-01") + pd.DateOffset(years=1)
    ps["age"] = (season_ref_date - ps["date_of_birth"]).dt.days / 365.25
    ps = ps[ps["age"].between(config.AGE_MIN, config.AGE_MAX)]

    # --- Step 6: drop unmapped/"Missing" position (~1%, per PLAN.md M2) --
    ps = ps[ps["position_group"].notna()].copy()

    # --- Step 7: per-90 metrics, guarding divide-by-zero -----------------
    ps["goals_per_90"] = np.where(
        ps["minutes_played"] > 0, ps["goals"] / ps["minutes_played"] * 90, np.nan
    )
    ps["assists_per_90"] = np.where(
        ps["minutes_played"] > 0, ps["assists"] / ps["minutes_played"] * 90, np.nan
    )

    return ps.reset_index(drop=True)


def attach_market_value(player_seasons: pd.DataFrame,
                        valuations: pd.DataFrame) -> pd.DataFrame:
    """Attach each player-season's nearest market valuation.

    Uses the same season reference date as `build_player_seasons` (Jan 1 of
    the season's second calendar year) and picks, per player, the valuation
    whose date is closest to that reference date (`pd.merge_asof`, nearest
    direction). Player-seasons for players with no valuation history at all
    get a NaN market value rather than being silently dropped.
    """
    df = player_seasons.copy()
    df["season_ref_date"] = pd.to_datetime(df["season"].astype(str) + "-01-01") + pd.DateOffset(years=1)

    val = valuations.copy()
    val["date"] = pd.to_datetime(val["date"], errors="coerce")
    val = val.dropna(subset=["date", "market_value_in_eur", "player_id"])
    val = val[val["market_value_in_eur"] > 0]
    val = val[["player_id", "date", "market_value_in_eur"]].sort_values("date")

    df_sorted = df.sort_values("season_ref_date")
    merged = pd.merge_asof(
        df_sorted,
        val,
        left_on="season_ref_date",
        right_on="date",
        by="player_id",
        direction="nearest",
    )
    merged = merged.rename(columns={"market_value_in_eur": "market_value_eur", "date": "valuation_date"})

    return merged.sort_index().reset_index(drop=True)


def fit_aging_curve(df: pd.DataFrame, metric: str, position: str) -> np.ndarray:
    """Fit performance-vs-age for one position and return the smoothed curve.

    TODO (together): quadratic fit first (peak = -b/2a), then LOESS. Add the
    delta-method robustness check for survivorship bias.
    """
    raise NotImplementedError("We'll build this step together.")


if __name__ == "__main__":
    data = load_raw()
    for name, frame in data.items():
        print(f"{name:14s} {frame.shape[0]:>8,} rows  cols={list(frame.columns)[:6]}...")
