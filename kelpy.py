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

def get_parsed_input(show_raw=False, suppress_output=False):
    """
    :return: input from the user
    """
    user_input = raw_input('>>> ')
    kexp = kelpy.parse(user_input)
    if show_raw:
        output = repr(kexp)
    else:
        output = str(kexp)
    if not suppress_output:
        print("~ {}".format(output))
    return kexp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-p', '--parse-only', action='store_true')
    args = parser.parse_args()
    print_welcome()
    while(True):
        try:
            kexp = get_parsed_input(args.raw, args.quiet)
            if not args.parse_only:
                result = kelpy.interpret(kexp)
                print(result)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except kelpy.KelpyException as e:
            print(e.message)
