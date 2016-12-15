SPEC!
---
`bfgame` is a brainfuck game engine (yes, seriously). This is its spec.

# Memory (a.k.a. "tape")
bfgame's memory space consists of a 'tape' with infinite cells, and a pointer, which you can move with the `<` and `>` operators.

In bfgame, each cell can hold an arbitrarily large integer.

The first five cells are reserved for the FFI.

# Instructions
bfgame has 8 instructions. The print(`.`) and input(`,`) operators have different functionalities than those in brainfuck:

	. Run the currently selected function
	, Get the next event from the event queue. If there are no events, this will be return 0.
	+ Increment the current cell's value by 1
	- Decrease the current cell's value by 1
	> Move pointer to next cell
	< Move pointer to previous cell (won't do anything if in cell #0)
	[ Jump past the matching ] if the cell under the pointer is 0 
	] Jump back to the matching [ if the cell under the pointer is nonzero

Any other characters will be ignored by the interpreter, acting like comments.

# FFI
To call external functions, you'll use the first 5 'tape' cells. Here's what 
each of them is used for:

	0: Module ID - When you select a module, its functions become available
	1: Function ID to call
	2: Pointer to beginning of args - This should point to a cell which will be the first one in the functions arguments list. If there are no args, this should be 0.
	3: Pointer to ending of args - If there are no args, this should be 0. If there is only one arg, it should be the same as #2.
	4: Returned value - If a function returns a value, it'll go here.

Now, let's say we want to print the string "A" (ASCII codes 65). The function for this is function 1, and it's in the IO module (ID 1). It takes a list of any length and prints it, returning 0.

	Example: Printing "A"

	+     Load the IO module
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

