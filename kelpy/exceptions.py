class ParseException(Exception):
    def __init__(self, message):
        super(ParseException, self).__init__("Error: {}".format(message))

class UnbalancedBracesException(ParseException):
    def __init__(self, expression=None):
        if expression is None:
            super(UnbalancedBracesException, self).__init__(
                "Unbalanced Braces in parsed expression.")
        else:
            super(UnbalancedBracesException, self).__init__(
                "Unbalanced Braces in parsed expression: '{}'".format(expression))

class SuperfluousDataException(ParseException):
    def __init__(self, expression=None):
        super(SuperfluousDataException, self).__init__(
            "Extra characters outside braces in expression: '{}'".format(expression))

class NoExpressionException(ParseException):
    def __init__(self, expression=None):
        super(NoExpressionException, self).__init__(
            "No expression found in text: '{}'".format(expression))
