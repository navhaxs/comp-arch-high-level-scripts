ldi length, 0
ldi high, 4
ldi low, 8
sub low, low, high
inc high
slt high
rshift low
rcall @loop
jmp @end
loop:
push high
push low
inc length
beq length, 3, @endFunct
rcall @loop
endFunct:
pop low
pop high
ret
end:
