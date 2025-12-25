# hcal

A simple command-line calendar utility written in Python that highlights the current date.

## Features

- Displays a formatted calendar for any month/year.
- **Highlights the current date** with a white background for quick focus.
- **Colors weekends:** Saturdays in blue and Sundays in red.
- **Supports Holidays:** Highlights holidays in red (currently supports Japan).
- **Three-Month View:** Option to display previous, current, and next months.
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
- `-h`: Disable highlighting of today's date.
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
