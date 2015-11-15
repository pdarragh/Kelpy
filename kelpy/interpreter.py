from exceptions import *
from types import *
from functions import handle_function

def interpret(kexp, env):
    """
    Takes an inputted KExpression and evaluates its contents.
    """
    # We should only interpret KExpressions, of course.
    if not isinstance(kexp, KExpression):
        raise InterpretException("Not a parsed expression: {}".format(kexp))
    # Handling for function calls. They all take arguments in the same way, so
    # it's easiest to handle them all with one method call.
    functions = [
        KAdd, KMultiply, KSubtract, KDivide, KModulo,
        KEquality, KInequality, KLessThan, KGreaterThan, KLessThanEqual, KGreaterThanEqual,
    ]
    if type(kexp) in functions:
        return interpret_function(kexp, env)
    # Some primitives don't need to be evaluated. Just return those.
    # In general, the exception is symbols (which should be looked up).
    skip_primitives = [
        KNumber, KBoolean, KList
    ]
    if type(kexp) in skip_primitives:
        return kexp
    # Handling expressions for everything else.
    return {
        KSymbol     : interpret_symbol,
        KIf         : interpret_if,
        KLet        : interpret_let,
    }.get(type(kexp), interpret_default)(kexp,env)

def interpret_symbol(ksymbol, env):
    return lookup(ksymbol, env)

def interpret_function(kfunction, env):
    return handle_function(kfunction.symbol, [interpret(arg, env) for arg in kfunction.args])

def interpret_if(kif, env):
    if KBoolean(interpret(kif.test, env)):
        return interpret(kif.true, env)
    else:
        return interpret(kif.false, env)

def interpret_let(klet, env):
    return interpret(
        klet.body,
        (env + KBinding(klet.name, klet.value))
    )

def interpret_default(kexp, env):
    raise InterpretException("No interpreter for KExpression: {}".format(kexp))
