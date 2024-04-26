#
# @author: Mario Torre
# @date: 09/30/2021
#
import logging
import param
import sys

class Logs(param.Parameterized):
    value = param.String(precedence=1, label='')
    def flush(self):
        pass
    def write (self, message):
        self.value = message + self.value

def get_logger(name, stream, format):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(format)
    handler = logging.StreamHandler(stream=stream)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    sout = logging.StreamHandler(sys.stdout)
    sout.setFormatter(formatter)
    logger.addHandler(sout)
    return logger

def get_logger_with_file(name, file, format):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(format)
    sfile = logging.FileHandler(file)
    sfile.setFormatter(formatter)
    logger.addHandler(sfile)
    return logger
