from exceptions import *
from parser import *
from functions import handle_function

def interpret(kexp):
    """
    Takes an inputted KExpression and evaluates its contents.
    """
    if not isinstance(kexp, KExpression):
        raise InterpretException("Not a parsed expression: {}".format(kexp))
    if isinstance(kexp, KNumber):
        return kexp.value
    elif isinstance(kexp, KSymbol):
        print("need lookup")
        return 0
    elif isinstance(kexp, KFunctionExpression):
        handle_function(kexp)
    else:
        raise RuntimeError()
    return result

def interpret_arguments(arguments):
    result = []
    for argument in arguments:
        result.append(interpret_expression(argument))
    return result

def interpret_expression(expression):
    if isinstance(expression, kexp):
        return interpret(expression)
    elif isinstance(expression, PNumber):
        return expression.value
    elif isinstance(expression, PFunction):
        raise BadFunctionException(expression)
    elif isinstance(expression, PSymbol):
        return expression
