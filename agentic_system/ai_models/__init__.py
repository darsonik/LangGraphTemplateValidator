import logging

"""
ai_models package initialization.

This file can be used to import key classes/functions for easier access,
set up package-level variables, or configure logging.
"""


logging.getLogger(__name__).addHandler(logging.NullHandler())

# Example: Import commonly used classes/functions here
# from .model import AIModel
# from .utils import load_model

__all__ = [
    # "AIModel",
    # "load_model",
]