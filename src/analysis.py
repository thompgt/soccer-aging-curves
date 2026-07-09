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
    """Aggregate per-game appearances into player-season rows.

    TODO (together):
      - join appearances -> games to get `season` and filter to COMPETITIONS/SEASONS
      - sum goals/assists/minutes per (player_id, season); filter MIN_MINUTES
      - join players for date_of_birth + position; compute age in that season
      - map position -> POSITION_GROUPS; compute per-90 metrics
    """
    raise NotImplementedError("We'll build this step together.")


def attach_market_value(player_seasons: pd.DataFrame,
                        valuations: pd.DataFrame) -> pd.DataFrame:
    """Attach the season's market value to each player-season.

    TODO (together): pick the valuation nearest each season for every player.
    """
    raise NotImplementedError("We'll build this step together.")


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
