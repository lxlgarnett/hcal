import subprocess
import datetime
import sys

def test_hcal_highlighting():
    # Get today's date
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    
    # Run hcal for current month/year
    cmd = [sys.executable, "./hcal", str(month), str(year)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Expected ANSI code sequence for today
    # Note: TextCalendar pads single digit days with space.
    # formatday width is usually 2 or 3 depending on context, but here standard cal is 2 chars + 1 space.
    # The highlighted string is `\033[47;30m{s}\033[0m`
    
    # We search for the start of the sequence
    ansi_start = "\033[47;30m"
    ansi_end = "\033[0m"
    
    output = result.stdout
    if ansi_start in output and ansi_end in output:
        print("PASS: Highlighting found.")
        # Optional: check if the day inside is correct
        start_idx = output.find(ansi_start) + len(ansi_start)
        end_idx = output.find(ansi_end, start_idx)
        highlighted_content = output[start_idx:end_idx].strip()
        if highlighted_content == str(day):
            print(f"PASS: Correct day {day} highlighted.")
        else:
            print(f"FAIL: Highlighted content '{highlighted_content}' does not match day '{day}'.")
            sys.exit(1)
    else:
        print("FAIL: No highlighting found.")
        print("Output was:")
        print(output)
        sys.exit(1)

def test_hcal_no_highlighting_wrong_month():
    # Check next month (or previous)
    now = datetime.datetime.now()
    if now.month == 12:
        month = 1
        year = now.year + 1
    else:
        month = now.month + 1
        year = now.year
        
    cmd = [sys.executable, "./hcal", str(month), str(year)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    ansi_start = "\033[47;30m"
    if ansi_start in result.stdout:
        print("FAIL: Highlighting found in wrong month.")
        sys.exit(1)
    else:
        print("PASS: No highlighting in wrong month.")

if __name__ == "__main__":
    test_hcal_highlighting()
    test_hcal_no_highlighting_wrong_month()
