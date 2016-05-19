start:
	ldi tag_i, 0                      // 0x0A00 2560
	ldi tag_idist,  7                 // 0x0004 4
	
	ld tag_i, i, 0
	ld tag_idist, cmp, 1
	
	slt tmp, tag_i, tag_idist         // should set tmp to '1'
	slt length, tag_idist, tag_i      // false, should set length to '0'
	
	st tag_i, cmp, 1
	st tag_idist, i, 0
	
	ldi i, 0
	inc i
	inc i
	inc i
	inc i
	inc i
	inc i
	inc i					// i is 7
	
	inc dir					// dir is 2
	inc dir
	
	add dir_param, dir, i	// 9
    sub high, dir, i		// 2 - 7 = -5
    sub high_param, i, dir  // 7 - 2 = 5
	
	rcall @foo
	
end:
	jmp @end
	
foo:
	ldi i, 0
	inc i
	inc i
	inc i
	inc i
	inc i
	inc i
	inc i					// i is 7
	
	rcall @bar
	
	inc midpoint
	inc midpoint
	inc midpoint
	inc midpoint
	inc midpoint
	inc midpoint
	
	ret
	
bar:
	inc length
	inc length
	inc length
	inc length
	inc length
	rcall @dummy

	inc low_param
	inc low_param
	inc low_param
	inc low_param
	inc low_param


	ret
	
dummy:
	inc low
	inc low
	inc low
	inc low
	inc low

	ret