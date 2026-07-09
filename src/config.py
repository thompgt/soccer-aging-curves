"""Project-wide configuration: paths and analysis settings."""

from pathlib import Path

# --- Paths -----------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
FIGURES = PROJECT_ROOT / "figures"

for _p in (DATA_RAW, DATA_PROCESSED, FIGURES):
    _p.mkdir(parents=True, exist_ok=True)

# --- Analysis settings -----------------------------------------------------
# Which leagues and seasons to pull. Start small; expand once the pipeline works.
LEAGUES = ["ENG-Premier League"]
SEASONS = ["2223", "2324"]

# Minimum minutes played for a player-season to count (filters out noise from
# players with tiny samples).
MIN_MINUTES = 450

# Age bins / range to study.
AGE_MIN = 16
AGE_MAX = 40

# Broad position groups we collapse detailed positions into.
POSITION_GROUPS = {
    "GK": "Goalkeeper",
    "DF": "Defender",
    "MF": "Midfielder",
    "FW": "Forward",
}
