"""
This algorithm solves the Peg Game found at Cracker Barrel stores,
returning a 'genius' solutions (defined below).
It has been generalized to any triangle of side size n, of which the Cracker Barrel version is n = 5.

The Peg Game is a triangular peg board with 15 peg holes and 14 pegs (n = 5),
each inserted into a peg hole but leaving one of the corners empty.
The goal is to end with one remaining peg (the 'genius' solution) by
jumping pegs over each other to open positions and removing the jumped peg.
Ex.: if pegs are in holes 1 and 2, but not 3 (on a board where holes 1 and 2 are adjacent,
as well as 2 and 3, and all 3 are in a line), then the peg in hole 1 would jump over the peg in hole 2
to end in hole 3, while the peg at 2 would be removed from the board.
 
As the Peg Game board says:
    1 peg remaining = genius
    2 pegs remaining = pretty smart
    3 pegs remaining = just plain dumb
    4 or more pegs remaining = 'EG-NO-RA-MOOSE'
"""


import copy
import sys
import csv
import os
from time import process_time
from random import randint


# Define the triangular board; all spaces but the top corner are filled.
#   init_board: 1 = peg, 0 = hole; initial board for starting game.
#   board_nums: gives the hole number.
init_board = []
board_nums = []

# Create dictionaries that define adjacent pegs and jump options:
#   peg_coord gives the peg number for board matrix coordinates.
#   peg_num gives the board matrix coordinates for that peg number.
#   adjacent_holes gives a list of holes adjacent to that hole number.
#   peg_jumps gives the middle hole number for a legitimate jump for two jump-able holes.
peg_coord = {}
peg_num = {}
adjacent_holes = {}
peg_jumps = {}

# Handle arguments.
print_out = False
save = False
for arg in sys.argv:
    if arg == 'print':
        print_out = True
    elif arg == 'save':
        save = True
    else:
        pass

# Set other global variables.
solutions = []
finished_boards = {}  # finished_boards is used to memoize by skipping boards that have been evaluated.


# Create the triangular board with given side length of n.
def peg_game(n):
    
    # Clear dicts and lists.
    global init_board
    global board_nums
    global peg_num
    global adjacent_holes
    global peg_jumps
    init_board = []
    board_nums = []
    peg_num = {}
    adjacent_holes = {}
    peg_jumps = {}
    
    # Initiate  board, board_nums, peg_coord, and peg_num.
    counter = 1
    for i in range(n):

        init_board.append([])
        board_nums.append([])
        
        for j in range(i+1):

            init_board[i].append(1)
            board_nums[i].append(counter)
            peg_coord[(i, j)] = counter
            peg_num[counter] = [i, j]
            counter += 1
    init_board[0][0] = 0

    # Print initial board if user desires.
    if print_out:
        print('\n' + str(n) + 'x' + str(n) + ' board hole numbers:')
        print_board(board_nums)
        print(str(n) + 'x' + str(n) + ' board peg start locations:')
        print_board(init_board)

    # Build a dictionary of adjacent pegs.
    for i in range(1, len(peg_num)+1):
        temp_pegs = []
        
        # Get peg numbers for up to 6 adjacent peg holes.
        try:
            # Peg above and to the left.
            if peg_num[i][0]-1 < 0 or peg_num[i][1]-1 < 0:
                raise IndexError
            temp_pegs.append(board_nums[peg_num[i][0]-1][peg_num[i][1]-1])
        except IndexError:
            pass
        
        try:
            # Peg above and to the right.
            if peg_num[i][0]-1 < 0 or peg_num[i][1] < 0:
                raise IndexError
            temp_pegs.append(board_nums[peg_num[i][0]-1][peg_num[i][1]])
        except IndexError:
            pass
        
        try:
            # Peg to the left.
            if peg_num[i][0] < 0 or peg_num[i][1]-1 < 0:
                raise IndexError
            temp_pegs.append(board_nums[peg_num[i][0]][peg_num[i][1]-1])
        except IndexError:
            pass
        
        try:
            # Peg to the right.
            if peg_num[i][0] < 0 or peg_num[i][1]+1 < 0:
                raise IndexError
            temp_pegs.append(board_nums[peg_num[i][0]][peg_num[i][1]+1])
        except IndexError:
            pass
        
        try:
            # Peg below and to the left.
            if peg_num[i][0]+1 < 0 or peg_num[i][1] < 0:
                raise IndexError
            temp_pegs.append(board_nums[peg_num[i][0]+1][peg_num[i][1]])
        except IndexError:
            pass
        
        try:
            # Peg below and to the right.
            if peg_num[i][0]+1 < 0 or peg_num[i][1]+1 < 0:
                raise IndexError
            temp_pegs.append(board_nums[peg_num[i][0]+1][peg_num[i][1]+1])
        except IndexError:
            pass
         
        # Remove duplicates, sort, and add results to dictionary.
        if i in temp_pegs:
            temp_pegs.remove(i)
        temp_pegs = list(set(temp_pegs))
        temp_pegs.sort()
        adjacent_holes[i] = temp_pegs
    
    # Build a dictionary of jump-able paths.
    for i in range(1, len(peg_num)+1):
        for j in range(1, len(peg_num)+1):
            
            # Get shared pegs.
            middle_pegs = list(set(adjacent_holes[i]) & set(adjacent_holes[j]))
            
            # If they share more or less than 1 peg, they do not make a jump-able path.
            # Also exclude adjacent pegs, as some can only share one peg.
            if len(middle_pegs) is not 1 or i in adjacent_holes[j]:
                continue
            
            # Add to the dictionary.
            peg_jumps[i, j] = middle_pegs[0]
    
    # Call the iterative method, save results.
    print('\nFinding solutions...')
    start = process_time()
    iterate_solve(init_board, [])
    end = process_time()
    time_elapsed = end - start

    global solutions
    num_solutions = len(solutions)

    if num_solutions == 0:
        print('\nNo solutions.\n')
        
    else:
        print('\nFound ' + str(num_solutions) + ' solutions in ' + str(time_elapsed) + ' seconds.\n')

        # Print out a random solution if user desires.
        if print_out:

            rand_num = randint(0, num_solutions)
            for element in solutions[rand_num]:
                move_peg(init_board, element[0], element[1])
            print('\nRandom solution (number ' + str(rand_num) + '):\n')
            print(solutions[rand_num])
            print()
            print_board(init_board)

        # Save the solutions to a CSV file if user desires.
        if save:

            header = ['Move' + str(i) for i in range(1, 13+1)]  # All solutions have 13 moves.
            header = ['SolutionNum'] + header
            filename = '.\\solutions.csv'

            if os.path.isfile(filename):
                os.remove(filename)
            with open(filename, 'w', newline='') as file:
                w = csv.writer(file)
                w.writerow(header)
                for i, solution in enumerate(solutions):
                    w.writerow([i+1] + solution)

            print('\nSolutions saved to file: ' + filename + '\n')


# Iterate through all possible moves to find all solutions.
def iterate_solve(start_board, jump_list):

    global solutions
    global finished_boards

    # Check to see if the board has already been evaluated.
    if convert_board(start_board) in finished_boards:
        # print('len(finished_boards) = ' + str(len(finished_boards)))  # TEMP
        return False

    if sum_board(start_board) == 1:
        solutions.append(jump_list)
        # print('len(solutions) = ' + str(len(solutions)))  # TEMP
        return True

    has_child_solution = False
    for element in peg_jumps:
        
        temp_board = copy.deepcopy(start_board)

        if move_peg(temp_board, element[0], element[1]):
            
            temp_jump_list = copy.deepcopy(jump_list)
            temp_jump_list.append(element)
            child_solution = iterate_solve(temp_board, temp_jump_list)

            # If the board has no child solutions, add it to the dict.
            if not child_solution:
                finished_boards[convert_board(temp_board)] = True
            else:
                has_child_solution = True

    # Check for any child solutions.
    if not has_child_solution:
        finished_boards[convert_board(start_board)] = True
        return False
    else:
        return True


# Move the pegs after checking for jump-ability and correct peg placement.
def move_peg(board, start, end):

    # Run jump checks.
    if (start, end) in peg_jumps:
        
        if (board[peg_num[start][0]][peg_num[start][1]] == 1 and
                board[peg_num[peg_jumps[(start, end)]][0]][peg_num[peg_jumps[(start, end)]][1]] == 1 and
                board[peg_num[end][0]][peg_num[end][1]] == 0):

            board[peg_num[start][0]][peg_num[start][1]] = 0
            board[peg_num[peg_jumps[(start, end)]][0]][peg_num[peg_jumps[(start, end)]][1]] = 0
            board[peg_num[end][0]][peg_num[end][1]] = 1
            return 1
        else:
            return 0
    
    # Compensate for jumping in reverse direction.
    elif (end, start) in peg_jumps:
        
        if (board[peg_num[end][0]][peg_num[end][1]] == 0 and
                board[peg_num[peg_jumps[(end, start)]][0]][peg_num[peg_jumps[(end, start)]][1]] == 1 and
                board[peg_num[start][0]][peg_num[start][1]] == 1):

            board[peg_num[end][0]][peg_num[end][1]] = 1
            board[peg_num[peg_jumps[(end, start)]][0]][peg_num[peg_jumps[(end, start)]][1]] = 0
            board[peg_num[start][0]][peg_num[start][1]] = 0
            return 1
        else:
            return 0

    else:
        return 0


# Given a board, return an ordered tuple of current peg positions.
def convert_board(board):

    peg_pos = []

    for i, row in enumerate(board):
        for j, peg in enumerate(row):
            if peg == 1:
                peg_pos.append(peg_coord[(i, j)])

    return tuple(peg_pos)


# Return number of pegs on board.
def sum_board(board):
    return sum([sum(row) for row in board])


# Print the board.
def print_board(board):

    for element in board:
        print(element)

    # Add buffer line.
    print()


if __name__ == '__main__':

    # The original Peg Game has n = 5.
    peg_game(5)
