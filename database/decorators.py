from functools import wraps
from .exceptions import DatabaseIsNotConnectedError


def required_connection(func):
    """ Decorator function to make sure that db is connected and source is defined"""

    @wraps(func)
    def db_must_be_connected(*args, **kwargs):
        if (len(args) <= 0) or (not args[0].is_db_connected()):
            raise DatabaseIsNotConnectedError()
        return func(*args, **kwargs)

    return db_must_be_connected
