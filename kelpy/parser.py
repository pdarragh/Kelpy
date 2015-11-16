from exceptions import *
from types import *
from functions import FUNCTION_MAP

def parse(text):
    # Strip the text of extra whitespace.
    text = text.strip()
    # Now ensure the braces are balanced (if there are any).
    #TODO: Replace this with an auto-indent form.
    check_matching_braces(text)
    # Begin parsing for KExpressions.
    ####
    # Primitives
    if kexp_match("NUMBER", text):
        return KNumber(text)
    elif kexp_match("SYMBOL", text):
        return KSymbol(text)
    elif kexp_match("BOOLEAN", text):
        return KBoolean(text)
    ####
    # Lists
    elif kexp_match("empty", text):
        return KList()
    elif kexp_match("{list}", text):
        return KList()
    elif kexp_match("{list NUMBER -> NUMBER}", text):
        parses  = kexp_to_list(text)
        low     = parse(parses[1])
        high    = parse(parses[3])
        if not low.integer or not high.integer:
            raise ParseException("Bad exclusive list definition.")
        values = [KNumber(x) for x in xrange(low.value, high.value)]
        return KList(*values)
    elif kexp_match("{list NUMBER => NUMBER}", text):
        parses  = kexp_to_list(text)
        low     = parse(parses[1])
        high    = parse(parses[3])
        if not low.integer or not high.integer:
            raise ParseException("Bad inclusive list definition.")
        values = [KNumber(x) for x in xrange(low.value, high.value + 1)]
        return KList(*values)
    elif kexp_match("{list ANY ...}", text):
        parses = kexp_to_list(text)
        return KList([parse(part) for part in parses[1:]])
    elif kexp_match("{empty? ANY}", text):
        parses = kexp_to_list(text)
        return KBoolean(parse(parses[1]) == KList())
    elif kexp_match("{first ANY}", text):
        parses = kexp_to_list(text)
        return first(parse(parses[1]))
    elif kexp_match("{second ANY}", text):
        parses = kexp_to_list(text)
        return first(rest(parse(parses[1])))
    elif kexp_match("{rest ANY}", text):
        parses = kexp_to_list(text)
        return rest(parse(parses[1]))
    elif kexp_match("{reverse ANY}", text):
        parses = kexp_to_list(text)
        return reverse(parse(parses[1]))
    elif kexp_match("{prepend ANY ANY}", text):
        parses = kexp_to_list(text)
        return prepend(
            parse(parses[1]),
            parse(parses[2])
        )
    elif kexp_match("{append ANY ANY}", text):
        parses = kexp_to_list(text)
        return append(
            parse(parses[1]),
            parse(parses[2])
        )
    ####
    # Functions
    elif kexp_match("{+ ANY ANY ...}", text):
        return KAdd(*parse_function_args(text))
    elif kexp_match("{* ANY ANY ...}", text):
        return KMultiply(*parse_function_args(text))
    elif kexp_match("{- ANY ANY ...}", text):
        return KSubtract(*parse_function_args(text))
    elif kexp_match("{/ ANY ANY ...}", text):
        return KDivide(*parse_function_args(text))
    elif kexp_match("{% ANY ANY ...}", text):
        return KModulo(*parse_function_args(text))
    elif kexp_match("{== ANY ANY ...}", text):
        return KEquality(*parse_function_args(text))
    elif kexp_match("{!= ANY ANY ...}", text):
        return KInequality(*parse_function_args(text))
    elif kexp_match("{< ANY ANY ...}", text):
        return KLessThan(*parse_function_args(text))
    elif kexp_match("{> ANY ANY ...}", text):
        return KGreaterThan(*parse_function_args(text))
    elif kexp_match("{<= ANY ANY ...}", text):
        return KLessThanEqual(*parse_function_args(text))
    elif kexp_match("{>= ANY ANY ...}", text):
        return KGreaterThanEqual(*parse_function_args(text))
    ####
    # Control Flow
    elif kexp_match("{if ANY ANY ANY}", text):
        parses = kexp_to_list(text)
        return KIf(
            parse(parses[1]),
            parse(parses[2]),
            parse(parses[3])
        )
    ####
    # Environment
    elif kexp_match("{let {SYMBOL ANY} ANY}", text):
        parses = kexp_to_list(text)
        interior = kexp_to_list(parses[1])
        return KLet(
            parse(interior[0]),
            parse(interior[1]),
            parse(parses[2])
        )
    ####
    # Lambda
    elif kexp_match("{lambda {SYMBOL ...} ANY}", text):
        parses = kexp_to_list(text)
        symbols = kexp_to_list(parses[1])
        return KLambda(
            parse(parses[-1]),
            [parse(symbol) for symbol in symbols]
        )
    ####
    # Functions
    elif kexp_match("{ANY ANY ...}", text):
        parses = kexp_to_list(text)
        return KApplication(
            parse(parses[0]),
            parse_function_args(text)
        )
    ####
    # Something else
    else:
        raise ParseException("Invalid input.")

def parse_function_args(text):
    parses = kexp_to_list(text)
    return [parse(arg) for arg in parses[1:]]

BRACES = {
    '{': '}',
    '[': ']',
    '(': ')',
}

def check_matching_braces(text):
    """
    Ensures that the text has a matching number of each type of brace.

    :param text: Input text to check.
    :return: Boolean for whether the braces match in numbers.
    """
    for opening, closing in BRACES.iteritems():
        if text.count(opening) != text.count(closing):
            raise UnbalancedBracesException(text)

def is_opening_brace(text):
    """
    Whether a text is an opening brace.

    :param text: Raw string.
    :return: Boolean for whether the text is an opening brace.
    """
    return text in BRACES

def is_closing_brace(text):
    """
    Whether a text is a closing brace.

    :param text: Raw string.
    :return: Boolean for whether the text is a closing brace.
    """
    return text in BRACES.values()

def matching_brace(brace):
    """
    Gets the appropriate matching brace for a given brace, regardless of whether
    the brace is an opening or closing brace.

    :param brace: An input brace.
    :return: The matching brace.
    """
    for opening, closing in BRACES.iteritems():
        if brace == opening:
            return closing
        if brace == closing:
            return opening
    return ''

def get_text_through_matching_brace(text):
    """
    Given a string with an opening curly brace, this method finds the substring
    up to the matching closing curly brace.

    :param text: A raw string of text.
    :return: The text up to the matching curly brace. If there is no opening
        curly brace as the first character, returns the empty string. If no
        matching curly brace is found, raises an UnbalancedBracesException.
    """
    if not text:
        return ''
    if is_opening_brace(text[0]):
        # Find the matching closing brace.
        count = 0
        r_index = 0
        for i in xrange(len(text)):
            char = text[i]
            if is_opening_brace(char):
                count += 1
            elif is_closing_brace(char):
                count -= 1
            if count == 0:
                if char == matching_brace(text[0]):
                    r_index = i
                    break
                else:
                    raise UnbalancedBracesException(text)
        if r_index <= 0:
            raise UnbalancedBracesException(text)
        return text[:r_index + 1]
    else:
        return ''

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
    if text[0] == "'" and is_opening_brace(text[1]):
        # Find the shortest matching brace expression starting after the
        # quote mark.
        return "'" + get_text_through_matching_brace(text[1:])
    elif is_opening_brace(text[0]):
        # Find the shortest matching brace expression.
        return get_text_through_matching_brace(text)
    else:
        # Check all the types of braces to see if the current expression is
        # attached to a closing brace. If it is, remove it.
        closest = -1
        for brace in BRACES.values():
            if text.find(brace) >= 0 and text.find(brace) < closest:
                closest = text.find(brace)
        if closest >= 0:
            text = text[:closest]
        # Just get the whole first word.
        return text.split()[0]

# This list describes the possible symbols that `type_match` should be able to
# handle. Expand as needed.
REPEAT = '...'
valid_types = [
    'NUMBER',
    'SYMBOL',
    'BOOLEAN',
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
    if not symbolic_text or not literal_text:
        return symbolic_text == literal_text
    # Check if the symbolic text starts with a brace..
    if is_opening_brace(symbolic_text[0]):
        # If it does, convert the strings to kexps.
        try:
            symbols  = kexp_to_list(symbolic_text)
            literals = kexp_to_list(literal_text)
        except:
            # Apparently one of the texts did not convert too well.
            return False
    else:
        # Otherwise, split them like regular strings.
        symbols  = string_to_kexp_strings(symbolic_text)
        literals = string_to_kexp_strings(literal_text)
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
        return match(symbols[-2], literals[-1])
    # Guarantee that if there was a repeat somewhere in the code and we exited
    # the loop, that we actually completed iteration over both lists.
    if symbols[-1] != REPEAT and (s != len(symbols) or l != len(literals)):
        return False
    # We made it out of the loop alive, which means it's a match! Woohoo!
    return True

def string_to_kexp_strings(text):
    """
    Converts a raw text string into strings that could be turned into
    KExpressions.

    :param text: The raw text to be converted.
    :return: A list of strings that can be KExpressions.
    """
    if not text:
        return []
    tokens = []
    while text:
        tokens.append(get_smallest_kexp_from_string(text))
        index = len(tokens[-1])
        text  = text[index:].strip()
    return tokens

def kexp_to_list(kexp):
    """
    Given a KExpression, converts its interior into a list of KExpressions. This
    is useful for parsing things.

    :param kexp: The text of the KExpression to parse.
    :return: A list of strings that can be KExpressions.
    """
    if not is_opening_brace(kexp[0]) or not is_closing_brace(kexp[-1]):
        raise ParseException("kexp_to_list: not a list: {}".format(kexp))
    kexp  = kexp[1:-1]
    return string_to_kexp_strings(kexp)

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
    elif symbol == 'BOOLEAN':
        try:
            KBoolean(literal)
            return True
        except ParseException:
            return False
    elif symbol == 'ANY':
        return True
    else:
        raise ImplementationException(
            "Unhandled type match in kelpy.parser.type_match: {}".format(symbol)
        ) # pragma: no cover
