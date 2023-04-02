#!/usr/bin/env python3
"""
Clean up some files.

Usage:
    sortof [options] PATH DESTINATION

Options:
    -h, --help      Display this message.
    --version       Show version information.
"""

from docopt import docopt
from pathlib import Path
from collections import namedtuple
from colorama import init, Fore, Style

import subprocess

VERSION="1.0"

def input_until_valid(
    prompt,
    message,
    check=lambda x: x != '',
    default=None,
    default_prompt="{prompt} [{default}]: "
):
    if default:
        prompt = default_prompt.format(
            prompt=prompt.strip(': '),
            default=default,
        )

    while True:
        s = input(prompt)

        if s == '' and default:
            s = default

        if check(s):
            return s

        print(message)


Choice = namedtuple('Choice', ['name', 'description'], defaults=[''])

def ask_for_choices(choices, case_sensitive=True):
    prompt = "[{},?] ".format(
        ",".join([choice.name.capitalize() for choice in choices])
    )

    def print_description():
        description = "{}".format(
            "\n".join([
                " ?- {}{}".format(
                    choice.name.capitalize(),
                    f": {choice.description}" if choice.description else ""
                )
                for choice in choices
            ])
        )

        print(description)

    if case_sensitive:
        match = lambda x, y: x == y
    else:
        match = lambda x, y: x.lower() == y.lower()

    while True:
        s = input(prompt)

        if s == '?':
            print_description()
            continue

        for choice in choices:
            if match(s, choice.name[0]):
                return choice.name



def clean_loop(path, destination):
    p = Path(path)

    dest = Path(destination)

    move_choices = [
        Choice("!", "Abort the operation")
    ]

    for subdest in dest.iterdir():
        if not subdest.is_dir():
            continue
        
        move_choices.append(
            Choice(subdest.name)
        )


    for subpath in p.iterdir():
        foreground_color = Fore.LIGHTBLUE_EX if subpath.is_dir() else Fore.GREEN

        print(foreground_color + str(subpath.name) + Style.RESET_ALL)

        while True:
            response = ask_for_choices([
                Choice("skip", "Go to the next item"),
                Choice("move", "Move to other directory"),
                Choice("open", "Open the file"),
                Choice("create", "Create a directory and then move"),
            ])

            if response == "skip":
                break
            
            if response == "move":
                directory = ask_for_choices(move_choices)

                if directory == '!':
                    continue

                subpath.rename(dest/directory/subpath.name)
                break
            
            if response == "open":
                subprocess.Popen(["open", subpath], start_new_session=True)
            
            if response == "create":
                directory = input_until_valid("mkdir:", "Input new directory name")

                new_dir = dest/directory
                new_dir.mkdir(exist_ok=True)
                subpath.rename(new_dir/subpath.name)

                move_choices.append(
                    Choice(new_dir.name)
                )

                break


def main():
    init()

    arguments = docopt(__doc__, version=VERSION)

    clean_loop(arguments['PATH'], arguments['DESTINATION'])


if __name__ == "__main__":
    main()