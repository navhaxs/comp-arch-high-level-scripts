inc length
inc high
inc high
inc low
inc low
inc low
rcall @loop
jmp @end

loop:
push length
push high
push low
inc length
inc length
inc length
inc length
pop low
pop high
pop length
ret
end:
