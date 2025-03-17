import calendar
from datetime import datetime, timedelta, date

def get_work_week_number(current_date: date, start_date: date) -> int:
    """
    Calculate the work week number starting from a specific date.
    Work weeks wrap back to 1 after week 52.
    
    Args:
        current_date (date): The date to calculate the work week for
        start_date (date): The date to start counting from (WW1)
        
    Returns:
        int: The work week number (1-52)
    """
    # Get to the Monday of the week containing the start_date
    start_weekday = start_date.weekday()
    adjusted_start = start_date - timedelta(days=start_weekday)
    
    # Get to the Monday of the week containing the current_date
    current_weekday = current_date.weekday()
    adjusted_current = current_date - timedelta(days=current_weekday)
    
    # Calculate weeks difference
    weeks_diff = (adjusted_current - adjusted_start).days // 7
    week_num = weeks_diff + 1
    
    # Wrap week number back to 1 if it exceeds 52
    return ((week_num - 1) % 52) + 1 