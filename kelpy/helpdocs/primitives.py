numbers = '''\
NUMBERS
Kelpy has a pretty advanced idea of what a 'number' is. Unlike most languages
where there is a difference between integers (2, 3, 1929, ...) and fractional
numbers (0.83, 1929.0, -.29), Kelpy treats these all as just 'numbers'.
'''

booleans = '''\
BOOLEANS
A boolean is a True or False value. These can be used to test for equality or
some other form of comparison.

Kelpy recognizes quite a few ways of representing booleans:
    True Values:  'true', 'TRUE', '#t', any non-zero number
    False Values: 'false', 'FALSE', '#f', zero
'''

symbols = '''\
SYMBOLS
Symbols are used by Kelpy as placeholders. You can think of symbols kind of
like variables, so long as you give them a definition!

Symbols are denoted with a leading single quote mark. The following are all
examples of acceptable symbols:
    'x
    'blah
    'long-symbol-name
    '{a long symbol here}

Any time Kelpy encounters a symbol, it will attempt to look up its value in the
current environment. To learn more about how to use symbols effectively, see the
documentation on 'let'.
'''

lists = '''\
LISTS
The list is an important type in Kelpy. It allows you to group elements together
and do things with them. You can create a list in Kelpy by doing:
    {list 1 2 3 4}
    {list 'x 'y 'z}
    {list 1 'x {+ 1 2}}
These are all considered perfectly acceptable list constructions. Additionally,
there are two ways to create an empty list:
    {list}
    empty
On top of all of these neat list constructions, there are two additional ways to
create a list: exclusive and inclusive bounds expansion.
    {list 1 -> 5} == {list 1 2 3 4}
    {list 1 => 5} == {list 1 2 3 4 5}
Note that these forms can only be used with integers on either side.

Lists come with many functions. Here's a list of all the things you can do to a
list! Pretty neat.
List Operations:
    {empty? {list 1 2 3}} == False
      - determines if a list is empty
    {first {list 1 2 3}} == 1
      - returns the first element of a list
    {second {list 1 2 3}} == 2
      - returns the second element of a list
    {rest {list 1 2 3}} == {list 2 3}
      - returns the list from the second element to the end
    {reverse {list 1 2 3}} == {list 3 2 1}
      - returns a reversed copy of the list
    {prepend 0 {list 1 2 3}} == {list 0 1 2 3}
      - returns a list with the given element added to the front
    {append 4 {list 1 2 3}} == {list 1 2 3 4}
      - returns a list with the given element added to the back
'''
