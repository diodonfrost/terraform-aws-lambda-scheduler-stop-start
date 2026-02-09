"""Decorators module for scheduler handlers."""

import functools
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def skip_on_dry_run(func):
    """Skip the actual operation and log instead when dry-run mode is enabled.

    Reads the DRY_RUN environment variable. When set to "true",
    the decorated method will only log the intended action
    without executing it.

    :param func: The method to wrap
    :return: Wrapped function
    """

    @functools.wraps(func)
    def wrapper(self, resource_id, action):
        if os.environ.get("DRY_RUN", "false").lower() == "true":
            logger.info("[DRY-RUN] Would %s: %s", action, resource_id)
            return
        return func(self, resource_id, action)

    return wrapper
