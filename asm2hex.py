#!/bin/python3


import re

table = {}
asm_code = []   # asm instructions (the program)
regfile = []    # register "friendly" names
jmpref = {}     # dictionary of label-address pairs
hexout = []     # first pass of hex
vhdlout = []    # program converted to final hex, ready to be pasted into instruction_memory.vhd

with open('regfile.txt', 'r') as f:
    for l in f:
        l = l.rstrip()
        regfile.append(l)

if len(regfile) > 16:
    print("Too many registers defined in regfile!")
    exit()

print(regfile)

# load in format of each instruction
# insn, field A (opcode), field B, field C, field D, "ASM instruction format"
with open('table.txt', 'r') as f:
    for l in f:
        l = l.rstrip().split('\t')

        # insert the pair:
        #   insn - A, B, C, D
        table[l[0]] = (l[1], l[2], l[3], l[4], l[5])

# first pass of the asm file: load & note down any labels
with open('program.asm', 'r') as f:
    insn_count = 0
    for line in f:

        # skip whitespace, blank, or comment lines
        l = line.rstrip().lstrip()
        if l.startswith("//"):
            continue
        elif len(l) == 0:
            continue

        if ":" in l:
            # there is a label here, mark down this address
            label = "@" + str(l[:-1])

            jmpref[label] = insn_count


            print("Noted label \"" + label + "\" which points to address " + str(insn_count))
            continue

        # this is a proper insn, split into parts
        l = re.sub(re.compile("//.*?\Z" ) ,"" ,l) # remove all occurance singleline comments (//COMMENT\n ) from string
        insn = l.split()
        insn= [s.strip(',') for s in insn]

        print("Line: " + str(insn_count))
        if insn[0] not in table:
            print("The instruction \"" + insn[0] + "\" on line " + str(insn_count) + " is unrecognised.")
            exit()
        else:
            hex_frmt = list(table[insn[0]][1:4])

            asm_frmt = table[insn[0]][4][1:-1].split(',')
            asm_frmt = list(filter(None, asm_frmt)) # strip out empty items
            l = l.replace(',', ' ').split()[1:]

            # populate the four fields
            opcode = table[insn[0]][0]
            decoded = [opcode, hex_frmt[0], hex_frmt[1], hex_frmt[2]]

            if not len(l) == len(asm_frmt):
                print("ABORT: Problem your program.asm")

                print(len(l) )
                print(len(asm_frmt))
                print("frmt" + str(asm_frmt))
                print("input" + str(l))

                exit()

            print("\t\t0 " + insn[0] + " => " + str(opcode))

            if len(asm_frmt)>0:

                this_line_hex = ''
                for i in range(len(asm_frmt)):
                    this_line_hex += l[i]

                    if l[i] in regfile:

                        # register label -> register address in hex
                        decoded_reg = str(hex(regfile.index(l[i])))[2:].upper()

                        # get field pos (A/B/C), add one to offset for Opcode
                        indices = [y for y, x in enumerate(hex_frmt) if x == asm_frmt[i]]

                        for each in indices:
                            decoded[each+1] = decoded_reg
                            print("\t\t" + str(each+1) + " " + asm_frmt[i] + " => " + str(decoded_reg))

                    elif asm_frmt[i] == "@label_8b":

                        # get field pos (A/B/C)
                        indices = [y for y, x in enumerate(hex_frmt) if x == "@label_8b"]

                        # insert placeholder
                        for each in indices:
                            # get field pos (A/B/C), add one to offset for Opcode
                            decoded[each+1] = l[i]
                            print("\t\t" + str(each+1) + " " + asm_frmt[i] + " => " + l[i])

                    elif asm_frmt[i] == "@offset_4b":

                        # get field pos (A/B/C)
                        indices = [i for i, x in enumerate(hex_frmt) if x == "@offset_4b"]

                        # insert placeholder
                        for each in indices:
                            # get field pos (A/B/C), add one to offset for Opcode
                            decoded[each + 1] = "@" + l[i]  # Double @@ denotes offset, not full address
                            print("\t\t" + str(each + 1) + " " + asm_frmt[i] + " => @" + l[i])

                    elif asm_frmt[i] == "memaddr_4b":

                        # get field pos (A/B/C), add one to offset for Opcode
                        index = hex_frmt.index("memaddr_4b") + 1

                        decoded[index] = l[i]

                        print("\t\t" + str(index) + " " + asm_frmt[i] + " => " + l[i])

                    elif asm_frmt[i] == "memaddr_8b":

                        # convert int -> hex
                        two_char = str(hex(int(l[i])))[2:].zfill(2)

                        # get field pos (A/B/C)
                        indices = [y for y, x in enumerate(hex_frmt) if x == "memaddr_8b"]

                        j = 0
                        # insert placeholder
                        for each in indices:
                            decoded[each+1] = two_char[j]
                            print("\t\t" + str(each + 1) + " memaddr_8b => " + two_char[j])
                            j += 1

                    else:
                        print("ABORT: Problem with the ASM format. Definition not found in table.txt/regfile.txt for: " + asm_frmt[i])
                        exit()


                #get the parts of this_line
                #print(''.join(this_line) + " --> " + ''.join(asm_frmt))
                #match them to asm_frmt

            hexout.append(decoded)
            print("\t" + str(hexout[insn_count]))

        insn_count += 1

# second pass: replace labels by addresses
print("\nstat: " + str(insn_count) + " total lines, range from 0x00 to " + str(hex(insn_count-1)))

i = 0
for each_line in hexout:
    this_line = ""
    address_to_insert = ""

    for char in each_line:
        if str(char).startswith("@@"):
            char = char[1:]
            if char in jmpref:
                dest_to_jump_int = str(jmpref[char])
                dest_to_jump_offset_int = int(dest_to_jump_int) - int(i) - 1
                # Minus one because "WILL JUMP ONE EXTRA AHEAD."

                # calculate the 16-bit offset
                # what if we need to go backwards??
                address_to_insert = str(hex(int(dest_to_jump_offset_int )))[2:].upper() #.zfill(2)

                this_line += address_to_insert[0]

        elif str(char).startswith("@"):

            if char in jmpref:
                if len(address_to_insert) == 0:
                    address_to_insert_int = str(jmpref[char])
                    address_to_insert = str(hex(int(address_to_insert_int)))[2:].upper().zfill(2)

                this_line += address_to_insert[0]
                address_to_insert = address_to_insert[1:]

        else:
            this_line += str(char)

    vhdlout.append((this_line))
    print(this_line)

    i += 1

print("\nFinal output:")

i = 0
for each in vhdlout:
    print("var_insn_mem(" + str(i) + "):= X\"" + each + "\";")
    i += 1


f = open("program.hex", "w")
print("\n".join(str(i) for i in vhdlout), end="\n", file=f)
f.close()

print("\nWrote hex to program.hex")
