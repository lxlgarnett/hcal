# hcal

A simple command-line calendar utility written in Python that highlights the current date.

## Features

- Displays a formatted calendar for any month/year.
- **Highlights the current date** with a white background for quick focus.
- **Colors weekends:** Saturdays in blue and Sundays in red.
- **Supports Holidays:** Highlights holidays in red (currently supports Japan).
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

### Configuration

You can configure `hcal` by creating a `~/.hcalrc` file.

**Supported options:**
- `country`: Set to `Japan` to enable Japanese holiday highlighting.

**Example `~/.hcalrc`:**
```ini
country=Japan
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
