from .Column import ColumnNameType


class KeyNotFound(Exception):
    def __init__(self, message: str, key: str):
        super().__init__(message)
        self.key = key


class KeyOutOfBound(Exception):
    def __init__(self, message: str, key: int):
        super().__init__(message)
        self.key = key
