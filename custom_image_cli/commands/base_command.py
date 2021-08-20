from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    The BaseCommand interface declares a method for running a subcommand.
    """

    @abstractmethod
    def initiate(self, args, log):
        pass

    @abstractmethod
    def run(self):
        pass
