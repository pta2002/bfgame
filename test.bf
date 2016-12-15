+     Load the IO module
>     Move forward to cell #1
+     Add 1 to its value so it's now 1
>     Move to cell #2
+++++ Add 5 to its value so it points to cell #5 which is where our string will start
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
