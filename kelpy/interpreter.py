from exceptions import *
from types import *
from functions import handle_function

def interpret(kexp):
    """
    Takes an inputted KExpression and evaluates its contents.
    """
    if not isinstance(kexp, KExpression):
        raise InterpretException("Not a parsed expression: {}".format(kexp))
    if isinstance(kexp, KSymbol):
        print("need lookup")
        return kexp
    elif isinstance(kexp, KFunctionExpression):
        return handle_function(interpret_arguments(kexp))
    elif isinstance(kexp, KIf):
        if KBoolean(interpret(kexp.test)):
            return interpret(kexp.true)
        return interpret(kexp.false)
    elif isinstance(kexp, KPrimitive):
        return kexp
    else:
        raise RuntimeError()

def interpret_arguments(kfunction):
    arguments = kfunction.args
    interpreted = []
    for argument in arguments:
        interpreted.append(interpret(argument))
    kfunction.args = tuple(interpreted)
    return kfunction
