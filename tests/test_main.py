from src.main import greet, get_work_week_calendar, get_work_week_number, get_current_work_week
from datetime import date, timedelta
from unittest.mock import patch

def test_print_daily_work_weeks():
    """
    Print work week numbers for every day of the year 2025.
    Run this test with pytest -s to see the output.
    """
    # Start from January 1st, 2025
    current_date = date(2025, 1, 1)
    year_end = date(2025, 12, 31)
    
    # Get the first Monday of the year for direct calculation
    year_start = date(2025, 1, 1)
    first_monday = year_start - timedelta(days=year_start.weekday())
    
    # Print header
    print("\nWork Week Calendar for Every Day of 2025:")
    print("Date       | Day of Week | Work Week | Notes")
    print("-" * 60)
    
    # Test every day of the year
    while current_date <= year_end:
        # Get work week number
        week_num = get_work_week_number(current_date, first_monday)
        day_name = current_date.strftime("%A")
        
        # Add notes for special cases
        notes = []
        if current_date.weekday() == 0:  # Monday
            notes.append("Week Start")
        if current_date.weekday() == 4:  # Friday
            notes.append("Week End")
        if current_date.day == 1:
            notes.append("Month Start")
        if (current_date + timedelta(days=1)).month != current_date.month:
            notes.append("Month End")
        
        # Print the day's information
        print(f"{current_date} | {day_name:<10} | WW{week_num:<2}     | {', '.join(notes)}")
        
        # Add separator between months
        if (current_date + timedelta(days=1)).month != current_date.month:
            print("-" * 60)
        
        # Move to next day
        current_date += timedelta(days=1)

def test_greet():
    """Test the greet function."""
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"

def test_work_week_number():
    """Test the work week number calculation."""
    # First Monday of 2025 is December 30, 2024
    first_monday = date(2024, 12, 30)
    
    # Test first week
    assert get_work_week_number(date(2025, 1, 1), first_monday) == 1
    assert get_work_week_number(date(2025, 1, 3), first_monday) == 1
    
    # Test second week
    assert get_work_week_number(date(2025, 1, 6), first_monday) == 2
    assert get_work_week_number(date(2025, 1, 10), first_monday) == 2
    
    # Test week wrapping
    # Create a date that would be week 53 and verify it wraps to week 1
    far_future_date = first_monday + timedelta(weeks=52)
    assert get_work_week_number(far_future_date, first_monday) == 1
    
    # Test a date that would be week 54 wraps to week 2
    far_future_date = first_monday + timedelta(weeks=53)
    assert get_work_week_number(far_future_date, first_monday) == 2

def print_work_week_for_entire_year():
    """
    Print work week numbers for every day of the year 2025.
    This function prints a table showing the date and its work week number.
    """
    def get_week_number_for_date(test_date: date) -> int:
        """Get work week number for a specific date."""
        year_start = date(test_date.year, 1, 1)
        first_monday = year_start - timedelta(days=year_start.weekday())
        return get_work_week_number(test_date, first_monday)
    
    # Start from January 1st, 2025
    current_date = date(2025, 1, 1)
    year_end = date(2025, 12, 31)
    
    # Print header
    print("\nWork Week Calendar for Every Day of 2025:")
    print("Date       | Day of Week | Work Week")
    print("-" * 40)
    
    # Test every day of the year
    while current_date <= year_end:
        week_num = get_week_number_for_date(current_date)
        day_name = current_date.strftime("%A")
        print(f"{current_date} | {day_name:<10} | WW{week_num}")
        
        # Add blank line at the end of each month
        if (current_date + timedelta(days=1)).month != current_date.month:
            print("-" * 40)
        
        # Move to next day
        current_date += timedelta(days=1)

def test_work_week_consistency_for_entire_year():
    """
    Test that get_current_work_week and get_work_week_number give consistent
    results for every day of the year 2025.
    """
    def extract_week_number(result_str: str) -> int:
        """Extract work week number from the result string."""
        import re
        match = re.search(r"Work Week (\d+)", result_str)
        return int(match.group(1))
    
    # Print the calendar for visual inspection
    print_work_week_for_entire_year()
    
    # Start from January 1st, 2025
    current_date = date(2025, 1, 1)
    year_end = date(2025, 12, 31)
    
    # Get the first Monday of the year for direct calculation
    year_start = date(2025, 1, 1)
    first_monday = year_start - timedelta(days=year_start.weekday())
    
    # Test every day of the year
    while current_date <= year_end:
        # Get work week number using get_current_work_week
        with patch('src.main.date') as mock_date:
            mock_date.today.return_value = current_date
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            current_week_str = get_current_work_week()
            week_from_current = extract_week_number(current_week_str)
        
        # Get work week number directly using get_work_week_number
        week_from_direct = get_work_week_number(current_date, first_monday)
        
        # Assert both methods give the same result
        assert week_from_current == week_from_direct, \
            f"Mismatch for {current_date}: get_current_work_week={week_from_current}, " \
            f"get_work_week_number={week_from_direct}"
        
        # Verify week number is within valid range (1-52)
        assert 1 <= week_from_current <= 52, \
            f"Invalid week number {week_from_current} for date {current_date}"
        
        # Move to next day
        current_date += timedelta(days=1)

def test_current_work_week():
    """Test the current work week function with various dates."""
    test_cases = [
        # (test_date, expected_week)
        (date(2025, 3, 14), 11),  # Regular week in March
        (date(2025, 1, 1), 1),    # First day of year
        (date(2025, 1, 6), 2),    # Start of second week
        (date(2025, 12, 31), 1),  # Last day of year (week 53 wraps to 1)
    ]
    
    for test_date, expected_week in test_cases:
        with patch('src.main.date') as mock_date_class:
            mock_date_class.today.return_value = test_date
            mock_date_class.side_effect = lambda *args, **kw: date(*args, **kw)
            
            result = get_current_work_week()
            assert f"Work Week {expected_week}" in result
            assert test_date.strftime('%Y-%m-%d') in result
            assert str(test_date.year) in result

def test_work_week_calendar():
    """Test the work week calendar function."""
    calendar_2025 = get_work_week_calendar(2025)
    
    # Test that the calendar contains all months
    assert "January 2025" in calendar_2025
    assert "December 2025" in calendar_2025
    
    # Test that it only includes weekdays
    assert "Sat" not in calendar_2025
    assert "Sun" not in calendar_2025
    assert "Mon Tue Wed Thu Fri" in calendar_2025
    
    # Test work week numbering
    assert "WW1" in calendar_2025
    assert "WW   Mon Tue Wed Thu Fri" in calendar_2025
    
    # Make sure WW1 doesn't appear twice in January
    january = calendar_2025.split("January 2025")[1].split("\n\n")[0]
    ww1_count = january.count("WW1")
    assert ww1_count == 1, f"WW1 appears {ww1_count} times in January"
    
    # Test that no week number exceeds 52
    for ww in range(53, 100):
        assert f"WW{ww}" not in calendar_2025, f"Found week number {ww} which exceeds 52"
    
    # Test that it generates non-empty output
    assert len(calendar_2025) > 100  # Calendar should be substantial in length 