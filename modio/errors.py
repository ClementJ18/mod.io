"""Errors generate by mod.io and the library."""


class modioException(Exception):
    """Base exception for the lib"""

    def __init__(self, msg, code=None):
        self.code = code
        super().__init__(msg)
