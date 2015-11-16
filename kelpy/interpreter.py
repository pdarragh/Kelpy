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
        KNumber, KBoolean, KList, KClosure
    ]
    if type(kexp) in skip_primitives:
        return kexp
    # Handling expressions for everything else.
    return {
        KSymbol         : interpret_symbol,
        KIf             : interpret_if,
        KLambda         : interpret_lambda,
        KApplication    : interpret_application,
    }.get(type(kexp), interpret_default)(kexp, env)

def interpret_symbol(ksymbol, env):
    value = lookup(ksymbol, env)
    # Explicit test against 'None' in case strings are implemented in the
    # future.
    return value if value is not None else ksymbol

def interpret_function(kfunction, env):
    # if any([type(arg) == KSymbol for arg in kfunction.args]):
    #     raise UninterpretedSymbolException(kfunction, env)
    return handle_function(kfunction.symbol, [interpret(arg, env) for arg in kfunction.args])

def interpret_if(kif, env):
    if KBoolean(interpret(kif.test, env)):
        return interpret(kif.true, env)
    else:
        return interpret(kif.false, env)

def interpret_lambda(klambda, env):
    return KClosure(klambda.body, klambda.args, env)

def interpret_application(kapp, env):
    closure = interpret(kapp.function, env)
    if not isinstance(closure, KClosure):
        raise BadApplicationException(kapp)
    return interpret(
        closure.body,
        # map(lambda binding: bind(binding[0], binding[1]), zip(closure.names, kapp.args))
        recursive_extend_env(KList(closure.names), KList(kapp.args), env)
    )

def interpret_default(kexp, env):
    raise InterpretException("No interpreter for KExpression: {}".format(kexp))

########
# Helper functions
def recursive_extend_env(names, args, env):
    if names.empty:
        if args.empty:
            return env
        else:
            raise InterpretException("Bad number of arguments.")
    else:
        if args.empty:
            raise InterpretException("Bad number of names.")
        else:
            return extend_env(
                bind(first(names), first(args)),
                recursive_extend_env(
                    rest(names),
                    rest(args),
                    env
                ))
