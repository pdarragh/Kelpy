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
    result = handle_function(function, arguments)
    return result

def interpret_arguments(arguments):
    result = []
    for argument in arguments:
        result.append(interpret_expression(argument))
    return result

def interpret_expression(expression):
    if isinstance(expression, PExpression):
        return interpret(expression)
    elif isinstance(expression, PNumber):
        return expression.value
    elif isinstance(expression, PFunction):
        raise BadFunctionException(expression)
    elif isinstance(expression, PSymbol):
        return expression
