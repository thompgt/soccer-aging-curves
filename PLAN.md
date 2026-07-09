# Implementation Plan — Soccer Aging Curves

Derived from the repo scope (`README.md`, `src/`, `paper/outline.md`) and the
project charter in `CLAUDE.md`. Calibrated to a beginner→intermediate developer,
1–3 month timeline, targeting a formal paper + portfolio piece.

**Primary data source:** David Cariboo *Player Scores* (Transfermarkt) on Kaggle —
chosen because age + market value + basic performance are pre-joined by
`player_id`, eliminating live-scraping and name-matching risk.

Complexity: ⭐ (easy) → ⭐⭐⭐⭐ (hardest for current skill level).

---

## Dependency chain
```
M0 → M1 → M2 → M3 → M4 → M6 → M7
                     ↘ M5 ↗
```
M5 (market-value efficiency) is parallel/optional — the paper is complete without it.

## Timeline (weeks)
| Weeks | Focus |
|------|-------|
| 1 | M0 + M1 |
| 2–3 | M2 + M3 |
| 4–6 | **M4** (scientific core) |
| 7–8 | M5 (if pursued) |
| 9–10 | M6 + M7 |

---

## M0 — Environment & reproducibility ⭐
**Goal:** reproducible dev setup.
- `.venv`, `pip install -r requirements.txt`, verify imports.
- Configure Kaggle API token; test one `kagglehub` download.
**Dependencies:** none. **Artifact:** working env + smoke test.
**Risks:** dependency wheels on Python 3.13/Windows; Kaggle auth setup.

## M1 — Data acquisition ⭐
**Goal:** stage the Transfermarkt tables locally.
- Run `src/data_collection.py`; confirm `players`, `appearances`,
  `player_valuations`, `games`, `competitions` land in `data/raw/`.
**Dependencies:** M0. **Artifact:** staged CSVs + row-count check.
**Risks:** dataset schema/column drift between Kaggle updates → pin/record the
dataset version used.

## M2 — Cleaning & feature engineering ⭐⭐⭐
**Goal:** analysis-ready player-season table.
- Aggregate `appearances` → per-(player, season) goals/assists/minutes.
- Compute **age in season** from `date_of_birth`; filter `MIN_MINUTES`.
- Map `position` → `POSITION_GROUPS`; compute **per-90** metrics.
- Decide the per-position performance metric (a real research decision).
**Dependencies:** M1.
**Risks:** metric validity (a weak proxy undermines the paper); position changes
across seasons; Transfermarkt performance is basic (no xG).

## M3 — Exploratory data analysis ⭐⭐
**Goal:** understand distributions before modeling.
- Age histograms, minutes distribution, sample counts per (age, position).
- Sanity checks (implausible ages, duplicates).
**Dependencies:** M2. **Artifact:** committed EDA figures + notes.
**Risks:** thin samples at age extremes → informs filtering + limitations.

## M4 — Aging-curve modeling ⭐⭐⭐⭐
**Goal:** the scientific core — fit curves and locate peaks.
- Quadratic fit (interpretable peak = -b/2a), then LOESS / spline / GAM.
- Peak age + uncertainty per position; decline slope.
- **Survivorship bias:** add a delta-method robustness check (year-over-year
  change for players present in consecutive seasons).
**Dependencies:** M2 (M3 recommended).
**Risks:** survivorship bias (the #1 methodological critique); overfitting →
prefer quadratic/LOESS/GAM over high-degree polynomials.

## M5 — Market-value efficiency ⭐⭐ (was ⭐⭐⭐; risk reduced by data choice)
**Goal:** the novel insight — does the market price aging correctly?
- Attach each player-season's market value from `player_valuations`.
- Overlay value-vs-age on performance-vs-age; find over/under-paid age bands.
- Performance-per-euro ranking.
**Dependencies:** M4.
**Note:** name-matching risk is *gone* — value shares `player_id` with performance.
**Risks:** market value is partly reputation/potential, not pure output — discuss.

## M6 — Figures & results ⭐⭐
**Goal:** publication-quality visuals (Plotly primary per `CLAUDE.md`).
- F1 per-position curves; F2 peak-age comparison; F3 value overlay.
**Dependencies:** M4 (M5 for F3). **Risks:** low; timebox aesthetics.

## M7 — Paper write-up ⭐⭐⭐
**Goal:** the application deliverable.
- Expand `paper/outline.md` to full prose; tie figures to claims; honest
  limitations (survivorship bias, metric choice, league/season scope).
**Dependencies:** M6. **Risks:** overclaiming beyond the evidence.

---

## Cross-cutting concerns (from `CLAUDE.md`)
- **Testing (pytest):** every transformation in M2/M4/M5 gets a unit test on a
  tiny fixture. Untested transforms are a stated anti-goal.
- **Reproducibility:** record the Kaggle dataset version; deterministic pipeline
  from raw → processed (Parquet) → figures.
- **Code quality:** ruff + black + mypy in CI before the project grows.

## Top risks to watch
1. **Metric validity (M2)** — the performance proxy is the foundation.
2. **Survivorship bias (M4)** — the intellectual crux and novel contribution.
3. **Stack vs. skill (cross-cutting)** — the `CLAUDE.md` stack (Polars, DuckDB,
   Streamlit, GAM/Bayesian) is powerful but adds learning overhead for a 1–3
   month beginner→intermediate timeline. Introduce advanced tools *incrementally*
   so tooling never blocks research progress. **Open decision — see below.**
