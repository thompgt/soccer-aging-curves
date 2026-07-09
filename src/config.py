"""Project-wide configuration: paths, data source, and analysis settings."""

from pathlib import Path

# --- Paths -----------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
FIGURES = PROJECT_ROOT / "figures"

for _p in (DATA_RAW, DATA_PROCESSED, FIGURES):
    _p.mkdir(parents=True, exist_ok=True)

# --- Data source -----------------------------------------------------------
# Primary backbone: David Cariboo "Player Scores" (Transfermarkt) on Kaggle.
# Age + market value + basic performance are already joined by player_id, which
# removes the live-scraping and name-matching risks of the FBref approach.
KAGGLE_DATASET = "davidcariboo/player-scores"

# The CSV tables we rely on (the dataset ships more; these are the core ones).
TABLES = {
    "players": "players.csv",              # player_id, date_of_birth, position, sub_position, ...
    "appearances": "appearances.csv",      # per-game goals, assists, minutes_played, cards
    "valuations": "player_valuations.csv", # market_value_in_eur over time (date)
    "games": "games.csv",                  # game_id -> season, date, competition
    "competitions": "competitions.csv",    # competition_id -> name, country
}

# --- Analysis settings -----------------------------------------------------
# Restrict to top competitions to start (expand once the pipeline works).
# These are Transfermarkt domestic competition IDs for the "big five" leagues.
COMPETITIONS = ["GB1", "ES1", "L1", "IT1", "FR1"]  # EPL, La Liga, Bundesliga, Serie A, Ligue 1

# Seasons to include (Transfermarkt season start year, e.g. 2022 = 2022/23).
SEASONS = [2020, 2021, 2022, 2023]

# Minimum minutes played in a season for a player-season to count.
MIN_MINUTES = 900

# Age range to study.
AGE_MIN = 16
AGE_MAX = 40

# Broad position groups we collapse Transfermarkt's `position` field into.
POSITION_GROUPS = {
    "Goalkeeper": "Goalkeeper",
    "Defender": "Defender",
    "Midfield": "Midfielder",
    "Attack": "Forward",
}
