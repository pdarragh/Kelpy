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
        text = text.strip()
        tokens = []
        pairs = find_brace_pairs(text)
        next_low = 0
        for pair in pairs:
            low, high = pair
            tokens += text[next_low:low].split()
            tokens.append(parse(text[low:high+1]))
            next_low = high + 1
        tokens += text[next_low:].split()
        for i in xrange(len(tokens)):
            if not isinstance(tokens[i], PExpression):
                tokens[i] = PValue(tokens[i])
        if len(tokens) == 0:
            raise NoArgumentsException(text)
        self.tokens = tokens
    def __repr__(self):
        return str(self.tokens)

class PValue(object):
    def __init__(self, text):
        self.value = text
    def __repr__(self):
        return self.value
