""" """

from conda.exceptions import CondaError


class LockfileFormatNotSupported(CondaError):
    def __init__(self, path: str):
        message = f"The specified file {path} is not supported."
        super().__init__(message)
