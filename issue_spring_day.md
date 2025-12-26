---
name: Feature request
about: Suggest an idea for this project
title: 'Feature Request: Add Vernal Equinox Day (Spring Day) to Japanese Holidays'
labels: enhancement
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
The current implementation of `hcal` lacks "Vernal Equinox Day" (Shunbun no Hi), often referred to as Spring Day. This is a national holiday in Japan, and its absence means the calendar displays incorrect holiday information for March.

**Describe the solution you'd like**
I would like to add the logic to calculate Vernal Equinox Day dynamically.
The date can be calculated using the astronomical approximation formula with year-dependent constants:

**Formula:**
`day = int(Constant + 0.242194 * (year - 1980)) - int((year - 1980) / 4)`

**Constants:**
*   **1980–2099:** `20.8431`
*   **1955–1979:** `20.8357`

This logic should be implemented in a new helper function (e.g., `_get_vernal_equinox_day`) within `hcal_holidays.py` and added to the `_get_japan_variable_holidays` set.

**Describe alternatives you've considered**
Using a fixed hardcoded list for every year, but that is inefficient and hard to maintain compared to the formula.

**Additional context**
This holiday typically falls on March 20th or 21st.
