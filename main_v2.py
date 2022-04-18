import os, enum
from abc import ABC, abstractmethod
from database.source import Database
from database.exceptions import FieldNotFoundError
from constants import *


class BuxSize(enum.Enum):
    SMALL = 1
    MEDIUM = 2
    BIG = 3


class Graphic:
    """
        This class displays result in a human readable format in CLI
    """

    def __init__(self, small_size=50, medium_size=80, big_size=100, hr_bar='-', vr_bar='|'):
        assert len(hr_bar) == 1, 'hr_bar must be one character'
        assert len(hr_bar) == 1, 'vr_bar must be one character'
        self.__horizontal_bar = hr_bar
        self.__vertical_bar = vr_bar
        self.__sizes = {
            BuxSize.SMALL: small_size,
            BuxSize.MEDIUM: medium_size,
            BuxSize.BIG: big_size
        }

    def show_title(self, title, size):
        lines = [
            " " + "".center(size - 2, self.__horizontal_bar) + " ",
            f"{self.__vertical_bar} " + f"{title.center(size - 4, ' ')}" + f" {self.__vertical_bar}",
            "|" + "".center(size - 2, self.__horizontal_bar) + "|",
        ]

        for line in lines:
            print(line)

    def show_content(self, result, size):
        assert type(result) in {str, dict, list, set}

        lines = []

        if isinstance(result, str):
            lines = [
                f"{self.__vertical_bar} " + f"{result.ljust(size - 4, ' ')}" + f" {self.__vertical_bar}",
            ]

        if isinstance(result, list):
            for i in range(len(result)):
                item = result[i]
                item = item[:size - 15] + '...' if len(item) > (size - 15) else item
                lines.append(
                    f"{self.__vertical_bar} {i + 1}. {item}".ljust(size - 2, ' ') + f" {self.__vertical_bar}")

        if isinstance(result, set):
            i = 1
            for item in result:
                item = item[:size - 15] + '...' if len(item) > (size - 15) else item
                lines.append(
                    f"{self.__vertical_bar} {i + 1}. {item}".ljust(size - 2, ' ') + f" {self.__vertical_bar}")
                i += 1

        if isinstance(result, dict):
            for key in result.keys():
                item = str(result[key])
                item = item[:size - 15] + '...' if len(item) > (size - 15) else item
                lines.append(
                    f"{self.__vertical_bar} {key}: {item}".ljust(size - 2, ' ') + f" {self.__vertical_bar}")

        lines.append(" " + "".center(size - 2, self.__horizontal_bar) + " ")

        for line in lines:
            print(line)

    def display(self, result, title='Result', bux_size=BuxSize.SMALL):
        assert isinstance(title, str), 'title type must be a string object'
        assert isinstance(bux_size, BuxSize), 'bux size type must be a BuxSize object'
        size = self.__sizes[bux_size]

        self.show_title(title, size)
        self.show_content(result, size)


class Runnable(ABC):
    """
        Runnable Interface enables concrete classes to be runnable
    """

    @abstractmethod
    def run(self):
        """Abstract method to run concrete classes objects"""


class Feedback(Runnable):
    """
        Feedback is base class for all action-reaction operations
    """

    @abstractmethod
    def action(self) -> dict:
        """This class enables doing specific actions and returns a dictinoary"""
        pass

    @abstractmethod
    def reaction(self, *args, **kwargs):
        """This class enables doing reaction based on the action"""

    def run(self):
        """Running a complete feedback"""
        kwargs = self.action()
        self.reaction(kwargs)


class MainQuestions(Feedback):
    def action(self) -> dict:
        try:
            option = int(input('What is your option'))
        except Exception as e:
            Graphic().display("Please only select 1 or 2 or 3", title='Error')

        return {'option': option}

    def reaction(self, args, kwargs):
        print(kwargs)


class ProgramState(enum.Enum):
    """
        Enum that defines state of the class
    """
    RUNNING = 1
    STOPPED = 2


class Program(Runnable):
    """
        Main program class that Runs other programs
    """

    def __init__(self):
        self.main_questions = MainQuestions()

    state = ProgramState.STOPPED
    user_db = Database().connect(entities[USER])
    ticked_db = Database().connect(entities[TICKET])
    organization_db = Database().connect(entities[ORGANIZATION])

    def run(self):
        self.main_questions.run()


class MainMenu(Feedback):
    """
        This class enables handling main questions
    """

    def __init__(self):
        self.__options = OptionBux()

    def action(self) -> dict:
        """This method displays option and """


class OptionBux(Runnable):
    def __init__(self, title='Please select an option'):
        self.__options = []
        self.__title = title

    def add_option(self, option: str):
        """Add option to be displayed"""
        assert isinstance(option, str), "Option must be string type"
        self.__options.append(option)

    def run(self):
        """Displaying list of options"""
        Graphic().display(self.__options, title=self.__title)


if __name__ == '__main__':
    graphic = Graphic()

    error = 'Something wrong exists with this command you have to change your mind'
    friends = [
        'Salman', "Amber", 'Zobair', 'Mohammad',
        "You must see something completely different in the command line to ensure that you are not ruining"
    ]

    cazins = {
        "Mohammad", 'Ahmad', 'Ali', 'Hamzeh', 'Khalid', 'Jasom', 'Ghasem', 'Naser', 'Khatam', 'Hazam'
    }

    todos = {
        "Algo": "Leanring about data structure and algorithms",
        "Design Patterns": "Leanring about design patterns",
        "Microservices": "Leanring about Microservices",
        "Turkish Language": "Leanring about Turkish language",
    }

    # graphic.display(result=error, title=error, bux_size=BuxSize.MEDIUM)
    # graphic.display(result=friends, title='Friends', bux_size=BuxSize.MEDIUM)
    # graphic.display(result=cazins, title='Best guys', bux_size=BuxSize.MEDIUM)
    # graphic.display(result=todos, title='Todo List', bux_size=BuxSize.MEDIUM)
    option_bux = OptionBux()
    option_bux.add_option('Search Zendesk')
    option_bux.add_option('View list of searchable fields')
    option_bux.add_option('Quit')

    # option_bux.run()

    program = Program()
    program.run()