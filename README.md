# Soccer Aging Curves ⚽📈

**When do soccer players peak — and do clubs overpay for players past their prime?**

A data-science research project studying how player performance changes with age
across positions, and whether the transfer market prices that aging correctly.

## Research questions

1. **Peak age by position:** At what age do goalkeepers, defenders, midfielders, and
   forwards reach their performance peak?
2. **Shape of the curve:** How steep is the rise before the peak and the decline after it?
3. **Market efficiency:** Do market values / transfer fees track the performance curve, or
   do clubs systematically overpay for post-peak players?

## Method (high level)

1. Collect player-season performance, ages, and market values from the Transfermarkt
   *Player Scores* dataset (all joined by `player_id`).
2. Build per-90 performance metrics, grouped by position and age.
3. Fit aging curves (quadratic + LOESS smoothing) to performance vs. age.
4. Overlay market value on the performance curve to find over/under-valued age bands.

All analysis is done in **Jupyter notebooks** (pandas + Matplotlib), run
top-to-bottom. See `protocol.md` for how we work and `PLAN.md` for the milestones.

## Project structure

```
soccer-aging-curves/
├── CLAUDE.md         # project charter (role, mission, stack, conventions)
├── PLAN.md           # milestones, dependencies, complexity, risks
├── protocol.md       # working protocol (update README after each commit, etc.)
├── data/
│   ├── raw/          # untouched downloaded data (git-ignored)
│   └── processed/    # cleaned, analysis-ready data (git-ignored)
├── notebooks/        # THE workspace — all analysis, modeling, and figures
├── src/              # small helpers the notebooks import (config, data download)
├── figures/          # exported charts for the paper
└── paper/            # research write-up (outline + drafts)
```

## Getting started

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Data sources

**Primary:** David Cariboo's [*Player Scores* dataset](https://www.kaggle.com/datasets/davidcariboo/player-scores)
(Transfermarkt) on Kaggle. Age, market value, and basic performance are already
joined by `player_id`, which removes the live-scraping and name-matching risks
of a from-scratch FBref pipeline. Downloaded via [`kagglehub`](https://pypi.org/project/kagglehub/).

**Optional enrichment (later):** advanced metrics (xG, progressive actions) from
FBref / Understat via [`soccerdata`](https://soccerdata.readthedocs.io).

All sources are free. Raw data is git-ignored; `src/data_collection.py` reproduces it.

> **Kaggle auth:** you need a free Kaggle API token. Create one at
> <https://www.kaggle.com/settings> → *Create New Token*, then save `kaggle.json`
> to `%USERPROFILE%\.kaggle\kaggle.json` (or set `KAGGLE_USERNAME` / `KAGGLE_KEY`).

## Status

🚧 Early scaffolding. See `paper/outline.md` for the planned write-up.
