#!/usr/bin/python3

# Assume low_param is regfile 11,
#        high_param is regfile 7


import sys

DATA_SIZE = 256

regfile = [0] * 16
data_mem = [0] * DATA_SIZE
insn_mem = [0] * 256


def hex2int(p):
    p = int(str(p), 16)
    return p


def int2hex(p):
    p = hex(int(p))[2:]
    return p


# load in mem from tags.txt
i = 0
with open("program.hex","r") as in_file:
    for line in in_file:
        if '\n' == line[-1]:
            insn_mem[i] = line[:-1]
            i += 1

i = 0
with open("tags.txt","r") as in_file:
    for line in in_file:
        if '\n' == line[-1]:
            data_mem[i] = line[:-1]
            i += 1

print(data_mem)

sp = 255
pc = 0
tick = 0
max_stack = sp
while 0 <= pc < 256:
    sys.stdout.write("\ntick: " + str(tick).ljust(4) + " pc: " + str(pc).ljust(4) + " sp: " + str(sp).ljust(4) + " >> ")

    regfile[0] = "0"
    regfile[1] = "1"

    pc_mux_override = False

    insn = insn_mem[pc]
    if str(insn) == "0":
        sys.stdout.write("CPU Halted")
        break

    # decode
    opcode = str(insn)[0]

    if opcode == "0":
        sys.stdout.write("nop")

    elif (opcode == "1") or (opcode == "2"):

        offset_reg = hex2int(insn[1])
        offset_val = hex2int(regfile[offset_reg])

        rt_reg = hex2int(insn[2])
        memory_base_addr = 0
        # memory_base_addr = hex2int(insn[3])

        if opcode == "1":
            # ld
            regfile[rt_reg] = data_mem[memory_base_addr + offset_val]
            sys.stdout.write("ld $r" + str(rt_reg) + " <= mem(" + str(memory_base_addr + offset_val) + ")")
        else:
            # st
            data_mem[memory_base_addr + offset_val] = regfile[rt_reg]
            sys.stdout.write("st mem(" + str(memory_base_addr + offset_val) + ") <= $r" + str(rt_reg))

    elif (opcode == "3") or (opcode == "4"):
        rd_reg = hex2int(insn[3])
        rt_reg = hex2int(insn[2])
        rs_reg = hex2int(insn[1])

        rt_reg_val = hex2int(regfile[rt_reg])
        rs_reg_val = hex2int(regfile[rs_reg])

        if opcode == "3":
            # add
            regfile[rd_reg] = int2hex(rs_reg_val + rt_reg_val)
            #sys.stdout.write('$r{0} <= $r{1} + $r{2}'.format(rd_reg, rs_reg, rt_reg))
            sys.stdout.write('add {0} <= {1} + {2}'.format(rs_reg_val + rt_reg_val, rs_reg_val, rt_reg_val))
        else:
            # sub
            regfile[rd_reg] = int2hex(rs_reg_val - rt_reg_val)
            #sys.stdout.write('$r{0} <= $r{1} - $r{2}'.format(rd_reg, rs_reg, rt_reg))
            sys.stdout.write('sub {0} <= {1} - {2}'.format(rs_reg_val - rt_reg_val, rs_reg_val, rt_reg_val))

    elif opcode == "5":
        pc_mux_override = True
        pc = hex2int(insn[2:4])

        if pc == 0:
            exit()
        sys.stdout.write("Jumping to @" + str(pc))

    elif (opcode == "6") or (opcode == "7"):
        rs_reg = hex2int(insn[1])
        rt_reg = hex2int(insn[2])
        offset_val = hex2int(insn[3])

        rs_reg_val = hex2int(regfile[rs_reg])
        rt_reg_val = hex2int(regfile[rt_reg])

        result = (rs_reg_val == rt_reg_val)

        #bne, beq
        sys.stdout.write("{0} <= {1} eq {2}; ".format(result, rs_reg_val, rt_reg_val))

        if opcode == "6":
            if result:
                pc = pc + offset_val + 1  # will skip ahead by 1 extra
                pc_mux_override = True
                sys.stdout.write("beq, jumping to {0}".format(pc))
            else:
                sys.stdout.write("beq, not jumping")
        elif opcode == "7":
            if not result:
                pc = pc + offset_val + 1  # will skip ahead by 1 extra
                pc_mux_override = True
                sys.stdout.write("bne, jumping to {0}".format(pc))
            else:
                sys.stdout.write("bne, not jumping")

    elif opcode == "8":
        # rshift
        rd_reg = hex2int(insn[3])
        rs_reg = hex2int(insn[3])
        rs_reg_val = hex2int(regfile[rd_reg])

        regfile[rd_reg] = int2hex(int(rs_reg_val / 2))

        sys.stdout.write("{0} <= {1}/2".format(int(rs_reg_val / 2), rs_reg_val))

    elif opcode == "9":
        sys.stdout.write("Stack not implemented")

    elif opcode == "A":
        # ldi
        rd_reg = hex2int(insn[3])
        immediate_hex = insn[1:3]

        regfile[rd_reg] = immediate_hex

        sys.stdout.write("ldi $r" + str(rd_reg) + " <= 0x" + immediate_hex + " (val: " + str(hex2int(immediate_hex)) + ")")

    elif opcode == "B":
        rd_reg = hex2int(insn[3])
        rt_reg = hex2int(insn[2])
        rs_reg = hex2int(insn[1])

        rs_reg_val = hex2int(regfile[rs_reg])
        rt_reg_val = hex2int(regfile[rt_reg])

        if rt_reg_val < rs_reg_val:
            regfile[rd_reg] = "1"

            sys.stdout.write("{0} < {1} is True. $r{2} <= 1".format(rt_reg_val,rs_reg_val, rd_reg))
        else:
            regfile[rd_reg] = "0"

            sys.stdout.write("{0} < {1} is False. $r{2} <= 0".format(rt_reg_val, rs_reg_val, rd_reg))

    elif opcode == "C":
        # pop
        rt_reg = hex2int(insn[2])

        regfile[rt_reg] = data_mem[sp]
        sys.stdout.write("Popped " + str(data_mem[sp]))
        sp += 1

    elif opcode == "D":
        # push
        rt_reg = hex2int(insn[2])

        sp -= 1 # create room in stack
        data_mem[sp] = regfile[rt_reg]

        sys.stdout.write("Pushed " +  str(regfile[rt_reg]))

        # stats
        if sp < max_stack:
            max_stack = sp

    elif opcode == "E":
        # rcall


        sp -= 1
        data_mem[sp] = int2hex(pc + 1) # TODO Save PC of the next instruction to ret to
        #print("Saved current PC+1: " + str(pc + 1))

        pc_mux_override = True
        pc = hex2int(insn[2:4])
        sys.stdout.write("rcall to @" + str(pc) + " [low_param:" + str(hex2int(regfile[11])) + " high_param:" + str(hex2int(regfile[7])) + "]")

        # stats
        if sp < max_stack:
            max_stack = sp

    elif opcode == "F":
        # ret


        pc_mux_override = True
        pc = hex2int(data_mem[sp])

        print("sp is currently: " + str(data_mem[sp]))

        sp += 1

        sys.stdout.write("ret to @" + str(pc))

    else:
        sys.stdout.write("Unrecognised")

    if not pc_mux_override:
        pc += 1

    if sp < 0:
        print("\n\nABORT: sp invalid (tried to set as negative)")
        exit()

    tick += 1

    if pc == 4:
        print("\n\nAssuming PC@4 is the end of the program.\nCPU halted.\nThe stack reached a max size of: " + str(max_stack) + " (" + str(DATA_SIZE - max_stack) + ")\nLook at all the sorted tags below!")
        print(data_mem)
        exit()

sys.stdout.write("\n")
print(data_mem)
