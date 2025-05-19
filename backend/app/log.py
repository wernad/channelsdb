"""Logging configuration module for the application.

This module sets up the basic logging configuration with a standard format
and creates a logger instance for use throughout the application.
"""

import logging

__all__ = ["log"]

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)
