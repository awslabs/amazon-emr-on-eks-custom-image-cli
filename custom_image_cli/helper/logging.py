import logging
import colorlog


class Log:
    def __init__(self):
        self.log = logging.getLogger("logger")
        stream = logging.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(levelname)s]%(reset)s "
            "%(message)s",
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            })
        stream.setFormatter(formatter)
        self.log.addHandler(stream)
        self.log.setLevel(logging.INFO)

    def info(self, s):
        self.log.info(s)

    def error(self, s):
        self.log.error(s)

    def warn(self, s):
        self.log.warning(s)
