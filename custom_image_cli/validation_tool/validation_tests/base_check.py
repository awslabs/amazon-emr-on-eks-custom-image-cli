from abc import ABC, abstractmethod


class BaseCheck(ABC):
    """
    The BaseCheck interface declares a method for checking the tests.
    """

    @abstractmethod
    def check(self):
        pass
