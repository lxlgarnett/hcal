"""
Tests for the -y option of hcal.
"""
import subprocess
import sys
import datetime

def test_hcal_y_flag_current_year():
    """Test that -y flag without arguments shows the current year."""
    now = datetime.datetime.now()
    year = now.year
    cmd = [sys.executable, "./hcal", "-y"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    output = result.stdout
    # Check that the year is displayed at the top
    # The output format for year view starts with lots of spaces and then the year
    if str(year) in output.split('\n')[0]:
        print(f"PASS: -y flag shows current year {year}")
    else:
        print(f"FAIL: -y flag did not show current year {year}")
        print("Output head:", output.split('\n')[:3])
        sys.exit(1)

def test_hcal_y_flag_specific_year():
    """Test that -y flag with a specific year argument shows that year."""
    year = 2030
    cmd = [sys.executable, "./hcal", "-y", str(year)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    output = result.stdout
    if str(year) in output.split('\n')[0]:
        print(f"PASS: -y {year} shows year {year}")
    else:
        print(f"FAIL: -y {year} did not show year {year}")
        print("Output head:", output.split('\n')[:3])
        sys.exit(1)

if __name__ == "__main__":
    test_hcal_y_flag_current_year()
    test_hcal_y_flag_specific_year()
