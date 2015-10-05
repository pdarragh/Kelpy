from ..exceptions import *

def are_valid_arguments(arguments):
    for argument in arguments:
        if not isinstance(argument, int) and not isinstance(argument, float):
            return False
    return True

def add(arguments):
    if not are_valid_arguments(arguments) or len(arguments) <= 0:
        raise InvalidArgumentsException('+', arguments)
    elif len(arguments) == 1:
        return arguments[0]
    else:
        result = arguments[0]
        for argument in arguments[1:]:
            result += argument
        return result

def subtract(arguments):
    if not are_valid_arguments(arguments) or len(arguments) <= 0:
        raise InvalidArgumentsException('-', arguments)
    elif len(arguments) == 1:
        return arguments[0]
    else:
        result = arguments[0]
        for argument in arguments[1:]:
            result -= argument
        return result

def multiply(arguments):
    if not are_valid_arguments(arguments) or len(arguments) <= 0:
        raise InvalidArgumentsException('*', arguments)
    elif len(arguments) == 1:
        return arguments[0]
    else:
        result = arguments[0]
        for argument in arguments[1:]:
            result *= argument
        return result

def divide(arguments):
    if not are_valid_arguments(arguments) or len(arguments) <= 0:
        raise InvalidArgumentsException('/', arguments)
    elif len(arguments) == 1:
        return arguments[0]
    else:
        result = arguments[0]
        for argument in arguments[1:]:
            result /= argument
        return result
