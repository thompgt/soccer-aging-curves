# Working Protocol

Lightweight rules for how we work on this project. These are process rules
(the *how*), separate from `CLAUDE.md` (the *what* and *why*) and `PLAN.md`
(the milestones).

---

## 1. Update the README after every commit

`README.md` is the front page of the repo and must always reflect the **current**
state of the project. After every commit, review the README and update it so it
matches what now exists.

**When committing, follow this sequence:**

1. Make the change (notebook, `src/` helper, doc, figure).
2. Update `README.md` to reflect the new reality. Check, at minimum:
   - **Status** section — what milestone (per `PLAN.md`) is now done / in progress.
   - **Project structure** — any new notebook or file.
   - **Research questions / method** — if scope or approach changed.
   - **Getting started** — if setup steps changed.
3. Stage the work **and** the README update together.
4. Commit (see message convention below).
5. Push.

Rule of thumb: **no commit lands without the README reflecting it.** If a change
doesn't affect anything the README describes, note that you checked — but usually
at least the Status line moves.

## 2. Keep PLAN.md honest

When a milestone starts or finishes, update its status in `PLAN.md` so the plan
tracks reality. The README carries the short public status; `PLAN.md` carries the
detailed one.

## 3. Notebook reproducibility before committing — HARD GATE

**No notebook is committed unless it has just been executed top-to-bottom, from a
clean kernel, with zero errors.** This is not a manual "looks fine" check — it
must be verified mechanically every time, no exceptions:

```bash
.venv/Scripts/python.exe -m jupyter nbconvert --to notebook --execute --inplace \
  notebooks/<name>.ipynb
```

- This clears all prior state and re-runs every cell in order, so there is no
  hidden state, no out-of-order execution, and no stale output.
- If the command exits non-zero (a cell raised), **the commit does not happen.**
  Fix the notebook and re-run the command until it succeeds.
- The committed `.ipynb` outputs are always the outputs of that exact run — never
  hand-edited or copied from an earlier execution.
- Applies to every commit that touches a notebook, not just "final" ones.

## 4. Commit message convention

- Short imperative summary line (≤ ~72 chars).
- Optional body: bullet points on *what changed and why*.
- Reference the milestone when relevant, e.g. `M2: aggregate appearances into player-seasons`.

## 5. Data is never committed

`data/raw/` and `data/processed/` are git-ignored. Reproducibility comes from the
code + the recorded Kaggle dataset version, not from committing data.

---

### Quick checklist (copy per commit)

- [ ] Change made
- [ ] If a notebook changed: `jupyter nbconvert --execute --inplace` run, **exit code 0**
- [ ] `README.md` updated to match
- [ ] `PLAN.md` status updated (if a milestone moved)
- [ ] Staged, committed, pushed
