import logging
import functools
from google.api_core.exceptions import BadRequest

logger = logging.getLogger(__name__)


def not_none_or_error(arg_value, arg_name):
    if arg_value is None:
        raise ValueError("{} can't be None".format(arg_name))


class ExtrasRequiredError(ImportError):
    pass


def log_syntax_error(method):

    @functools.wraps(method)
    def decorated(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except BadRequest as e:
            if 'Syntax error' in e.message:
                logger.error(e.message)
            else:
                raise e

    return decorated


def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}