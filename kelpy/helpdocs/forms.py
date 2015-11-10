if_form = '''\
IF
The 'if' allows the programmer to branch the program. It has the following
syntax:
    {if EXPRESSION TRUE FALSE}
During evaluation, the EXPRESSION is evaluated. If its value can be considered
'true', then the TRUE expression is evaluated; otherwise the FALSE expression
will be evaluated. However, note that only one of the two result expressions
will ever be executed!

Example:
    {if True 1 0} -> 1
    {if {== 3 4} 1 0} -> 0
    {if {!= {* 3 4} {+ 10 2}} {- 10 9} {list 1 2 3}} -> {list 1 2 3}
'''

let = '''\
LET
Using a 'let' allows you to create a sort of shortcut for a long expression that
you may want to use multiple times within a single expression. The syntax is:
    {let {SYMBOL EXPRESSION} BODY}
Throughout the evaluation of BODY, any instance of SYMBOl will be replaced with
EXPRESSION. Neat!

Example:
    {let {'x 3} {+ x 10}} -> 13
'''
