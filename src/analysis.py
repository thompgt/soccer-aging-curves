"""Build aging curves from collected player-season data.

Scaffold only — the real fitting logic gets filled in once we have data. The
function signatures below sketch the intended pipeline so the structure is
clear from day one.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config


def load_raw() -> pd.DataFrame:
    """Load the raw FBref stats saved by data_collection."""
    path = config.DATA_RAW / "fbref_standard.parquet"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python -m src.data_collection` first."
        )
    return pd.read_parquet(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Filter to usable player-seasons and add derived columns.

    TODO (together): filter by MIN_MINUTES, map detailed positions to
    POSITION_GROUPS, compute per-90 metrics, and coerce age to an integer.
    """
    raise NotImplementedError("We'll build this step together.")


def fit_aging_curve(df: pd.DataFrame, metric: str, position: str) -> np.ndarray:
    """Fit performance-vs-age for one position and return the smoothed curve.

    TODO (together): try a quadratic fit first (simple, interpretable peak),
    then LOESS for a non-parametric view.
    """
    raise NotImplementedError("We'll build this step together.")


if __name__ == "__main__":
    data = load_raw()
    print(f"Loaded {len(data)} rows. Columns:\n{list(data.columns)[:20]}")
