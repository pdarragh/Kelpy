from exceptions import *
from types import *
from functions import handle_function

def interpret(kexp, env):
    """
    Takes an inputted KExpression and evaluates its contents.
    """
    if not isinstance(kexp, KExpression):
        raise InterpretException("Not a parsed expression: {}".format(kexp))
    if isinstance(kexp, KSymbol):
        return lookup(kexp, env)
    elif isinstance(kexp, KFunctionExpression):
        return handle_function(interpret_arguments(kexp, env))
    elif isinstance(kexp, KIf):
        if KBoolean(interpret(kexp.test, env)):
            return interpret(kexp.true, env)
        return interpret(kexp.false, env)
    elif isinstance(kexp, KLet):
        return interpret(
            kexp.body,
            (env + KBinding(kexp.name, kexp.value))
        )
    elif isinstance(kexp, KPrimitive):
        return kexp
    else:
        raise RuntimeError() # pragma: no cover

def interpret_arguments(kfunction, env):
    arguments = kfunction.args
    interpreted = []
    for argument in arguments:
        interpreted.append(interpret(argument, env))
    kfunction.args = tuple(interpreted)
    return kfunction
