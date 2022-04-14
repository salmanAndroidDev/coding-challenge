class Error(Exception):
    """Base class that all error classes should extend from"""
    pass


class DataIsNotJSONError(Error):
    """This exception is thrown when some data is not Json type"""

    def __init__(self, message='Data is not list type or json file path') -> None:
        super().__init__(message)


class DataIsInvalidError(Error):
    """This exception is thrown when the data is not valid"""

    def __init__(self, message='Data has not valid type') -> None:
        super().__init__(message)


class FieldNotFoundError(Error):
    """This exception is thrown when the field doesn't exist"""

    def __init__(self, message='field was not found') -> None:
        super().__init__(message)


class DatabaseIsNotConnectedError(Error):
    """This exception is thrown when the field doesn't exist"""

    def __init__(self, message='database is not connected') -> None:
        super().__init__(message)
