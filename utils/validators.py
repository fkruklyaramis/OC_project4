from datetime import datetime, date
import re


def validate_date_format(date_str: str) -> bool:
    """
    Validate if a string is in YYYY-MM-DD format.
    Args:
        date_str (str): Date string to validate
    Returns:
        bool: True if date format is valid, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_chess_id(chess_id: str) -> bool:
    """
    Validate chess ID format (two letters followed by five digits).
    Args:
        chess_id (str): Chess ID to validate
    Returns:
        bool: True if chess ID format is valid, False otherwise
    """
    pattern = r'^[A-Za-z]{2}\d{5}$'
    return bool(re.match(pattern, chess_id))


def validate_player_age(birth_date_str: str) -> bool:
    """
    Validates if a player is at least 18 years old based on their birth date.
    Args:
        birth_date_str (str): Birth date in 'YYYY-MM-DD' format
    Returns:
        bool: True if player is 18 or older, False if under 18 or if date format is invalid
    Example:
        >>> validate_player_age('1990-01-01')
        True
        >>> validate_player_age('2010-01-01')  # Under 18
        False
        >>> validate_player_age('invalid-date')
        False
    """

    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age >= 18
    except ValueError:
        return False


def validate_tournament_start_date(start_date: str) -> bool:
    """
    Validate if tournament start date is valid and not in the past.
    Args:
        start_date (str): Start date in YYYY-MM-DD format
    Returns:
        bool: True if start date is valid and not in the past
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        today = date.today()
        return start >= today
    except ValueError:
        return False


def validate_tournament_dates_order(start_date: str, end_date: str) -> bool:
    """
    Validate if end date is after or equal to start date.
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format

    Returns:
        bool: True if end date is after or equal to start date
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        return end >= start
    except ValueError:
        return False
