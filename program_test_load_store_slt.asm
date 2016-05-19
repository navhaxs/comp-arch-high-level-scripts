start:
	ldi tag_i, 0                      // 0x0A00 2560
	ldi tag_idist,  7                 // 0x0004 4
	
	ld tag_i, i, 0
	ld tag_idist, cmp, 1
	
	slt tmp, tag_i, tag_idist         // is tag_i (2560) > tag_idist (4) == true. should set tmp to '1'
	slt length, tag_idist, tag_i      // false, should set length to '0'
	
	st tag_i, cmp, 1
	st tag_idist, i, 0