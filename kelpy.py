#!/usr/bin/env python

import argparse
import atexit
import sys

import kelpy

def print_welcome():
    """
    Prints the welcome information to the screen.
    """
    print(
        "Welcome to Kelpy, the Python Kelp interpreter!\n"
        "Current Version: {version}\n"
        ).format(
            version=kelpy.__version__
            )

@atexit.register
def goodbye():
    print("\nThank you for using Kelpy!")

def get_input(show_raw=False):
    """
    :return: input from the user
    """
    inputted = raw_input('>>> ')
    parsed = kelpy.parse(inputted)
    if show_raw:
        output = repr(parsed)
    else:
        output = str(parsed)
    print(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', action='store_true')
    args = parser.parse_args()
    print_welcome()
    while(True):
        try:
            get_input(args.raw)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except kelpy.ParseException as e:
            print(e.message)
