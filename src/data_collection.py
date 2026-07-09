"""Collect raw player-season data from FBref (and later Transfermarkt).

This is a starting scaffold. Run it once the environment is set up:

    python -m src.data_collection

It pulls standard player stats for the leagues/seasons in ``config`` and saves
them to ``data/raw/``. We keep collection separate from analysis so we only hit
the network when we need to.
"""

from __future__ import annotations

import pandas as pd

from . import config


def collect_fbref_player_stats() -> pd.DataFrame:
    """Download standard player-season stats from FBref via soccerdata.

    Returns a tidy DataFrame and also writes it to ``data/raw/``.
    """
    # Imported here so the module imports cheaply even without soccerdata installed.
    import soccerdata as sd

    fbref = sd.FBref(leagues=config.LEAGUES, seasons=config.SEASONS)

    # "standard" includes minutes, age, position, goals, assists, etc.
    stats = fbref.read_player_season_stats(stat_type="standard")

    out_path = config.DATA_RAW / "fbref_standard.parquet"
    stats.to_parquet(out_path)
    print(f"Saved {len(stats)} player-season rows -> {out_path}")
    return stats


def main() -> None:
    print("Collecting FBref player-season stats...")
    print(f"  Leagues: {config.LEAGUES}")
    print(f"  Seasons: {config.SEASONS}")
    collect_fbref_player_stats()
    print("Done. Next: run the cleaning/analysis step.")


if __name__ == "__main__":
    main()
