# Write up of the project

I used pygame for this as at the time it was the best fit for me.

Opening a window and getting familiar to the general structure and syntax of it was now the time to start.

First step was to figure out how to draw the board, after some researching I found a writeup by *Keno Leon*: https://medium.com/better-programming/making-grids-in-python-7cf62c95f413.

## Day 1: Drawing the board
I managed to draw the board after 5 hours of trial and error thanks to the write up above.
Now step 2 is to figure out how to alternate colors from black to white for each cell and to actually link each cell to something I can change and work with.
The solution: Matrices.

Using `numpy` I made a matrice with alternating `1` and `0` and used a `for` loop that checks for `1` and colors it black, same for `0`

After finishing the board, I tweaked and polished the code and called it a rest.

![board](/writeup/image.png)

## Day2: The pieces

After getting the board done now it's time for the pieces, I wrote a function that draws a circle in the middle of the square and got the dimensions of said center from the function that draws the board.

Then I had to think of a way to know which would be colored white and which would be black. So, based on the same idea of the board I made a matrice that places `'w'` for white and `'b'` for black, worked great! 
![pieces](image-1.png)
Here I found myself in front of a problem. That being in the future when I implement movement and turns, each time a piece gets moved the whole board would be drawn again which could get laggy.
To remediate that I had to separate the functions `drawBoard()` from `placePieces()` and for that I made some variables global constants so any functions could use em which got the job done!