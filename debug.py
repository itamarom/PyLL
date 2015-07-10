from functools import wraps

IS_DEBUG = False
LOG_FILE = None


def log(func):
    """
    A decorator that allows functions to be called with
    verbose=True for logging.

    By default, logging will be made to stdout.
    If a filename is specified with logfile, the
    output of the function will be written to there instead
    """
    @wraps(func)
    def inner(*args, **kwargs):
        if kwargs.pop('verbose', False) or IS_DEBUG:
            params = []
            if args: params.append(args)
            if kwargs: params.append(kwargs)
            line = "%s(%s) = " % (func.__name__, ", ".join(map(str, params)))
            
            if LOG_FILE: LOG_FILE.write(line)
            else: print line,
            
            value = func(*args, **kwargs)
            
            if LOG_FILE: LOG_FILE.write(str(value) + "\r\n")
            else: print value
            
            return value
        else:
            return func(*args, **kwargs)
    return inner
