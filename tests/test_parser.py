from kelpy import parser
from kelpy.types import *
from kelpy.exceptions import *
from kelpy.functions import FUNCTION_MAP

from nose2.tools import params
from nose2.tools.such import helper

################################################################################
# parse
####

@params('0', '892', '-1', '.235', '-1.3589', '-.235')
def test_parse_number(number):
    assert isinstance(parser.parse(number), KNumber)

@params("'blah", "'something")
def test_parse_symbol(symbol):
    assert isinstance(parser.parse(symbol), KSymbol)

@params('true', 'True', '#t', '#f', 'FALSE')
def test_parse_bool(boolean):
    assert isinstance(parser.parse(boolean), KBoolean)

@params("{+ 2}", "{+ 'blah}")
def test_parse_function(function):
    assert isinstance(parser.parse(function), KFunctionExpression)

@params('empty', '{list}')
def test_parse_empty_list(text):
    assert parser.parse(text) == KList()
    assert parser.parse('{{empty? {}}}'.format(text)) == KBoolean(True)

@params('{list 1}', 'empty', '{list 2 {+ 1 2 3}}', "{list 'x 'y}")
def test_parse_list(text):
    assert isinstance(parser.parse(text), KList)

def test_parse_list_other():
    assert parser.parse('{first {list 1 2 3}}') == KNumber(1)
    assert parser.parse('{second {list 1 2 3}}') == KNumber(2)
    assert parser.parse('{rest {list 1 2 3}}') == KList(KNumber(2), KNumber(3))
    assert parser.parse('{prepend 1 {list 2 3}}') == KList(KNumber(1), KNumber(2), KNumber(3))
    assert parser.parse('{append 3 {list 1 2}}') == KList(KNumber(1), KNumber(2), KNumber(3))

@params('{if 0 1 2}')
def test_parse_if(text):
    assert isinstance(parser.parse(text), KIf)

@params("{let {'x 3} 0}")
def test_parse_let(text):
    assert isinstance(parser.parse(text), KLet)

@params('blah blah blah')
def test_parse_parseexception(text):
    helper.assertRaises(ParseException, parser.parse, text)

@params('{blah', '{1 2} 3}', '{{ blah }{}{{}}}}}')
def test_parse_unbalanced_braces(text):
    helper.assertRaises(UnbalancedBracesException, parser.parse, text)

################################################################################
# get_text_through_matching_brace (gttmb)
####

@params('', 'blah', 'something}', 'blah blah blah', ' {blah}')
def test_gttmb_empty(text):
    assert parser.get_text_through_matching_brace(text) == ''

@params('{blah', '{{double blah}')
def test_gttmb_exceptions(text):
    helper.assertRaises(UnbalancedBracesException, parser.get_text_through_matching_brace, text)

def test_gttmb():
    assert parser.get_text_through_matching_brace('{a b c}') == '{a b c}'
    assert parser.get_text_through_matching_brace('{a b} c') == '{a b}'
    assert parser.get_text_through_matching_brace('{}') == '{}'

################################################################################
# get_smallest_kexp_from_string (gskfs)
####

@params('', '   ')
def test_gskfs_empty(text):
    assert parser.get_smallest_kexp_from_string(text) == ''

@params('1', 'blah', '{1 2 3}', "'blah", "'{long symbol test}")
def test_gskfs_identity(text):
    assert parser.get_smallest_kexp_from_string(text) == text

def test_gskfs():
    assert parser.get_smallest_kexp_from_string('{1 2 3} 4 5') == '{1 2 3}'
    assert parser.get_smallest_kexp_from_string('1 {2 3 4}') == '1'

################################################################################
# absolute_symbol_count
####

def test_absolute_symbol_count():
    assert parser.absolute_symbol_count('NUMBER SYMBOL'.split()) == 2
    assert parser.absolute_symbol_count('NUMBER ... SYMBOL'.split()) == 2
    assert parser.absolute_symbol_count('ANY'.split()) == 1
    assert parser.absolute_symbol_count(''.split()) == 0

################################################################################
# kexp_match
####

@params('1', '0', '-2', '0.29', '-190.2')
def test_kexp_match_number(number):
    assert parser.kexp_match('NUMBER', number)

@params("'blah", "'{long symbol}")
def test_kexp_match_symbol(symbol):
    assert parser.kexp_match('SYMBOL', symbol)

@params('true', 'True', '#t', '#f', 'FALSE')
def test_kexp_match_bool(boolean):
    assert parser.kexp_match('BOOLEAN', boolean)

@params(*FUNCTION_MAP)
def test_kexp_match_function(function):
    assert parser.kexp_match('FUNCTION', function)

@params('1', '+', "'blah", "{{1 2 3}}")
def test_kexp_match_any(kexp):
    assert parser.kexp_match('ANY', kexp)

@params('1 2 3', '0 -39 0.12', '939', '2 4')
def test_kexp_match_number_repeat(numbers):
    assert parser.kexp_match('NUMBER ...', numbers)

@params("'one 'two", "'blah", "'something 'something 'something")
def test_kexp_match_symbol_repeat(symbols):
    assert parser.kexp_match('SYMBOL ...', symbols)

@params('true false #t', 'True TRUE true', '#t #f #f #t', '#f')
def test_kexp_match_bool_repeat(booleans):
    assert parser.kexp_match('BOOLEAN ...', booleans)

@params('1 2 3', "1 'blah", "'blah", '4 5 {+ 1 2}', "{* 2 0} 'blah 3")
def test_kexp_match_any_repeat(kexps):
    assert parser.kexp_match('ANY ...', kexps)

def test_kexp_match():
    assert parser.kexp_match('NUMBER ... SYMBOL', "1 2 3 'blah")
    assert parser.kexp_match('{FUNCTION NUMBER NUMBER}', '{+ 1 2}')
    assert parser.kexp_match('{test ANY NUMBER ...}', "{test 'blah 1 2 3}")
    assert parser.kexp_match('', '')
    assert parser.kexp_match('ANY NUMBER SYMBOL ...', "{+ 1 2} 3 'blah 'something 'anotherthing")

def test_kexp_match_false():
    assert not parser.kexp_match('', 'blah')
    assert not parser.kexp_match('SYMBOL', '')
    assert not parser.kexp_match('SYMBOL NUMBER', "'blah")
    assert not parser.kexp_match('{NUMBER SYMBOL}', "{'blah 2}")
    assert not parser.kexp_match('NUMBER ...', "1 2 'blah")

################################################################################
# string_to_kexp_strings
####

def test_string_to_kexp_strings_empty():
    assert parser.string_to_kexp_strings('') == []

################################################################################
# kexp_to_list
####

def test_kexp_to_list():
    assert parser.kexp_to_list('{1 2 3}') == ['1', '2', '3']
    assert parser.kexp_to_list("{+ 1 'x}") == ['+', '1', "'x"]
    assert parser.kexp_to_list('{}') == []

@params('blah', '{+ 1 2', '{{blah ')
def test_kexp_to_list_exceptions(kexp):
    helper.assertRaises(ParseException, parser.kexp_to_list, kexp)

################################################################################
# match
####

def test_match():
    assert parser.match('literal', 'literal')
    assert not parser.match('symbolic', 'literal')

################################################################################
# literal_match
####

def test_literal_match():
    assert parser.literal_match('blah', 'blah')
    assert parser.literal_match('', '')

################################################################################
# type_match
####

@params('1', '0', '-39', '0.293', '-.290')
def test_type_match_number(number):
    assert parser.type_match('NUMBER', number)

@params('blah', "'something", '{+ 1 2}')
def test_type_match_number_false(nonnumber):
    assert not parser.type_match('NUMBER', nonnumber)

@params("'x", "'something", "'{a long symbol}")
def test_type_match_symbol(symbol):
    assert parser.type_match('SYMBOL', symbol)

@params('1', '+', 'blah')
def test_type_match_symbol_false(nonsymbol):
    assert not parser.type_match('SYMBOL', nonsymbol)

@params('true', 'True', '#t', '#f', 'FALSE')
def test_type_match_bool(boolean):
    assert parser.type_match('BOOLEAN', boolean)

@params('1', "'blah", '#g')
def test_type_match_bool_false(nonboolean):
    assert not parser.type_match('BOOLEAN', nonboolean)

@params(*FUNCTION_MAP)
def test_type_match_function(function):
    assert parser.type_match('FUNCTION', function)

@params('blah', '1', "'blah")
def test_type_match_function_false(nonfunction):
    assert not parser.type_match('FUNCTION', nonfunction)

@params('1', "'x", '{+ 1 2}')
def test_type_match_any(kexp):
    assert parser.type_match('ANY', kexp)

def test_type_match_invalidexpression():
    helper.assertRaises(InvalidExpressionTypeException, parser.type_match, 'blah', '1')
