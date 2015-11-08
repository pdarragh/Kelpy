# Kelpy

A parser and interpreter for a made-up prefix (Polish) notation language.

## Table of Contents

* [Description](#description)
* [Note on the Documentation](#note-on-the-documentation)
* [Usage](#usage)
* [Types of Objects](#types-of-objects)
* [The Future](#the-future)
    - [Language Enhancements](#language-enhancements)

## Description

Kelpy is a parser and interpreter for a made-up prefix operator language. This language is based on the coursework done in the Unviersity of Utah's CS 5510 "Programming Languages" course, taught by Matthew Flatt (GitHub: @mflatt).

My goal in writing Kelpy was to gain further insight into the language created in-class over the course of the semester. In class we used the [Racket](https://github.com/racket/racket) programming language, which is much better suited for such things. However, I'm much more familiar with Python and thought it would be a fun and challenging project to try to implement this in my preferred language with my own changes.

## Note on the Documentation

Throughout the documentation, I will refer to the parsed language (the language that you write, which is read by the `kelpy.py` interpreter) as "KL" (the Kelpy Language). This language is parsed into various Python objects, and those objects will be interpreted and converted into a result.

## Usage

To try out Kelpy, just run the interpreter! You can either `chmod +x kelpy.py` or simply `python kelpy.py` to get started.

Right now Kelpy doesn't do too much. It can do some nested arithmetic, really. Kelpy is a prefix-operated language, and the supported mathematical operations so far are `+` addition, `-` subtraction, `*` multiplication, `/` division, and `%` modulo. By default, Kelpy will output the uninterpreted values of your expression before getting the result.

```
>>> 1
~ 1
1
>>> 'x
~ 'x
need lookup
'x
>>> {+ 1 2}
~ KFAdd(1, 2)
3
>>> {* 6 7}
~ KFMultiply(6, 7)
42
>>> {+ 1 2 3 4 5}
~ KFAdd(1, 2, 3, 4, 5)
15
>>> {+ 1 2 3 {* 6 7} {/ 9 3}}
~ KFAdd(1, 2, 3, KFMultiply(6, 7), KFDivide(9, 3))
51
```

There are a few command-line options for Kelpy, too:

| Option                |Purpose                                            |
|-----------------------|---------------------------------------------------|
| `-h`, `--help`        | Shows the help information and quits.             |
| `-q`, `--quiet`       | Only prints the return value of each expression.  |
| `-p`, `--parse-only`  | Parses the expressions but does not interpret.    |
| `--raw`               | Outputs the "raw" form of expressions (instead of the pretty version; useful for debugging). |

Simply invoke these as desired during `kelpy.py` execution.

## Types of Objects

If I had it completely my way, everything in this project would be purely functional. However, there are some primitive types that Racket provides which Python does not. So I made some. I also made some other decisions along the way to make the Python-based implementation make a bit more sense while trying to preserve the Racket-y nature of it all.

In particular, Racket provides for a unified `number` type (which is just magical, to be honest) and what is called an `s-expression`.

### Note on the Syntax

With each usable type of object I've included the valid syntax to use the object in Kelpy. All `KExpression`s are created from a combination of literals and primitives. The literals change object to object (e.g. `{let ...` is used for the `KLet`), but there are only a few primitives (and they have pretty intuitive names, I'd say).

| Syntax    | Primitive                                             |
|-----------|-------------------------------------------------------|
| `NUMBER`  | `KNumber`                                             |
| `SYMBOL`  | `KSymbol`                                             |
| `BOOLEAN` | `KBoolean`                                            |
| `ANY`     | `KExpression`                                         |
| `...`     | Repeats previous syntactic element 0 or more times.   |

### KExpression

| Attribute | Value                                                         |
|-----------|---------------------------------------------------------------|
| `.raw`    | The raw value of whatever was put in the `KExpression`        |
| `.type`   | `kexp`                                                        |

**Syntax**: The `KExpression` cannot be created directly.

The `KExpression` is the simplest parsed object. Absolutely anything can be a `KExpression`; it simply takes a single raw parameter and stores that within itself.

### KPrimitive

The `KPrimitive` is an inherited type for the primitive types. It has no implementation on its own and cannot even be created!

**Syntax**: The `KExpression` cannot be created directly.

#### KSymbol

| Attribute | Value                                                         |
|-----------|---------------------------------------------------------------|
| `.raw`    | The raw value of whatever was put in the `KSymbol`            |
| `.type`   | `symbol`                                                      |

**Syntax**: `'symbol-name`, `'x`, etc.

A `KSymbol` can be thought of as a variable name in many cases. A `KSymbol` must start with a single quote (`'`) to denote its status as a deliberate symbol.

#### KBoolean

| Attribute | Value                                                         |
|-----------|---------------------------------------------------------------|
| `.raw`    | The raw value of whatever was put in the `KBoolean`           |
| `.type`   | `boolean`                                                     |

**Syntax**: `#t`, `true`, `#f`, `false`, etc.

A `KBoolean` is a simple boolean value implementation. There are a few ways to create one:

| Value   | Input                                                           |
|---------|-----------------------------------------------------------------|
| `true`  | `true`, `#t`, any `KExpression` that evaluates to a non-zero value. |
| `false` | `false`, `#f`, any `KExpression` that evalutaes to a zero value. |

#### KNumber

| Attribute | Value                                                         |
|-----------|---------------------------------------------------------------|
| `.raw`    | The raw value of whatever was put in the `KNumber`            |
| `.type`   | `number`                                                      |

**Syntax**: `1`, `0`, `-38`, `3.28`, `-.389`, etc.

`KNumber`s contain numeric values. They can be written in the KL any way a number can be written regularly, e.g.:

* `42` – an integer
* `3.89` – a fractional value
* `.789` – yes, it even accepts fractional values without a leading 0
* `-0.382` - negative values

(There is no support for complex numbers yet.)

The `KNumber` is necessary to evaluate the value of expressions. For example, the KL expression `{+ 1 3}` uses both `1` and `3` as `KNumber`s and will pass them to the interpreter as such.

`KNumbers` have most of the Python magic double-underscore arithmetic operators implemented, meaning `KNumber(1) + KNumber(4)` will yield a single `KNumber(5)`.

### KFunctionExpression

| Attribute | Value                                                         |
|-----------|---------------------------------------------------------------|
| `.raw`    | The raw value of whatever was put in the `KFunctionExpression`|
| `.type`   | `KF{Function}`, where `Function` is the name of the function. |
| `.function` | The specific function given.                                |
| `.args`   | A tuple of the arguments given to the function.               |

**Syntax**: The `KFunctionExpression` cannot be created directly. It is brought about by other functions.

A `KFunctionExpression` is the representation of a function in KL. There are only a few acceptable `KFunctionExpression` values; if you don't use one of those, you will get a parse error. These are gone over elsewhere.

### KList

| Attribute | Value                                                         |
|-----------|---------------------------------------------------------------|
| `.raw`    | The raw value of whatever was put in the `KList`              |
| `.type`   | `list`                                                        |
| `.kexps`  | The list of `KExpression`s stored within.                     |

**Syntax**: `{list ANY ...}`

A list of `KExpressions`.

#### Empty Lists

You can also create empty lists.

**Syntax**: `{list}`, `empty`

### KIf

| Attribute | Value                                                         |
|-----------|---------------------------------------------------------------|
| `.raw`    | The raw value of whatever was put in the `KIf`                |
| `.type`   | `KIf`                                                         |
| `.test`   | The `KExpression` to test for truthiness.                     |
| `.true`   | If `.test` is true, return this `KExpression`.                |
| `.false`  | If `.test` is false, return this `KExpression`.               |

**Syntax**: `{if ANY ANY ANY}`

To branch execution based on truthiness, use the `KIf`. The first `ANY` is the test expression. The second is the returned `KExpression` if the test is true, and the third is the equivalent for if the expression is false.

### KLet

| Attribute | Value                                                         |
|-----------|---------------------------------------------------------------|
| `.raw`    | The raw value of whatever was put in the `KIf`                |
| `.type`   | `KLet`                                                        |
| `.name`   | The "name" of the let expression (a symbol).                  |
| `.value`  | The associated `KExpression` in the let expression.           |
| `.body`   | The interior of the let, executed with a modified environment.|

**Syntax**: `{if ANY ANY ANY}`

## The Future

I have plenty of plans for improving this project over time. Here are some of the big ideas.

* Add a tutorial
    - I'm sure this won't be intuitive to someone who hasn't taken the U's CS 5510 class, so a brief tutorial on how to use the language would be good.
* Auto-indent interpreter (similar to the DrRacket interpreter)
* More documentation
    - Any good, lasting project has documentation, right? I'll work on it.

### Language Enhancements

Of course, I also want to increase the capabilities of the Kelpy language itself!

* Variables (symbols exist but do nothing; requires an environment)
* `let` capability (requires an environment)
* Closures and lambda functions
* Classes
* Custom methods ("`define`" syntax)
