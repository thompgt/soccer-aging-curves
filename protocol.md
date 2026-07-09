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

## 3. Notebook reproducibility before committing

Because this is a notebook-driven project, before committing any notebook:

- **Restart kernel and Run All** — confirm it runs top-to-bottom with no hidden
  state and no out-of-order cells.
- Make sure outputs shown are the ones the fresh run produced.
- Clear obviously stale/scratch cells.

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
- [ ] Notebook restarted & run all (if a notebook changed)
- [ ] `README.md` updated to match
- [ ] `PLAN.md` status updated (if a milestone moved)
- [ ] Staged, committed, pushed
