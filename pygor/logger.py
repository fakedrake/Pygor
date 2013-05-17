import logging
from types import FunctionType

from pygor.settings import LOGGER_ID


def log_call(func):
    def wrapped(obj, *args, **kwargs):
        obj.logger.debug("Calling: %s" % func.__name__)
        return func(obj, *args, **kwargs)

    return wrapped

class MetaLogger(type):
    def __new__(meta, classname, bases, classDict):
        newClassDict = {}

        for attributeName, attribute in classDict.items():
            if type(attribute) == FunctionType:
                attribute = log_call(attribute)

            newClassDict[attributeName] = attribute

        log = logging.LoggerAdapter(logging.getLogger(LOGGER_ID), dict(class_name=classname))
        newClassDict['logger'] = log

        return type.__new__(meta, classname, bases, newClassDict)

class Logger(object):
    """Whoever subclasses Logger has the benefit of a local logger that
    outputs with class_name in the message context. Also if you
    setLevel of the master logger (defined by LOGGER_ID) to
    logging.DEBUG you even get logs on function calls.

    """
    __metaclass__ = MetaLogger
