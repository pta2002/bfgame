SPEC!
---
`bfgame` is a brainfuck game engine (yes, seriously). This is its spec.

# Memory (a.k.a. "tape")
bfgame's memory space consists of a 'tape' with 2^32 cells, and a pointer, which you can move with the `<` and `>` operators.

In bfgame, each cell can hold a 32-bit value.

The first five cells are reserved for the FFI.

# FFI
To call external functions, you'll use the first 5 'tape' cells. Here's what 
each of them is used for:

	0: Module ID to load - When you load a module, its functions become available
	1: Function ID to call
	2: Pointer to beginning of args - This should point to a cell which will be the first one in the functions arguments list. If there are no args, this should be 0.
	3: Pointer to ending of args - If there are no args, this should be 0. If there is only one arg, it should be the same as #2.
	4: Returned value - If a function returns a value, it'll go here.

To load a module, you would need to select cell #0, and then print it (`.`):

	Example: Loading the IO module, ID 1
	
		Cell #0 is selected by default when the program starts
	+ 	Add 1 to its value so it's now 1
	. 	Print the value to load the module
	

Now, let's say we want to print the string "A" (ASCII codes 65). The function for this is function 1, and it's in the IO module (ID 1). It takes a list of any length and prints it, returning 0.

	Example: Printing "A"

	+.    Load the IO module
	>     Move forward to cell #1
	+     Add 1 to its value so it's now 1
	>     Move to cell #2
	+++++ Add 5 to its value so it points to cell #5 which is where our string will start.
	>     Move to cell #3
	+++++ Add 5 to its value which is where our string will end
	>>> Move to cell #6 our loop counter
	++++++ Set the loop counter to 6
	[
	    <++++++++++ Go back to cell #5 and add 10
	    >-          Go back to cell #6 and subtract 1
	]
	<+++++ Go back to cell #5 and add 5 so it's 65
	<<<<. Go back to cell #1 and print it to run the function

Easy, right? :D

