class ParseException(Exception):
    def __init__(self, message, expression=None):
        if expression is not None:
            message = message[:-1] + ": '{}'".format(expression)
        super(ParseException, self).__init__("Error: {}".format(message))

class UnbalancedBracesException(ParseException):
    def __init__(self, expression=None):
        message = "Unbalanced Braces in parsed expression."
        super(UnbalancedBracesException, self).__init__(message, expression)

class SuperfluousDataException(ParseException):
    def __init__(self, expression=None):
        message = "Extra characters outside braces in expression."
        super(SuperfluousDataException, self).__init__(message, expression)

class NoExpressionException(ParseException):
    def __init__(self, expression=None):
        message = "No expression found in text."
        super(NoExpressionException, self).__init__(message, expression)

class NoArgumentsException(ParseException):
    def __init__(self, expression=None):
        message = "Cannot create empty expression."
        super(NoArgumentsException, self).__init__(message, expression)

class InvalidFunctionException(ParseException):
    def __init__(self, expression=None):
        message = "Invalid function name given."
        super(InvalidFunctionException, self).__init__(message, expression)

class InvalidNumberException(ParseException):
    def __init__(self, expression=None):
        message = "Invalid number format given."
        super(InvalidNumberException, self).__init__(message, expression)
