// Memory shuffler
// Implements bitonic sort algorithm
//
// program.asm
//
// dir_param: UP = 1
//	      DOWN = 0

start:
	// set up bitonic sort param
	ldi low_param,  0
	ldi high_param, 15 // N-1 elements
	ldi dir_param,  1
	// do call
	rcall @bitonicSort

end:
	jmp @end

bitonicSort:

	push high
	push low
	push dir
	push midpoint

	// copy paramters to local variables
	add low, low_param, r0
	add high, high_param, r0
	add dir, dir_param, r0

	// calculate length
	sub length, high, low
	inc length

	// Condition: length <= 1
	// Condition true: set cmp to '1'
	// Condition false: set to '0'
	sub length, length, r1
	slt cmp, r1, length

	// if condition is true, goto ret
	beq cmp, r1, @bitonicSort_end

	// else,

  	// calculate midpoint
	add midpoint, low, high
	rshift midpoint
	inc midpoint

	// call
	//         bitonicSort(UP, low, midpoint-1);
	add low_param, low, r0
	sub high_param, midpoint, r1
	add dir_param, r1, r0
	rcall @bitonicSort

	// call
	//        bitonicSort(DOWN, midpoint, high);
	add low_param, midpoint, r0
	add high_param, high, r0
	add dir_param, r0, r0
	rcall @bitonicSort

	// call
	//        bitonicMerge(direction, low, high);
	add low_param, low, r0
	add high_param, high, r0
	add dir_param, dir, r0
	rcall @bitonicMerge

bitonicSort_end:
	pop midpoint
	pop dir
	pop low
	pop high
	ret


bitonicMerge:
	push high
	push low
	push dir
	push midpoint

	// load function param --> local
	add low, low_param, r0
	add high, high_param, r0
	add dir, dir_param, r0

	// calculate length
	sub length, high, low
	inc length

	// calculate midpoint
	add midpoint, low, high
	rshift midpoint
	inc midpoint

	beq length, r1, @bitonicMerge_end

	// call
	//         bitonicCompare(direction, low, high);
	add low_param, low, r0
	add high_param, high, r0
	add dir_param, dir, r0
	rcall @bitonicCompare

	// call
	//        bitonicMerge(direction, low, midpoint-1);
	add low_param, low, r0
	sub high_param, midpoint, r1
	add dir_param, dir, r0
	rcall @bitonicMerge

	// call
	//        bitonicMerge(direction, midpoint, high);
	add low_param, midpoint, r0
	add high_param, high, r0
	add dir_param, dir, r0
	rcall @bitonicMerge

bitonicMerge_end:
	pop midpoint
	pop dir
	pop low
	pop high
	ret

bitonicCompare:
	push high
	push low
	push dir

	// load param --> local
	add low, low_param, r0
	add high, high_param, r0
	add dir, dir_param, r0

	// calculate length
	sub length, high, low
	inc length

	// calculate distance
	add dist, length, r0
	rshift dist

	// BEGIN LOOP

	// initialise i <= 'low'
	add i, low, r0
	
bitonicCompare_loop:

	// load mem[i] to $tag_i
	ld tag_i, i, 1
	
	// load mem[i+dist] to $tag_idist
	// where $cmp = i+dist
	// $cmp is some unused register
	add cmp, i, dist
	ld tag_idist, cmp, 0
	
	// Condition: tag[i+dist] < tag[i]
	// Condition true: '1'
	// Condition false: '0'
	slt cmp, tag_i, tag_idist
	
	// if (condition != direction), continue loop
	bne cmp, dir, @bitonicCompare_loop_end

	// else, do swap:

	// where $cmp = i+dist
	// $cmp is some unused register
	add cmp, i, dist
	st tag_i, cmp, 0 // Save $tag_i to mem[i+dist]
	st tag_idist, i, 1  // Save tag_idist to mem[i]

bitonicCompare_loop_end:

	inc i

	// Condition: i < low+dist
	// Condition true: 1 => continue loop
	// Condition false: 0 => break loop
	//
	// add tmp, low, dist
	// slt cmp, tmp, i
	// beq cmp, r1, @bitonicCompare_loop

	// We cannot jump backwards using bne/beq as above,
	// so alternative implementation:

	add tmp, low, dist
	slt cmp, tmp, i
	beq cmp, r0, @bitonicCompare_end
	jmp @bitonicCompare_loop

bitonicCompare_end:
	pop dir
	pop low
	pop high
	ret

	
	
   

  

