import meta
import primitives
# import concepts
# import forms

from ..__init__ import __version__ as version

ABOUT = (
    "ABOUT\n"
    "Kelpy is a functional, Polish prefix-operated language. It can recognize various\n"
    "types of input, and is still under development to add more features!\n"
)

TOPICS_LIST = {
    'getting started'   : (0, meta.getting_started),
    'numbers'           : (1, "primitives.numbers"),
    'symbols'           : (1, "primitives.symbols"),
    'booleans'          : (1, "primitives.booleans"),
    'lists'             : (1, "primitives.lists"),
    'functions'         : (2, "concepts.functions"),
    'math'              : (2, "concepts.math"),
    'comparison'        : (2, "concepts.comparison"),
    'if'                : (3, "forms.if_form"),
    'let'               : (3, "forms.let"),
}

TOPICS = (
    "TOPICS\n"
    "Simply input 'help TOPIC' with any of the following topics to learn more!\n"
    "{topics}"
).format(
    topics = '\n'.join(
        ['  * {}'.format(topic) for topic in 
            # This sorts the topics list by the first value in the tuple.
            sorted(TOPICS_LIST, key=lambda topic: TOPICS_LIST[topic][0])
        ]
    )
)

def general_help():
    print(
        "Kelpy {version} Help Documentation\n"
        "\n"
        "{about}"
        "\n"
        "{topics}"
        "\n"
    ).format(
        version = version,
        about   = ABOUT,
        topics  = TOPICS
    )

def specific_help(topic):
    if not topic in TOPICS_LIST:
        print("Invalid topic selected.")
        return
    print(TOPICS_LIST[topic][1] + '\n')
