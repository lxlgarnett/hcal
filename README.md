# hcal

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Flxlgarnett%2Fhcal%2Fmain%2Fpyproject.toml&query=%24.project%5B%27requires-python%27%5D&label=python&color=blue)](pyproject.toml)
[![Pylint](https://github.com/lxlgarnett/hcal/actions/workflows/pylint.yml/badge.svg)](https://github.com/lxlgarnett/hcal/actions/workflows/pylint.yml)
[![GitHub issues](https://img.shields.io/github/issues/lxlgarnett/hcal)](https://github.com/lxlgarnett/hcal/issues)
[![GitHub stars](https://img.shields.io/github/stars/lxlgarnett/hcal)](https://github.com/lxlgarnett/hcal/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/lxlgarnett/hcal)](https://github.com/lxlgarnett/hcal/commits/main)
[![GitHub top language](https://img.shields.io/github/languages/top/lxlgarnett/hcal)](https://github.com/lxlgarnett/hcal)

A simple command-line calendar utility written in Python that highlights the current date, weekends, and holidays.

## Features

- Displays a formatted calendar for any month or year.
- **Highlights the current date** with a white background for quick focus.
- **Colors weekends:** Saturdays in blue and Sundays in red.
- **Supports Holidays:** Highlights holidays in red. Currently supports Japan, including complex rules like substitute holidays (Furikae Kyūjitsu) and Citizen's Holidays.
- **Flexible Views:** Support for displaying multiple months or entire years.
- **Julian Days:** Support for displaying the day of the year (Julian day) with the `-j` option.
- Supports standard `cal` style arguments.

## Usage

### Running Locally

Ensure the script is executable:
```bash
chmod +x hcal
```

Run for the current month:
```bash
./hcal
```

Run for a specific month of the current year:
```bash
./hcal 12
```

Run for a specific month and year:
```bash
./hcal 12 2025
```

Run for a whole year:
```bash
./hcal 2026
```

### Command Line Options

- `-3`: Display previous, current, and next month.
- `-A, --after <n>`: Display `<n>` additional months after the specified month.
- `-B, --before <n>`: Display `<n>` additional months before the specified month.
- `-h`: Disable highlighting of today's date.
- `-j`: Display Julian days (day of year).
- `-y [year]`: Display a calendar for the specified year (defaults to current year if no year provided).

### Configuration

You can configure `hcal` by creating a `~/.hcalrc` file.

**Supported options:**
- `country`: Set to `Japan` to enable Japanese holiday highlighting.
- `holiday_color`: Set the color for holidays (default: `red`). Supported colors: `red`, `green`, `blue`, `yellow`, `magenta`, `cyan`, `white`.

**Example `~/.hcalrc`:**
```ini
country=Japan
holiday_color=blue
```

## Docker

You can also run `hcal` using Docker.

### Build the Image
```bash
docker build -t hcal .
```

### Run the Container
```bash
# Current month
docker run --rm hcal

# Specific date
docker run --rm hcal 1 2026

# Sync with local timezone
docker run --rm -v /etc/localtime:/etc/localtime:ro hcal
```
