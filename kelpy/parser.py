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
    elif kexp_match("FUNCTION ANY ANY", text[1:-1]):
        parses = kexp_to_list(text)
        f = parses[0] # Don't parse this. It won't go well.
        l = parse(parses[1])
        r = parse(parses[2])
        return KFunctionExpression(text, f, l, r)
    else:
        raise ParseException("Invalid input.")

def kexp_to_list(rawkexp):
    """
    Converts a raw KExpression form into a list of KExpressions.

    This requires that the string is a full KExpression, with braces on either
    side of the string.

    :return: A list of strings of possible KExpressions.
    """
    kexps = []
    if rawkexp[0] == '{' and rawkexp[-1] == '}':
        rawkexp = rawkexp[1:-1]
    rawkexp = rawkexp.strip()
    while len(rawkexp) > 0:
        kexp = get_smallest_kexp_from_string(rawkexp)
        kexps.append(kexp)
        rawkexp = rawkexp[len(kexp):]
        rawkexp = rawkexp.strip()
    return kexps

def get_text_through_matching_brace(text):
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
valid_types = [
    'NUMBER',
    'SYMBOL',
    'FUNCTION',
    'ANY'
]

def kexp_match(symbolic_text, literal_text):
    """
    Compares an expression text to the specially-formatted match_text to
    determine whether they are equivalent.

    :param symbolic_text: A string to match against. It can contain the symbols
        listed in `valid_types`, which describe the types of KExpressions to
        look for in the literal text.
    :param literal_text: The text inputted into the parser.
    :return: Boolean value describing equality.
    """
    # print("Symbolic: '{}'".format(symbolic_text))
    # print("Literal:  '{}'".format(literal_text))
    while any(t in symbolic_text for t in valid_types):
        # print("  Found a symbol.")
        next_type = None
        next_type_index = len(symbolic_text)
        for t in valid_types:
            index = symbolic_text.find(t)
            if  index < 0:
                continue
            if index < next_type_index:
                next_type = t
                next_type_index = index
                break
        # print("    Symbol: {}".format(next_type))
        # Now we know which type is in the symbolic text and where it starts.
        # Compare the two strings up to that point.
        symbolic_to_next = symbolic_text[:next_type_index]
        literal_to_next  = literal_text[:next_type_index]
        # print("  Comparing: '{}' == '{}'".format(symbolic_to_next, literal_to_next))
        if symbolic_to_next != literal_to_next:
            # print("  False")
            return False
        # print("    True")
        # They're equal on a literal level. Now truncate to that point and find
        # and compare the expressions.
        # print("  Adjusting strings.")
        symbolic_text = symbolic_text[next_type_index:]
        literal_text  = literal_text[next_type_index:]
        # Advance the symbolic text past the symbol.
        symbolic_text = symbolic_text[len(next_type):]
        # print("    symbolic: {}".format(symbolic_text))
        # print("    literal: {}".format(literal_text))
        # Get the shortest KExpression out of the literal text.
        kexp = get_smallest_kexp_from_string(literal_text)
        # print("  Smallest kexp: '{}'".format(kexp))
        # Check that that KExpression matches what the symbolic string things it
        # should match.
        # print("  Comparing kexp to type: {}".format(next_type))
        if not type_match(kexp, next_type):
            # print("    False")
            return False
        # print("    True")
        literal_text = literal_text[len(kexp):]
    # print("  Testing remaining: {} == {}".format(symbolic_text, literal_text))
    return symbolic_text == literal_text

def type_match(text, expression_type):
    """
    Given a set of text and a type, determines whether the given text could be
    converted to that type.

    :param text: The raw input to build the expression from.
    :param expression_type: One of the valid types to match against.
    :return: A boolean for whether the typecasting is successful.
    """
    if not expression_type in valid_types:
        raise InvalidExpressionTypeException(expression_type)
    if expression_type == 'NUMBER':
        try:
            KNumber(text)
            return True
        except ParseException:
            return False
    elif expression_type == 'SYMBOL':
        try:
            KSymbol(text)
            return True
        except ParseException:
            return False
    elif expression_type == 'FUNCTION':
        if text in FUNCTION_MAP:
            return True
        else:
            return False
    elif expression_type == 'ANY':
        try:
            KExpression(text)
            return True
        except ParseException:
            return False
    else:
        raise ImplementationException("Unhandled type match in kelpy.parser.type_match: {}".format(expression_type))
