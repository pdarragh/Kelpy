################################################################################
#
# exceptions.py
#
# This module defines all of the exceptions used in the Kelpy environment.
#
################################################################################

################################################################################
# KelpyException
#
# The root object from which all other custom exceptions are made. This makes it
# convenient to write try/except blocks around.
####

class KelpyException(Exception):
    """
    Used to subclass all exceptions in the Kelpy environment. Never created
    directly.
    """
    pass

################################################################################
# Implementation Exception
#
# These are errors in the implementation, such as if a method is called
# correctly with valid values but there is nothing to handle it.
####

class ImplementationException(KelpyException):
    def __init__(self, message):
        super(ImplementationException, self).__init__("Implementation Error: {}".format(message))

################################################################################
# Interpreter Exceptions
####

class InterpretException(KelpyException):
    def __init__(self, message):
        super(InterpretException, self).__init__("Interpret Error: {}".format(message))

class InvalidFunctionException(InterpretException):
    def __init__(self, function):
        message = "Tried to evaluate a function without a definition: '{}'".format(function)
        super(InvalidFunctionException, self).__init__(message)

class InvalidArgumentsException(InterpretException):
    def __init__(self, function, arguments):
        message = "Function: {}. Invalid arguments given: {}".format(function, arguments)
        super(InvalidArgumentsException, self).__init__(message)

class TooFewArgumentsException(InterpretException):
    def __init__(self, function, arguments):
        message = "Function: {}. Too few ({}) arguments given: {}".format(function, len(arguments), arguments)
        super(TooFewArgumentsException, self).__init__(message)

class UninterpretedSymbolException(InterpretException):
    def __init__(self, kfunction, env):
        message = "Symbol without binding in function ({function}) and environment ({env}).".format(
            function = kfunction,
            env      = env
        )
        super(UninterpretedSymbolException, self).__init__(message)

################################################################################
# Parser Exceptions
####

class ParseException(KelpyException):
    def __init__(self, message, expression=None):
        if expression is not None:
            message = message[:-1] + ": '{}'".format(expression)
        super(ParseException, self).__init__("Parse Error: {}".format(message))

class RawExpressionException(ParseException):
    def __init__(self):
        message = "Cannot create a raw KExpression object."
        super(RawExpressionException, self).__init__(message)

class BadRepeatTypeException(ParseException):
    def __init__(self, expression=None):
        message = "Attempted to use repeat type without a previous type."
        super(BadRepeatTypeException, self).__init__(message, expression)

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

class FunctionlessExpressionException(ParseException):
    def __init__(self, expression=None):
        message = "No valid leading function in expression."
        super(FunctionlessExpressionException, self).__init__(message, expression)

class NoArgumentsException(ParseException):
    def __init__(self, expression=None):
        message = "Cannot create empty expression."
        super(NoArgumentsException, self).__init__(message, expression)

class RawPrimitiveException(ParseException):
    def __init__(self, expression=None):
        message = "Cannot create a raw KPrimitive."
        super(RawPrimitiveException, self).__init__(message, expression)

class InvalidListException(ParseException):
    def __init__(self, expression=None):
        message = "Invalid list creation."
        super(InvalidListException, self).__init__(message, expression)

class BadListIndexException(ParseException):
    def __init__(self, expression=None):
        message = "Cannot access index of list."
        super(BadListIndexException, self).__init__(message, expression)

class InvalidFirstException(ParseException):
    def __init__(self, expression=None):
        message = "Could not get 'first' from expression."
        super(InvalidFirstException, self).__init__(message, expression)

class InvalidRestException(ParseException):
    def __init__(self, expression=None):
        message = "Could not get 'rest' from expression."
        super(InvalidRestException, self).__init__(message, expression)

class InvalidReverseException(ParseException):
    def __init__(self, expression=None):
        message = "Could not get 'reverse' from expression."
        super(InvalidReverseException, self).__init__(message, expression)

class InvalidPrependException(ParseException):
    def __init__(self, expression=None):
        message = "Could not prepend value to list."
        super(InvalidPrependException, self).__init__(message, expression)

class InvalidAppendException(ParseException):
    def __init__(self, expression=None):
        message = "Could not append value to list."
        super(InvalidAppendException, self).__init__(message, expression)

class BadLookupException(ParseException):
    def __init__(self, expression=None):
        message = "Could not find symbol in environment."
        super(BadLookupException, self).__init__(message, expression)

class InvalidFunctionException(ParseException):
    def __init__(self, expression=None):
        message = "Invalid function name given."
        super(InvalidFunctionException, self).__init__(message, expression)

class InvalidNumberException(ParseException):
    def __init__(self, expression=None):
        message = "Invalid number format given."
        super(InvalidNumberException, self).__init__(message, expression)

class InvalidSymbolException(ParseException):
    def __init__(self, expression=None):
        message = "Invalid symbol format given."
        super(InvalidSymbolException, self).__init__(message, expression)

class InvalidBooleanException(ParseException):
    def __init__(self, expression=None):
        message = "Invalid boolean format given."
        super(InvalidBooleanException, self).__init__(message, expression)

class InvalidExpressionTypeException(ParseException):
    def __init__(self, expression=None):
        message = "Invalid expression type given to parser."
        super(InvalidExpressionTypeException, self).__init__(message, expression)
