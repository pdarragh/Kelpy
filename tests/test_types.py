from kelpy.types import *

from nose2.tools import params

################################################################################
# KNumber
####

@params('1', '0', '-1', '0.5', '2.5', '-3.5', '.38', '-.28', '1.0', '3/3')
def test_knumber(number):
    assert isinstance(KNumber(number), KNumber)

def test_knumber_math():
    a = KNumber(1)
    b = KNumber(2)
    assert (a + b) == KNumber(3)
    assert (a - b) == KNumber(-1)
    assert (a * b) == KNumber(2)
    assert (a // b) == KNumber(0)
    assert (a / b) == KNumber(0)
    assert (a % b) == KNumber(1)
    assert (a < b) == True
    assert (a <= b) == True
    assert (a == b) == False
    assert (a != b) == True
    assert (a >= b) == False
    assert (a > b) == False
    assert bool(a) == True

################################################################################
# KList
####

def test_klist_math():
    a = KList(KNumber(1), KNumber(2), KNumber(3))
    b = KList(KNumber(4), KNumber(5), KNumber(6))
    assert bool(a) == True
    assert (a == b) == False
    assert (a != b) == True
    assert (a == '') == False
    assert KList() == KList()
    assert a != KList()
    for x in a:
        pass
    assert a.first == KNumber(1)
    assert a.rest == KList(KNumber(2), KNumber(3))
    assert a.empty == False
    assert a.reversed == KList(KNumber(3), KNumber(2), KNumber(1))
