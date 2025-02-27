import sys
"""
AI Project 2: Kropki Sudoku
Ananya Shah
Sayuri Hadge
"""

# maps row/col index to starting subgrid index
subgrid_mappings = {
    0: 0,
    1: 0, 
    2: 0,
    3: 3,
    4: 3,
    5: 3,
    6: 6,
    7: 6,
    8: 6,
}

# check if assignment is valid
def is_valid(grid, row, col, num, horizontally_adjacent_constraints, vertically_adjacent_constraints):
    # checking row and column constraints
    for i in range(9):
        # if the number is in the same row or column, invalid assignment
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    # check for 3x3 subgrid constraints
    row_ix = subgrid_mappings[row]
    col_ix = subgrid_mappings[col]
    for i in range(3):
        for j in range(3):
            # if number already in subgrid, assignment is invalid
            if grid[row_ix + i][col_ix + j] == num:
                return False
    
    # EVALUATE DOT CONSTRAINTS:
    
    # check left neighbor
    if col > 0 and horizontally_adjacent_constraints[row][col - 1] > 0:
        left = grid[row][col - 1]
        # if left neighbor has been assigned a value, evaluate dot constraints
        if left:
            # white dot constraint
            if horizontally_adjacent_constraints[row][col - 1] == 1 and abs(left - num) != 1:
                return False
            # black dot constraint
            if horizontally_adjacent_constraints[row][col - 1] == 2 and not (left == 2 * num or num == 2 * left):
                return False
    
    # check right neighbor
    if col < 8 and horizontally_adjacent_constraints[row][col] > 0:
        right = grid[row][col + 1]
        # if the right neighbor has been assigned a value, evaluate dot constraints
        if right:
            # white dot constraint
            if horizontally_adjacent_constraints[row][col] == 1 and abs(right - num) != 1:
                return False
            # black dot constraint
            if horizontally_adjacent_constraints[row][col] == 2 and not (right == 2 * num or num == 2 * right):
                return False

    # check neighbor above
    if row > 0 and vertically_adjacent_constraints[row - 1][col] > 0:
        top = grid[row - 1][col]
        # if cell above has a value, check dot constraints
        if top:
            # white dot constraint
            if vertically_adjacent_constraints[row - 1][col] == 1 and abs(top - num) != 1:
                return False
            # black dot constraint
            if vertically_adjacent_constraints[row - 1][col] == 2 and not (top == 2 * num or num == 2 * top):
                return False
    
    # check neighbor below
    if row < 8 and vertically_adjacent_constraints[row][col] > 0:
        bottom = grid[row + 1][col]
        # if cell below has already been assigned a value, evaluate dot constraints
        if bottom:
            # white dot constraint
            if vertically_adjacent_constraints[row][col] == 1 and abs(bottom - num) != 1:
                return False
            # black dot constraint
            if vertically_adjacent_constraints[row][col] == 2 and not (bottom == 2 * num or num == 2 * bottom):
                return False
    return True

# forward checking algorithm
def inference_forward_checking(grid, row, col, num, order_domain_values):
    # keep track of cells whose domains were modified
    modified = []
    
    # iterate through row neighbors
    for i in range(9):
        # only looks at new cells in different columns that are unassigned, where the number to remove still exists in the domain
        if i != col and not(grid[row][i]) and num in order_domain_values[row][i]:
            # remove number from domain, as it has been assigned a value
            order_domain_values[row][i].remove(num)
            # add to list of modified cells
            modified.append((row, i, num))
            # if removal of value results in empty domain, forward checking has failed
            if len(order_domain_values[row][i]) == 0:
                return False, modified

    # iterate through column neighbors
    for i in range(9):
        # only looks at new cells (in different rows) that are unassigned, where the number is in the domain
        if i != row and not(grid[i][col]) and num in order_domain_values[i][col]:
            # remove number from domain, as has already been assigned
            order_domain_values[i][col].remove(num)
            # add to list of modified cells
            modified.append((i, col, num))
            if not order_domain_values[i][col]:  # Domain becomes empty
                return False, modified
    # if all checks pass, forward checking is successful
    return True, modified

# select unassigned variable using MRV and degree heuristic
def select_unassigned_variable(grid, horizontally_adjacent_constraints, vertically_adjacent_constraints):
    # keep track of smallest number of valid values found so far
    min_left = float('inf')
    # coordinates of unassigned variable to be selected next
    next_var = None
    # keep track of degree heuristic
    max_degree = -float('inf')

    for row in range(9):
        for col in range(9):
            # only looks at unassigned variable
            if grid[row][col] == 0:
                domain = [num for num in range(1, 10) if is_valid(grid, row, col, num, horizontally_adjacent_constraints, vertically_adjacent_constraints)]
                # if the domain has fewer valid numbers/values, update variables
                if len(domain) < min_left:
                    min_left = len(domain)
                    next_var = (row, col)
                    max_degree = calculate_degree(row, col, horizontally_adjacent_constraints, vertically_adjacent_constraints)
                # if the number of valid numbers is the same as the minimum, apply degree heuristic
                elif len(domain) == min_left:
                    degree = calculate_degree(row, col, horizontally_adjacent_constraints, vertically_adjacent_constraints)
                    # if degree is higher, update variables
                    if degree > max_degree:
                        next_var = (row, col)
                        max_degree = degree
    # return final variable after iterating
    return next_var

def calculate_degree(row, col, horizontally_adjacent_constraints, vertically_adjacent_constraints):
    degree = 0
    # check constraint for left neighbor
    if col > 0 and horizontally_adjacent_constraints[row][col - 1] > 0: degree += 1
    # check constraint for right neighbor
    if col < 8 and horizontally_adjacent_constraints[row][col] > 0: degree += 1
    # check constraint for neighbor below
    if row > 0 and vertically_adjacent_constraints[row - 1][col] > 0: degree += 1
    # check constraint neighbor above
    if row < 8 and vertically_adjacent_constraints[row][col] > 0: degree += 1
    return degree

# backtracking, including forward checking
def backtracking(grid, order_domain_values, horizontally_adjacent_constraints, vertically_adjacent_constraints):
    # find next cell to be assigned
    cell = select_unassigned_variable(grid, horizontally_adjacent_constraints, vertically_adjacent_constraints)
    # no assigned variables - done
    if not cell:
        return True
    # extract row and column indices
    row, col = cell

    # iterate over domain over current cell
    for num in order_domain_values[row][col]:
        # check if assignment is valid
        if is_valid(grid, row, col, num, horizontally_adjacent_constraints, vertically_adjacent_constraints):
            # if assignment is valid, assign value to current cell
            grid[row][col] = num
            # calls for forward checking to update domains
            passed, modified = inference_forward_checking(grid, row, col, num, order_domain_values)
            # if forward checking passes, call recursively and select next variable
            if passed:
                if backtracking(grid, order_domain_values, horizontally_adjacent_constraints, vertically_adjacent_constraints):
                    return True
            # if forward checking fails, backtrack and restore domains
            grid[row][col] = 0
            for r, c, value in modified:
                order_domain_values[r][c].append(value)
    # no solution found
    return False

# Main function
def main(input_file, output_file):
    # try to read input file, handles FileNotFoundException if not found, and exits program
    try:
        with open(input_file, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print("File not found. Exiting now...")
        sys.exit(1)
    
    # load grid
    grid = [[int(num) for num in line.split()] for line in lines[:9]]
    # reads and loads constraints between horizontally adjacent cells
    horizontally_adjacent_constraints = [[int(num) for num in line.split()] for line in lines[10:19]]
    # reads and loads constraints between vertically adjacent cells
    vertically_adjacent_constraints = [[int(num) for num in line.split()] for line in lines[20:]]
    # calls is_valid, and loads structure with domains for each cell
    order_domain_values = [[[val for val in range(1, 10) if is_valid(grid, row, col, val, horizontally_adjacent_constraints, vertically_adjacent_constraints)] for col in range(9)] for row in range(9)]

    # if solution found, generate and write to output file
    if backtracking(grid, order_domain_values, horizontally_adjacent_constraints, vertically_adjacent_constraints):
        with open(output_file, 'w') as f:
            for row in grid:
                f.write(' '.join(map(str, row)) + '\n')
    # no solution found - print to console
    else:
        print("No solution found.")

# call main function -> specify input file in first argument and name of output file in the second argument
main('Input3.txt', 'Output3.txt')
