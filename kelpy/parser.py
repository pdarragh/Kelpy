import re
from exceptions import *

def parse(text):
    text = text.strip()
    if text.count('{') == 0:
        raise NoExpressionException(text)
    if text.count('{') != text.count('}'):
        raise UnbalancedBracesException(text)
    if text[0] != '{' or text[-1] != '}':
        raise SuperfluousDataException(text)
    return PExpression(text[1:-1])

def find_brace_pairs(text):
    if not text:
        return []
    text = text.strip()
    pairs = []
    l_index = text.find('{')
    while l_index >=0 and l_index < len(text):
        count = 1
        r_index = l_index
        for i in xrange(l_index + 1, len(text)):
            char = text[i]
            if char == '{':
                count += 1
            elif char == '}':
                count -= 1
            if count == 0:
                r_index = i
                break
        if r_index <= l_index:
            raise UnbalancedBracesException(text)
        pairs.append( (l_index, r_index) )
        move_forward = text[r_index:].find('{')
        if move_forward == -1:
            break
        l_index = r_index + move_forward
    return pairs

class PExpression(object):
    def __init__(self, text):
        """
        The PExpression is created from the interior of a braced expression.
        This means that if your base string is:
            text = "{ one two three }"
        then you should create the PExpression with:
            PExpression(text[1:-1])
        """
        # Strip the text. This fixes some problems.
        text = text.strip()
        # Prepare a place to store all the parsed tokens.
        tokens = []
        # Find the brace pairs. This is used to group expressions and values.
        pairs = find_brace_pairs(text)
        # Iterate over each pair. Each pair represents an expression, so
        # everything within a brace pair will be parsed as a PExpression via
        # `parse`, and everything else will be put into a PValue.
        next_low = 0
        for pair in pairs:
            low, high = pair
            tokens += text[next_low:low].split()
            tokens.append(parse(text[low:high+1]))
            next_low = high + 1
        tokens += text[next_low:].split() # get the last token
        # Iterate over the tokens, replacing them with their parsed values.
        for i in xrange(len(tokens)):
            if not isinstance(tokens[i], PExpression):
                tokens[i] = get_PValue_from_raw(tokens[i])
        if len(tokens) == 0:
            raise NoArgumentsException(text)
        # Save those tokens!
        self.tokens = tokens
    def __repr__(self):
        result = "["
        for token in self.tokens[:-1]:
            result += repr(token) + ", "
        result += repr(self.tokens[-1]) + "]"
        return result
    def __str__(self):
        result = "("
        for token in self.tokens[:-1]:
            result += str(token) + " "
        result += str(self.tokens[-1]) + ")"
        return result

def get_PValue_from_raw(raw):
    try:
        return PNumber(raw)
    except InvalidNumberException:
        # Not a number...
        pass
    try:
        return PFunction(raw)
    except InvalidFunctionException:
        # Not a function...
        pass
    # Must be a symbol.
    return PSymbol(raw)

class PValue(object):
    def __init__(self, raw):
        self.raw = raw
        self.type = 'raw'

class PSymbol(PValue):
    def __init__(self, symbol):
        self.raw = symbol
        self.type = 'symbol'
    def __repr__(self):
        return "<sym: {raw}>".format(raw=self.raw)
    def __str__(self):
        return "'{raw}".format(raw=self.raw)

class PNumber(PValue):
    def __init__(self, number):
        self.raw = number
        integer     = re.compile(r"^-?\d+$")
        floating_nd = re.compile(r"^-?\d+.\d*$")
        floating_wd = re.compile(r"^-?\d*.\d+$")
        if not (re.match(integer, self.raw) or
                re.match(floating_nd, self.raw) or
                re.match(floating_wd, self.raw)):
            raise InvalidNumberException(number)
        self.type = 'number'
    def __repr__(self):
        return "<num: {raw}>".format(raw=self.raw)
    def __str__(self):
        return self.raw

functions = [
    '+',
    '*',
]

class PFunction(PValue):
    def __init__(self, function):
        self.raw = function.lower()
        if self.raw not in functions:
            raise InvalidFunctionException(function)
        self.type = 'function'
    def __repr__(self):
        return "<func: {raw}>".format(raw=self.raw)
    def __str__(self):
        return self.raw
