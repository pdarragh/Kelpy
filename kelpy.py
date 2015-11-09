#!/usr/bin/env python

import argparse
import atexit
import readline # This is used to fix the `raw_input` call.
import sys

import kelpy

def print_welcome():
    """
    Prints the welcome information to the screen.
    """
    print(
        "Kelpy {version}\n"
        "Written by Pierce Darragh, (c) 2015\n"
        "Welcome to Kelpy, the Python Kelpy interpreter!\n"
    ).format(version=kelpy.__version__)

@atexit.register
def goodbye():
    print("\nThank you for using Kelpy!")

def get_parsed_input(user_input, show_raw=False, suppress_output=False):
    """
    :return: input from the user
    """
    kexp = kelpy.parse(user_input)
    if show_raw:
        output = repr(kexp)
    else:
        output = str(kexp)
    if not suppress_output:
        print("~ {}".format(output))
    return kexp

def kelp_help(message):
    if not message:
        kelpy.helpdocs.general_help()
    else:
        kelpy.helpdocs.specific_help(message)

def exit():
    raise KeyboardInterrupt

def builtin_delegate(text):
    command = text.split()[0]
    message = ' '.join(text.split()[1:])
    if command == 'exit' or command == 'quit':
        exit()
    elif command == 'help':
        kelp_help(message)

BUILTINS = {
    'help': kelp_help,
    'exit': exit,
    'quit': exit,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-p', '--parse-only', action='store_true')
    args = parser.parse_args()
    print_welcome()
    while(True):
        try:
            user_input = raw_input('>>> ')
            if not user_input:
                continue
            if user_input.split()[0].lower() in BUILTINS:
                builtin_delegate(user_input.lower())
                continue
            kexp = get_parsed_input(user_input, args.raw, args.quiet)
            if not args.parse_only:
                result = kelpy.interpret(kexp, kelpy.types.empty_env)
                print(result)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except kelpy.KelpyException as e:
            print(e.message)
