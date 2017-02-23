What do these programs do?
----

These scripts are super rough, since the purpose of writing them was to test some VHDL logic (which was the main coursework).

`simulator.py` - a simulator for our custom processor. The idea was to compare the result of the simulation here against the simulation of the VHDL logic to test correctness.

`asm2hex.py` - encodes a text file of assembly code to machine code (aka. the hex file). For example, you can see that `program.hex` is the result of running `program.asm` through this script.

Definition files
----

For this course, we designed and implemented a MIPS-like architecture in VHDL.
The scripts use some text files which define features of our architecure:

`regfile.txt` - friendly names for register file

`table.txt` - defines the instruction set encoding

Misc stuff
----

The `*_mem_gen.py` scripts generate random data for use by the VHDL simulation. e.g. `data.txt` and `tags.txt`

