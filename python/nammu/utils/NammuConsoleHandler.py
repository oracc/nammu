import logging
from logging import StreamHandler


class NammuConsoleHandler(StreamHandler):
    """
    Extends StreamHandler to make it print log messages in Nammu's console for
    the user to see.
    """
    def __init__(self, nammu_console):
        """
        Needs a reference to nammu to be able to get ahold of Nammu's console.
        """
        super(logging.StreamHandler, self).__init__()
        self.nammu_console = nammu_console

    def emit(self, record):
        """
        This is the method that prints out the log message. Format the given
        record and send to Nammu's console for the user to see.
        """
        msg = self.format(record)
        self.nammu_console.addText(msg + "\n")
