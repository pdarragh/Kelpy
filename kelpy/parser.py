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
        tokens = []
        pairs = find_brace_pairs(text)
        next_low = 0
        for pair in pairs:
            low, high = pair
            tokens += text[next_low:low].strip().split()
            tokens.append(parse(text[low:high+1]))
            next_low = high + 1
        tokens += text[next_low:].strip().split()
        for i in xrange(len(tokens)):
            if not isinstance(tokens[i], PExpression):
                tokens[i] = PValue(tokens[i])
        self.tokens = tokens
    def __repr__(self):
        return str(self.tokens)

class PValue(object):
    def __init__(self, text):
        self.value = text
    def __repr__(self):
        return self.value

class ParseException(Exception):
    def __init__(self, message):
        super(ParseException, self).__init__("Error: {}".format(message))

class UnbalancedBracesException(ParseException):
    def __init__(self, expression):
        super(UnbalancedBracesException, self).__init__(
            "Unbalanced Braces in parsed expression: '{}'".format(expression))

class SuperfluousDataException(ParseException):
    def __init__(self, expression):
        super(SuperfluousDataException, self).__init__(
            "Extra characters outside braces in expression: '{}'".format(expression))

class NoExpressionException(ParseException):
    def __init__(self, expression):
        super(NoExpressionException, self).__init__(
            "No expression found in text: '{}'".format(expression))
