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
    arguments = pexpression.arguments
    handle_function(function, arguments)
