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


# Define the triangular board; all spaces but the top corner are filled.
# init_board: 1 = peg, 0 = hole; initial board for starting game.
# board_nums: gives the hole number.
init_board = []
board_nums = []

# Create dictionaries that define adjacent pegs and jump options.
# peg_num gives the board matrix coordinates for that peg number.
# adjacent_holes gives a list of holes adjacent to that hole number.
# peg_jumps gives the middle hole number for a legitimate jump for two jump-able holes.
peg_num = {}
adjacent_holes = {}
peg_jumps = {}

# Handle arguments.
print_out = True
save = False
for arg in sys.argv:
    if arg == 'print':
        print_out = False
    elif arg == 'save':
        save = True
    else:
        pass


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
    
    # Initiate  board, board_nums, and peg_num.
    counter = 1
    for i in range(n):

        init_board.append([])
        board_nums.append([])
        
        for j in range(i+1):

            init_board[i].append(1)
            board_nums[i].append(counter)
            peg_num[counter] = [i, j]
            counter += 1
            
    init_board[0][0] = 0
    print('\n' + str(n) + 'x' + str(n) + ' board peg numbers:')
    print_board(board_nums)
    print(str(n) + 'x' + str(n) + ' board peg locations:')
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
    solutions = iterate_solve(init_board, [])
    
    if solutions == -1:
        print('\nNo solution\n')
        
    else:
        
        for element in solutions:
            move_peg(init_board, element[0], element[1])
            
        print('\nFinal ordered solution:\n')
        print(solutions)
        print()
        print_board(init_board)


# Iterate through all possible moves to find all solutions.
def iterate_solve(start_board, jump_list):
    
    if sum_board(start_board) == 1:
        return jump_list
    
    for element in peg_jumps:
        
        temp_board = copy.deepcopy(start_board)
        
        if move_peg(temp_board, element[0], element[1]):
            
            temp_list = copy.deepcopy(jump_list)
            temp_list.append(element)
            temp = iterate_solve(temp_board, temp_list)
            
            if temp == -1:
                continue
            
            else:
                return temp
    
    if sum_board(start_board) is not 1:
        return -1


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
