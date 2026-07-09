# Aging Curves in Professional Soccer — Paper Outline

Working title: *"Past Their Prime? Performance Aging Curves and Market Value
Efficiency in Professional Soccer"*

## 1. Introduction
- Motivation: teams spend enormous sums on transfers; age is a key factor.
- The question: when do players peak, and does the market price aging correctly?
- Contribution: position-specific aging curves + a market-efficiency comparison.

## 2. Related work / background
- Aging curves in other sports (baseball WAR curves, the "peak at 27" idea).
- Prior soccer analytics on player valuation.
- Gap this fills.

## 3. Data
- Source: FBref (performance, age, position), Transfermarkt (market value).
- Leagues / seasons covered.
- Sample-size filters (minimum minutes).
- Descriptive statistics table.

## 4. Methods
- Per-90 performance metrics by position.
- Curve fitting: quadratic vs. LOESS; how we locate the peak.
- Handling survivorship bias (only good players stay in the league at older ages).

## 5. Results
- Peak age by position (with the curves as figures).
- Steepness of decline.
- Market value vs. performance overlay — where the market over/underpays.

## 6. Discussion
- Practical implications for recruitment.
- Limitations (survivorship bias, one metric ≠ full value, league scope).

## 7. Conclusion & future work

## Figures to produce (see `figures/`)
- F1: Performance vs. age curve per position.
- F2: Peak-age comparison across positions.
- F3: Market value vs. age, overlaid on performance.
