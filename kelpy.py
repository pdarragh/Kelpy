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

def get_input():
    """
    :return: input from the user
    """
    inputted = raw_input('>>> ')

if __name__ == '__main__':
    print_welcome()
    while(True):
        try:
            get_input()
        except KeyboardInterrupt:
            break
        except EOFError:
            break
