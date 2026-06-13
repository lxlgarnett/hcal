# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`hcal` is a `cal`-style command-line calendar that highlights today, weekends, and holidays
using ANSI color codes. Pure Python 3.9+, **standard library only** — no runtime dependencies.

## Commands

Use the project venv for all tooling (pytest/pylint live there, not in system Python):

```bash
# Run the full test suite
.venv/bin/python -m pytest tests/

# Run a single test file or test
.venv/bin/python -m pytest tests/test_hcal_holidays.py
.venv/bin/python -m pytest tests/test_hcal.py::test_hcal_highlighting

# Lint (CI gate is --fail-under=8.0 on all tracked .py files)
.venv/bin/python -m pylint $(git ls-files '*.py') --fail-under=8.0

# Run the tool directly
./hcal              # current month
./hcal 12 2025      # specific month/year
./hcal 2026         # whole year
```

CI (`.github/workflows/pylint.yml`) runs pylint plus `tests/test_hcal_holidays.py` and
`tests/test_hcal.py` on every push.

## Architecture

Three modules, no package — the entry point imports the other two by filename:

- **`hcal`** — executable entry script. Argument parsing (`argparse`, with a manual `-h` that
  means "no highlight", not help — `--help` is the real help flag) and all **multi-month
  layout** logic: rendering months 3-per-row, padding lines to a fixed visual width,
  normalizing block heights, and grouping by year with headers. Layout math accounts for ANSI
  codes by measuring visual length via `strip_ansi`.
- **`hcal_util.py`** — `HighlightCalendar`, a subclass of `calendar.TextCalendar`. Overrides
  `formatday` (applies ANSI color: white-bg for today, holiday color, red Sundays, blue
  Saturdays, and Julian day-of-year rendering) and `formatmonth` (sets `curr_y`/`curr_m` and
  refreshes the holiday set for the year being rendered). Also `read_config` (`~/.hcalrc`,
  `KEY=VALUE` lines) and the shared `strip_ansi` helper.
- **`hcal_holidays.py`** — `get_holidays(country, year)` returns a set of `(month, day)` tuples.
  Only Japan is implemented. Fixed and variable holidays are computed per-year (variable ones
  depend on era-specific rules, e.g. Happy Monday weekday shifts, equinox astronomical
  approximations, one-off 2020/2021 Olympics dates), then two post-processing passes run over
  `datetime.date` objects: Citizens' Holiday (a non-holiday sandwiched between two holidays)
  and Substitute Holiday (Monday after a Sunday holiday).

### Key conventions

- **Holiday correctness is year-range-sensitive.** When touching `hcal_holidays.py`, preserve
  the `if year >= …` / `if 1955 <= year <= …` boundaries — each Japanese holiday changed
  definition over time, and the per-holiday tests assert specific historical years.
- **Layout assumes a per-day column width** of 2 (default) or 3 (Julian, `-j`), with the month
  width derived in `HighlightCalendar.__init__`. Code that builds or pads output lines must
  account for ANSI escapes by comparing `strip_ansi` length, never raw `len`.

### Tests

Most test files subclass `HcalTestCase` (`tests/hcal_test_base.py`), which runs the real `./hcal`
binary as a subprocess and provides ANSI-aware assertion helpers (`assert_visual_length`,
`assert_months_row_alignment`, etc.). Tests are run via pytest but the suite is a mix of
`unittest.TestCase` classes and a few plain `def test_*` functions.
