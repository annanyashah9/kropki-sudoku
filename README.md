# Kropki-Sudoku

This project is an implementation of Sudoku as a constraint satisfaction problem, but the Kropki variant, which calls for the following:
1. White Dot: One cell must be exactly one greater than the other
2. Black Dot: One cell must be exactly double of the other
3. No Dot: No additional constraint

The project features consist of Backtracking, which recursively explores the 9x9 Sudoku space, in addition to Minimum Remaining Value (MRV) and degree heuristics to determine the next grid to be filled, based on the fewest legal values and the smallest number of constraints. Lastly, it implements Forward Checking, with prunes invalid values from the domain of legal values, once a value has been assigned to a cell. 

The functionality of the program consists of the following:
1. It takes in an input file, a few of which are given as part of this repo: Input1.txt, Input2.txt, Input3.txt. The first 9 rows consist of the sudoku grid, where a value of 0 represents an empty cell that needs to be filled. The next 9 rows represent the horizontal constraints between row-adjacent cells, where 0 = no dot, 1 = white dot, and 2 = black dot. The last 8 rows represent vertical constraints between column-adjacent cells, which follows the same format.
2. The program runs and generates an output file, representing the completed Sudoku grid under the given constraints. If no solution is found, the file will contain "No solution found."

The instructions to run this project are as follows:
1. When calling the main function, set the first parameter to the desired input file, and set the second parameter to the name of the desired output file (Ex. main("Input1.txt", "Output1.txt"))
2. To run the program (for MacOS), run the following command: python3 proj2_final.py

From following these instruction, an output file with the specified name in (1) will be created. This repo contains corresponding output files that were generated, from running our program on the input files. 
