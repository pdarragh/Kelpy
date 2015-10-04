# Kelpy

## Description

Kelpy is a parser and interpreter for a made-up functional language. This language is based on the coursework done at the Unviersity of Utah's CS 5510 "Programming Languages" course, taught by Matthew Flatt.

My goal in writing Kelpy was to gain further insight into the language created in-class over the course of the semester. In class we used the [Racket](https://github.com/racket/racket) programming language, which is much better suited for such things. However, I'm much more familiar with Python and thought it would be a fun and challenging project to try to implement this in my preferred language.

## Note on the Documentation

Throughout the documentation, I will refer to the parsed language (the language that you write, which is read by the `kelpy.py` interpreter) as "KL" (the Kelpy Language). This language is parsed into various Python objects, and those objects will be interpreted and converted into a result.

## Types of Objects

### PObject

`PObject` is the inherited type for all parsed objects.

#### PExpression

The `PExpression` is the quintessential parsed object. Each `PExpression` contains a function and one or more arguments. In the KL, PExpressions are written as:

```
{ <func> <arg> ... }
```

Where `<func>` represents a function symbol (e.g. `+`, `*`, etc.), `<arg>` represents any other `PObject`, and `...` symbolizes that you can have any additional number of arguments.

#### PFunction

A `PFunction` is the representation of a function in KL. Whenever you write something at the front of a `PExpression`, it's assumed to be a `PFunction`. There are only a few acceptable `PFunction` values; if you don't use one of those, you will get a parse error.

#### PNumber

`PNumber`s contain numeric values. They can be written in the KL any way a number can be written regularly, e.g.:

* `42` – an integer
* `3.89` – a fractional value
* `.789` – yes, it even accepts fractional values without a leading 0

The `PNumber` is necessary to evaluate the value of expressions. For example, the KL `{+ 1 3}` uses both `1` and `3` as `PNumber`s and will pass them to the interpreter as such.

#### PSymbol

A `PSymbol` can be thought of as a variable name. Anything that doesn't convert into any other `PObject` will be assumed to be a `PSymbol`.

### Interpreted Objects
