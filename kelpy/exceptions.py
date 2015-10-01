class ParseException(Exception):
    def __init__(self, message):
        super(ParseException, self).__init__("Error: {}".format(message))

class UnbalancedBracesException(ParseException):
    def __init__(self, expression=None):
        message = "Unbalanced Braces in parsed expression."
        if expression is not None:
            message = message[:-1] + ": '{}'".format(expression)
        super(UnbalancedBracesException, self).__init__(message)

class SuperfluousDataException(ParseException):
    def __init__(self, expression=None):
        message = "Extra characters outside braces in expression."
        if expression is not None:
            message = message[:-1] + ": '{}'".format(expression)
        super(SuperfluousDataException, self).__init__(message)

class NoExpressionException(ParseException):
    def __init__(self, expression=None):
        message = "No expression found in text."
        if expression is not None:
            message = message[:-1] + ": '{}'".format(expression)
        super(NoExpressionException, self).__init__(message)

class NoArgumentsException(ParseException):
    def __init__(self, expression=None):
        message = "Cannot create empty expression."
        if expression is not None:
            message = message[:-1] + ": '{}'".format(expression)
        super(NoArgumentsException, self).__init__(message)
