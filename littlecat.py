#!/usr/bin/env python3
import argparse
import time
import sys
import re

indent_start_pattern = "^ (    )*$"
indent_mid_pattern = "^ (    )* {1,3}$"

repeated_letters = ".*[a-zA-Z][a-zA-Z]$"
repeated_numbers = ".*[0-9][0-9]$"

patterns = {
    'indent_start': (indent_start_pattern, 0.25),
    'indent_mid': (indent_mid_pattern, 0),
    'symbol': (".*[\>\<:;\-_=\+\(\)]$(?!\n)", 0.8),
    #'symbol': ("^.*=$", 10.8),
    'repeated_letters': (repeated_letters, 0.1),
    'repeated_numbers': (repeated_numbers, 0.1),
    #'symbol': (".*[`~!@#%&-_=\{\}\[\]\|;:]$", 1)
}

full_pattern = "|".join("(?P<%s>%s)" % (x[0], x[1][0]) for x in patterns.items())
pattern_matcher = re.compile(full_pattern,
                             re.MULTILINE)

parser = argparse.ArgumentParser(description="Slowly prints file to stdout as "\
                                             "if someone were typing it")
parser.add_argument('file_name', help="path of file to print")

args = parser.parse_args()

f = open(args.file_name)

contents = ""
while 1:
    c = f.read(1)
    if c:
        contents += c
        sys.stdout.flush()
        m = pattern_matcher.search(contents)
        delay = 0.25
        if m:
            for name, info in patterns.items():
                if m.group(name):
                    delay = info[1]
                    break
        time.sleep(delay)
        print(c, end='')
    else:
        break

f.close()
