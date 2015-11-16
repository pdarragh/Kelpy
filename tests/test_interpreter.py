from kelpy import interpreter
from kelpy.types import *
from kelpy.exceptions import *

from nose2.tools import params
from nose2.tools.such import helper

################################################################################
# interpret
####

def test_interpret_unparsed():
    helper.assertRaises(InterpretException, interpreter.interpret, 'blah', 'something')

def test_interpret_symbol():
    env = KEnvironment(KBinding(KSymbol("'x"), KNumber(1)))
    assert interpreter.interpret(KSymbol("'x"), env) == KNumber(1)

def test_interpret_function():
    func = KAdd(*[KNumber(1), KNumber(2)])
    assert interpreter.interpret(func, empty_env) == KNumber(3)

def test_interpret_if():
    kif_true = KIf(KBoolean(True), KNumber(0), KNumber(1))
    kif_false = KIf(KBoolean(False), KNumber(0), KNumber(1))
    assert interpreter.interpret(kif_true, empty_env) == KNumber(0)
    assert interpreter.interpret(kif_false, empty_env) == KNumber(1)
