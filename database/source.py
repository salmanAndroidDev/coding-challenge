import json
from abc import ABC, abstractmethod
from .decorators import required_connection
from .exceptions import *


class DBInterface(ABC):
    """
        Database Interface that all concrete DBs should extend from
        * CRUD methods could be added here
    """

    @abstractmethod
    def get(self, field, value):
        """Abstract method to apply filtering and return first matched item"""
        pass

    @abstractmethod
    def filter(self, field, value):
        """Abstract method to apply filtering and return list of filtered data"""
        pass

    @abstractmethod
    def fields(self):
        """Abstract method to return entity fields"""


class BaseDB(DBInterface):
    """
        Base class that all types of databases should extend from
    """

    @abstractmethod
    def add_data(self, data):
        """Abstract method to store source of data"""
        pass

    def process_data(self, data):
        """Optional method to any processing"""
        raise NotImplementedError()


class JSONDB(BaseDB):
    """
        This class allows navigation through JSON database
    """

    def __init__(self) -> None:
        self.__data = []
        self.__fields = set()

    def add_data(self, data):
        """ Store data in memory.
            data: (list or str) data must be list or json path string that contains
                   list of dictionaries ( or JSON objects)
        """
        if not isinstance(data, list):
            data = self.convert_file_path_to_json(data)

        self.process_data(data)
        self.__data = data

    def process_data(self, data):
        """ Validate received data and store fields in memory"""
        assert isinstance(data, list), "data must be list type"
        for item in data:
            if not isinstance(item, dict):
                raise DataIsInvalidError()
            self.__fields.update(item.keys())

    def filter(self, field, value):
        """ Apply filtering
            field: (str) field to apply filter based on it
            value: (str, int, bool) value to apply filter based on it
            :return: result of filter
        """
        assert type(value) in {int, str, bool}, "value must string, integer or boolean type"

        if field not in self.__fields:
            raise FieldNotFoundError()

        result = []
        for item in self.__data:
            if self.exists(item, field, value):
                result.append(item)

        return result

    @staticmethod
    def exists(source, key, value):
        """ Condition to check whether value exist in the source
            source: (dict) source of data
            key: (str, int, bool)
            value: (str, int, bool)
            :Return: (bool)
        """
        found_value = source.get(key)
        if found_value is None:
            return False

        # if value in dictionary is str or bool or int compare it with value
        if (type(found_value) in {str, int, bool}) and (found_value == value):
            return True

        # if value in dictionary is list type check if value exist in it
        if isinstance(found_value, list) and (value in found_value):
            return True

        return False

    def fields(self):
        """Return fields (or columns)"""
        return self.__fields

    def get(self, field, value):
        """ Get first matched value
            field: (str) field to apply filter based on it
            value: (str, int, bool) value to apply filter based on it
            :return: dictionary
        """
        assert type(value) in {int, str, bool}, "value must string, integer or boolean type"

        if field not in self.__fields:
            raise FieldNotFoundError()

        for item in self.__data:
            if self.exists(item, field, value):
                return item
        return None

    @staticmethod
    def convert_file_path_to_json(file_path):
        """Converts json_file path to python list"""
        try:
            with open(file_path) as json_file:
                return json.load(json_file)
        except Exception as e:
            raise DataIsNotJSONError()


class Database:
    """
        Main Database class that other application can instantiate and connect to
        any type of database (as default it's connected to JSON type DB)
    """

    def __init__(self):
        self.db = None

    def connect(self, source, db=None):
        """ Connect to data and initialize db
            source: (list of dictionaries, or string path to source)
            db: Concrete class that is extended from BaseDB.
            :return: instance
        """
        if db is None:
            db = JSONDB()

        self.db = db
        self.db.add_data(source)
        return self

    def is_db_connected(self):
        """Check whether db is connected to appropriate source"""
        return not (self.db is None)

    @required_connection
    def filter(self, field, value):
        """ return filtered list based on matched result """
        print('.........', field, value, type(field), type(value))
        return self.db.filter(field, value)

    @required_connection
    def fields(self):
        """ return fields list"""
        return self.db.fields()

    @required_connection
    def get(self, field, value):
        """ Return matched item"""
        return self.db.get(field, value)
