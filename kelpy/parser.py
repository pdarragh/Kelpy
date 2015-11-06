from exceptions import *
from types import *
from functions import FUNCTION_MAP

def parse(text):
    # Strip the text of extra whitespace.
    text = text.strip()
    # Now ensure the braces are balanced (if there are any).
    #TODO: Replace this with an auto-indent form.
    if text.count('{') != text.count('}'):
        raise UnbalancedBracesException(text)
    # Begin parsing for KExpressions.
    if kexp_match("NUMBER", text):
        return KNumber(text)
    elif kexp_match("SYMBOL", text):
        return KSymbol(text)
    elif kexp_match("{FUNCTION ANY ...}", text):
        parses = kexp_to_list(text)
        f = parses[0] # Don't parse this. It won't go well.
        args = [parse(arg) for arg in parses[1:]]
        return KFunctionExpression(text, f, *args)
    else:
        raise ParseException("Invalid input.")

def get_text_through_matching_brace(text):
    """
    Given a string with an opening curly brace, this method finds the substring
    up to the matching closing curly brace.

    :param text: A raw string of text.
    :return: The text up to the matching curly brace. If there is no opening
        curly brace as the first character, returns the empty string. If no
        matching curly brace is found, raises an UnbalancedBracesException.
    """
    if text[0] == '{':
        # Find the matching closing brace.
        count = 0
        r_index = 0
        for i in xrange(len(text)):
            char = text[i]
            if char == '{':
                count += 1
            elif char == '}':
                count -= 1
            if count == 0:
                r_index = i
                break
        if r_index <= 0:
            raise UnbalancedBracesException(text)
        return text[:r_index + 1]
    else:
        return ""

def get_smallest_kexp_from_string(text):
    """
    Takes a string and finds the smallest possible complete KExpression
    beginning with the first character.

    :param text: The text to search against from the beginning.
    :return: A string containing the smallest complete raw KExpression.
    """
    if not text.strip():
        # Ensure that we don't throw an error if the text is blank.
        return ""
    if text[0] == "'" and text[1] == '{':
        # Find the shortest matching brace expression starting after the
        # quote mark.
        return "'" + get_text_through_matching_brace(text[1:])
    elif text[0] == '{':
        # Find the shortest matching brace expression.
        return get_text_through_matching_brace(text)
    else:
        # In case the expression is attached to a brace, remove it.
        if text.find('}') >= 0:
            text = text[:text.find('}')]
        # Just get the whole first word.
        return text.split()[0]

# This list describes the possible symbols that `type_match` should be able to
# handle. Expand as needed.
REPEAT = '...'
valid_types = [
    'NUMBER',
    'SYMBOL',
    'FUNCTION',
    'ANY',
    REPEAT,
]

def absolute_symbol_count(symbols):
    """
    Gets the number of "absolute" symbols in a list of symbols. This is just
    the number of symbols that aren't REPEAT.

    :param symbols: A list of symbols.
    :return: The number of symbols in the list that aren't REPEAT.
    """
    return len([symbol for symbol in symbols if symbol != REPEAT])

def kexp_match(symbolic_text, literal_text):
    """
    Compares an expression text to the specially-formatted symbolic_text to
    determine whether they are equivalent.

    :param symbolic_text: A string to match against. It can contain the symbols
        listed in `valid_types`, which describe the types of KExpressions to
        look for in the literal text.
    :param literal_text: The text inputted into the parser.
    :return: Boolean value describing equality.
    """
    # Check if the symbolic text starts with a brace..
    if symbolic_text[0] == '{':
        # If it does, convert the strings to kexps.
        try:
            symbols  = kexp_to_list(symbolic_text)
            literals = kexp_to_list(literal_text)
        except:
            # Apparently one of the texts did not convert too well.
            return False
    else:
        # Otherwise, split them like regular strings.
        symbols  = symbolic_text.split()
        literals = literal_text.split()
    # Check empty lists.
    if not symbols or not literals:
        return False
    # If there is only one symbol, match it directly:
    if len(symbols) == 1 and len(literals) == 1:
        return match(symbols[0], literals[0])
    # Check the literals are at least as many as the necessary symbols.
    if not len(literals) >= absolute_symbol_count(symbols):
        return False
    # Check the lengths match if there is no repeat operation.
    if len(symbols) != len(literals) and not REPEAT in symbols:
        return False
    # Iterate over the two lists to check for valid literals.
    # This is a more complicated loop structure, so I use an pseudo-C-style
    # method with loop counters.
    s = 0               # counter for symbols
    l = 0               # counter for literals
    repeated = False    # denotes when we've just repeated a symbol via REPEAT
    while s < len(symbols) and l < len(literals):
        # First get the current symbol and literal to make life easier.
        symbol  = symbols[s]
        literal = literals[l]
        # If the symbol is the repeat symbol, we need to repeat (obviously).
        if symbol == REPEAT:
            # Decrement the symbol counter and set the 'repeated' flag.
            s -= 1
            repeated = True
            continue
        # Recursively check if the symbol matches up with the literal.
        if not kexp_match(symbol, literal):
            # Did we just check a repeat?
            if repeated:
                # If we just repeated, then maybe we've just finally moved beyond
                # the scope of the repeat indicator. Try moving on.
                s += 2
                continue
            else:
                # No repeat, so it's a positive negative result.
                # (I promise that wording makes sense.)
                return False
        # Nothing interesting happened. Increment the counters and be sure to
        # reset the 'repeated' flag.
        l += 1
        s += 1
        repeated = False
    if repeated:
        # If we were just repeating, anything will match. Ensure that we
        # actually do the final check.
        return type_match(symbols[-2], literals[-1])
    if symbols[-1] != REPEAT and (s != len(symbols) or l != len(literals)):
        return False
    # We made it out of the loop alive, which means it's a match! Woohoo!
    return True

def kexp_to_list(kexp):
    """
    Given a KExpression, converts its interior into a list of KExpressions. This
    is useful for parsing things.

    :param kexp: The text of the KExpression to parse.
    :return: A list of strings that can be KExpressions.
    """
    if kexp[0] != '{' and kexp[-1] != '}':
        raise ParseException("kexp_to_list: not a list: {}".format(kexp))
    kexp  = kexp[1:-1]
    parts = []
    while kexp:
        parts.append(get_smallest_kexp_from_string(kexp))
        index = len(parts[-1])
        kexp  = kexp[index:].strip()
    return parts

def match(symbol, literal):
    """
    Comapres a symbol and a literal for equivalence.

    :param symbol: The symbolic text to test against.
    :param literal: The raw text to test.
    :return: A boolean describing whether the expressions are equivalent.
    """
    if not literal_match(symbol, literal):
        try:
            return type_match(symbol, literal)
        except:
            return False
    return True

def literal_match(symbol, literal):
    """
    Just compares the two values literally.

    :param symbol: The symbolic text.
    :param literal: The literal text.
    :return: A boolean whether the strings are equal.
    """
    return symbol == literal

def type_match(symbol, literal):
    """
    Given a set of text and a type, determines whether the given text could be
    converted to that type.

    :param symbol: One of the valid types to match against.
    :param literal: The raw input to build the expression from.
    :return: A boolean for whether the typecasting is successful.
    """
    if not symbol in valid_types:
        raise InvalidExpressionTypeException(symbol)
    if symbol == 'NUMBER':
        try:
            KNumber(literal)
            return True
        except ParseException:
            return False
    elif symbol == 'SYMBOL':
        try:
            KSymbol(literal)
            return True
        except ParseException:
            return False
    elif symbol == 'FUNCTION':
        if literal in FUNCTION_MAP:
            return True
        else:
            return False
    elif symbol == 'ANY':
        KExpression(literal)
        return True
    else:
        raise ImplementationException("Unhandled type match in kelpy.parser.type_match: {}".format(symbol))
