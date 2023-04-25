#!/usr/bin/python

"""
Outputs a random permutation of its input lines. Each output permutation is equally likely.

Python implementation of GNU shuf command.
"""

import random, sys, string, argparse

def main():
    parser = argparse.ArgumentParser(description="Write a random permutation of the input lines to standard output.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("file", nargs='?', default="-", metavar="FILE", help="with no FILE, or when FILE is -, read standard input.")
    group.add_argument("-e", "--echo", nargs='*', metavar="ARG", help="treat each ARG as an input line")
    group.add_argument("-i", "--input-range", nargs=1, metavar="LO-HI", help="treat each number LO through HI as in input line")
    parser.add_argument("-n", "--head-count", nargs=1, type=int, metavar="COUNT", help="output at most COUNT lines")
    parser.add_argument("-r", "--repeat", action="store_true", help="output lines can be repeated")
    args = parser.parse_args()

    # global variables
    input = None
    neednewlines = False
    opmode = 0
    
    # determining operational mode
    if args.echo:
        opmode = 1
    elif args.input_range:
        opmode = 2
        if len(args.input_range) > 1:
            print("shuf.py: extra operand")
            return(1)
    else:
        opmode = 0
    
    # default mode 0: read in file or standard input
    if opmode == 0:
        if args.file == "-":
            input = sys.stdin.readlines()
        else:
            with open(args.file, "r") as inputfile:
                input = inputfile.readlines()
        random.shuffle(input)

    # echo mode 1: read in from command line
    if opmode == 1:
        input = args.echo
        random.shuffle(input)
        neednewlines = True

    # input-range mode 2: create input from given range
    if opmode == 2:
        nums = args.input_range[0].split('-')
        if len(nums) != 2 or nums[0]=="" or nums[1]=="":
            print("shuf.py: invalid input range: " + args.input_range[0])
            return(1)
        lo = int(nums[0])
        hi = int(nums[1])
        if lo > hi:
            print("shuf.py: invalid input range: " + args.input_range[0])
            return(1)
        input = [str(i) for i in range(lo, hi+1)]
        random.shuffle(input)
        neednewlines = True

    # determining additional behavior
    # repeat
    if args.repeat:
        if args.head_count:
            count = args.head_count[0]
            r_input = []
            for i in range(0, count):
                r_input.append(random.choice(input))
            input = r_input
        else:
            i = 999
            while i > 0:
                output = random.choice(input)
                if neednewlines:
                    output += "\n"
                sys.stdout.write(output)

    # head-count
    if args.head_count:
        if len(args.head_count) > 1:
            print("shuf.py: extra operand")
            return(1)
        count = args.head_count[0]
        if not isinstance(count, int) or count < 0:
            print("shuf.py: invalid line count: " + str(count))
            return(1)
        input = input[:count]

    # formatting results and displaying them
    output = ""
    for i in input:
        output += i
        if neednewlines:
            output += "\n"
    sys.stdout.write(output)

    
if __name__ == "__main__":
    main()
