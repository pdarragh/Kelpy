from exceptions import *
from parser import *
from functions import handle_function

def interpret(pexpression):
    """
    Takes an inputted PExpression and evaluates its contents.
    """
    if not isinstance(pexpression, PExpression):
        raise InterpretException("Not a parsed expression: {}".format(pexpression))
    function  = pexpression.function
    arguments = interpret_arguments(pexpression.arguments)
    return handle_function(function, arguments)

def interpret_arguments(arguments):
    result = []
    for argument in arguments:
        result.append(interpret_expression(argument))
    return result

def interpret_expression(expression):
    pass
