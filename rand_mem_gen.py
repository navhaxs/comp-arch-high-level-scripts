#!/bin/python3

import os
import binascii

# parameters
MACHINE_BITNESS_MULTIPLIER = 2  # this is multiplied by 8
MEMORY_SIZE = 256
DATA_TAG_SIZE = 128

MAX_DIGITS = 1 + len(str(MEMORY_SIZE))

# file format
OUTPUTS = ["tags.txt", "data.txt"]
WORDS_PER_LINE = 1 #8

for f in OUTPUTS:

    # grab enough random #
    data = []
    for block in range(MEMORY_SIZE):
        gen_rnd = binascii.b2a_hex(os.urandom(MACHINE_BITNESS_MULTIPLIER))
        rnd = gen_rnd.decode("utf-8")
        data.append(rnd)

    with open(f, "wt") as out_file:
        ## out_file.write("// format=hex addressradix=h dataradix=h version=1.0 wordsperline=" + str(WORDS_PER_LINE) + "\n")

        for i in range(DATA_TAG_SIZE):
            ##if i % WORDS_PER_LINE == 0:
            ##    line_start = "@" + str(i)
            ##    out_file.write(line_start.rjust(MAX_DIGITS))

            ##out_file.write(" " + str(data[i]).upper())
            out_file.write(str(data[i]).upper())

            if i % WORDS_PER_LINE == WORDS_PER_LINE - 1:
                out_file.write("\n")

        # fill the rest of the memory with zeros
        for i in range(DATA_TAG_SIZE, MEMORY_SIZE):
            ##if i % WORDS_PER_LINE == 0:
            ##    line_start = "@" + str(i)
            ##    out_file.write(line_start.rjust(MAX_DIGITS))

            ##out_file.write(" " + "0"*2*MACHINE_BITNESS_MULTIPLIER)
            out_file.write("0"*2*MACHINE_BITNESS_MULTIPLIER)

            if (i % WORDS_PER_LINE == WORDS_PER_LINE - 1) and (i != MEMORY_SIZE - 1):
                out_file.write("\n")

    print("Wrote " + f + " with " + str(DATA_TAG_SIZE) + " random values from 0-" + str(DATA_TAG_SIZE-1))
