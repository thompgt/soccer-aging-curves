# Implementation Plan — Soccer Aging Curves

Derived from the repo scope (`README.md`, `src/`, `paper/outline.md`) and the
project charter in `CLAUDE.md`. Calibrated to a beginner→intermediate developer,
1–3 month timeline, targeting a formal paper + portfolio piece.

**Primary data source:** David Cariboo *Player Scores* (Transfermarkt) on Kaggle —
chosen because age + market value + basic performance are pre-joined by
`player_id`, eliminating live-scraping and name-matching risk.

**Tech stack:** intentionally minimal — **pandas + Jupyter Notebook + Matplotlib**
(plus numpy/scipy/statsmodels for curve fitting). All work happens in numbered
notebooks run top-to-bottom; no separate production pipeline, dashboard, or
heavyweight tooling. This keeps effort on the research, not the toolchain.

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
**Status:** `notebooks/01_exploration.ipynb` (extensive raw-data EDA) is done and
already answers several M2 inputs — see its §8 summary:
- Final analysis-ready sample after all filters: **6,480 player-seasons, 2,970
  unique players** (big-five leagues, 2020-2023, `MIN_MINUTES >= 900`, valid
  position + age 16-40).
- Only ~1% of players (505/48,381) have an unmapped `"Missing"` position — safe to drop.
- **Thin-tail risk confirmed:** goalkeepers are sparse below age ~24; all positions
  are sparse past age 35 — M4's curve fitting needs to handle this explicitly
  (wider uncertainty bands / coarser bins at the extremes, not silent extrapolation).
- No duplicate rows found in `players`, `appearances`, or `(player_id, game_id)` pairs.

## M3 — Exploratory data analysis ⭐⭐
**Goal:** understand distributions before modeling.
- Age histograms, minutes distribution, sample counts per (age, position).
- Sanity checks (implausible ages, duplicates).
**Dependencies:** M2. **Artifact:** committed EDA figures + notes.
**Status:** raw-data EDA done early, ahead of schedule, in `notebooks/01_exploration.ipynb`
(see M2 status note below) — most of this milestone's checks already ran against the
raw tables. M3 proper should re-run the same checks against the *processed* M2 table
to confirm nothing broke in the join/aggregation step.
**Risks:** thin samples at age extremes → informs filtering + limitations.

## M4 — Aging-curve modeling ⭐⭐⭐⭐
**Goal:** the scientific core — fit curves and locate peaks.
- Quadratic fit (interpretable peak = -b/2a), then LOESS smoothing
  (`statsmodels` lowess) as a non-parametric check.
- Peak age + uncertainty per position; decline slope.
- **Survivorship bias:** add a delta-method robustness check (year-over-year
  change for players present in consecutive seasons).
**Dependencies:** M2 (M3 recommended).
**Risks:** survivorship bias (the #1 methodological critique); overfitting →
prefer quadratic/LOESS over high-degree polynomials.

## M5 — Market-value efficiency ⭐⭐ (was ⭐⭐⭐; risk reduced by data choice)
**Goal:** the novel insight — does the market price aging correctly?
- Attach each player-season's market value from `player_valuations`.
- Overlay value-vs-age on performance-vs-age; find over/under-paid age bands.
- Performance-per-euro ranking.
**Dependencies:** M4.
**Note:** name-matching risk is *gone* — value shares `player_id` with performance.
**Risks:** market value is partly reputation/potential, not pure output — discuss.

## M6 — Figures & results ⭐⭐
**Goal:** publication-quality visuals (Matplotlib).
- F1 per-position curves; F2 peak-age comparison; F3 value overlay.
- Export from notebooks to `figures/`.
**Dependencies:** M4 (M5 for F3). **Risks:** low; timebox aesthetics.

## M7 — Paper write-up ⭐⭐⭐
**Goal:** the application deliverable.
- Expand `paper/outline.md` to full prose; tie figures to claims; honest
  limitations (survivorship bias, metric choice, league/season scope).
**Dependencies:** M6. **Risks:** overclaiming beyond the evidence.

---

## Cross-cutting concerns (from `CLAUDE.md`)
- **Reproducibility:** record the Kaggle dataset version; each notebook must
  re-run top-to-bottom from a clean kernel and reproduce its outputs.
- **Narrative:** every notebook explains its steps in markdown cells — the
  notebooks double as the lab record for the paper.
- **README upkeep:** update `README.md` after every commit (see `protocol.md`).

## Top risks to watch
1. **Metric validity (M2)** — the performance proxy is the foundation.
2. **Survivorship bias (M4)** — the intellectual crux and novel contribution.
3. **Notebook reproducibility (cross-cutting)** — notebook-only work makes it easy
   to leave hidden state or out-of-order cells. Mitigate by always doing a
   "Restart & Run All" before committing, so results are deterministic.
