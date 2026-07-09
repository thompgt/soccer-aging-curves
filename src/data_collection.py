"""Download the raw dataset from Kaggle and stage it in data/raw/.

Primary source: David Cariboo "Player Scores" (Transfermarkt).
https://www.kaggle.com/datasets/davidcariboo/player-scores

Run once after setting up the environment:

    python -m src.data_collection

Auth: kagglehub needs a free Kaggle API token. Create one at
https://www.kaggle.com/settings -> "Create New Token" (downloads kaggle.json),
then place it at %USERPROFILE%\\.kaggle\\kaggle.json  (Windows), or set the
KAGGLE_USERNAME / KAGGLE_KEY environment variables.
"""

from __future__ import annotations

import shutil

from . import config


def download_dataset() -> str:
    """Download the Kaggle dataset and return the local cache path."""
    import kagglehub

    print(f"Downloading '{config.KAGGLE_DATASET}' via kagglehub...")
    path = kagglehub.dataset_download(config.KAGGLE_DATASET)
    print(f"  cached at: {path}")
    return path


def stage_tables(source_dir: str) -> None:
    """Copy the core CSV tables we use into data/raw/ for a stable local copy."""
    from pathlib import Path

    src = Path(source_dir)
    for key, filename in config.TABLES.items():
        found = next(src.rglob(filename), None)
        if found is None:
            print(f"  ! WARNING: {filename} not found in download ({key})")
            continue
        dest = config.DATA_RAW / filename
        shutil.copyfile(found, dest)
        print(f"  staged {filename} -> {dest}")


def main() -> None:
    cache = download_dataset()
    print("Staging core tables into data/raw/ ...")
    stage_tables(cache)
    print("Done. Next: build the cleaning step in src/analysis.py.")


if __name__ == "__main__":
    main()
