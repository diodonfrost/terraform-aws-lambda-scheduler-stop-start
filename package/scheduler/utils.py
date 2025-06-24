"""Utility functions for scheduler operations."""

import logging
from datetime import datetime


def is_date_excluded(excluded_dates: list[str]) -> bool:
    """Check if the current date should be excluded from scheduling.

    Args:
        excluded_dates: List of dates in MM-DD format to exclude

    Returns:
        True if current date should be excluded, False otherwise
    """
    if not excluded_dates:
        return False

    current_date = datetime.now()
    current_date_str = current_date.strftime("%m-%d")

    if current_date_str in excluded_dates:
        logging.info(
            "Skipping execution - current date (%s) is in excluded dates: %s",
            current_date_str,
            excluded_dates,
        )
        return True

    return False


def strtobool(value: str) -> bool:
    """Convert string to boolean."""
    return value.lower() in ("yes", "true", "t", "1")
