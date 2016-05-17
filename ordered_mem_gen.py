#!/bin/python3

import os
import binascii

# parameters
MACHINE_BITNESS_MULTIPLIER = 2  # this is multiplied by 8
MEMORY_SIZE = 256
DATA_TAG_SIZE = 8 # N

MAX_DIGITS = 1 + len(str(MEMORY_SIZE))

# file format
OUTPUTS = ["tags.txt", "data.txt"]
WORDS_PER_LINE = 1 #8

for f in OUTPUTS:

    data = []
    m = 0
    for block in range(MEMORY_SIZE):       
        data.append(hex(DATA_TAG_SIZE - m)[2:].zfill(4))
        
        m += 1

    with open(f, "wt") as out_file:

        for i in range(DATA_TAG_SIZE):
            out_file.write(str(data[i]).upper())

            if i % WORDS_PER_LINE == WORDS_PER_LINE - 1:
                out_file.write("\n")

        # fill the rest of the memory with zeros
        for i in range(DATA_TAG_SIZE, MEMORY_SIZE):
            out_file.write("0"*2*MACHINE_BITNESS_MULTIPLIER)

            if (i % WORDS_PER_LINE == WORDS_PER_LINE - 1) and (i != MEMORY_SIZE - 1):
                out_file.write("\n")

    print("Wrote " + f + " with " + str(DATA_TAG_SIZE) + " random values from 0-" + str(DATA_TAG_SIZE-1))
