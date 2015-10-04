from ..exceptions import *

def add(*args):
    print("add")
    if len(args) <= 0:
        raise InvalidArgumentsException('+', args)
    elif len(args) == 1:
        return args[0]
    else:
        result = args[0]
        for arg in args[1:]:
            result += arg
        return result
def subtract(*args):
    print("subtract")
def multiply(*args):
    print("multiply")
def divide(*args):
    print("divide")
