inc length
inc length
inc length
inc length
inc length
inc length
inc length
inc length
inc length
inc length
inc length
inc length
nop
nop

// set up bitonic sort param
ldi low_param,  0
ldi high_param, 7// N-1 elements
ldi dir_param,  1

// copy paramters to local variables
add low, low_param, r0
add high, high_param, r0
add dir, dir_param, r0

sub length, high, low


inc length
