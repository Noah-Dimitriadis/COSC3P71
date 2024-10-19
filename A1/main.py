'''
Noah Diomitriadis 
Student number: 7558224
Email: nd22zr@brocku.ca

This is the main file for the assignment.

Imported my Cell class
Easygui is for reading the file
PriorityQueue is the data structure that A* uses 
Deepcopy is used to expand a node
Time is for timing each algorithm

When running this file please ensure that easygui has installed. The console will output further instructions

'''

from Cell import Cell
import easygui as gui
from queue import PriorityQueue
from copy import deepcopy
import time


# This function generates a list of possible moves for a given board state
def generate_moves(position:list) -> list[list]:
    position[4].append(deepcopy(position[3]))       # add current position to the parent list

    empty_cell = find_empty(position)
    move_coordinates = [            # this is a list of all possible moves
        empty_cell.row,
        empty_cell.col + 1,
        empty_cell.row,
        empty_cell.col - 1,
        empty_cell.row - 1,
        empty_cell.col,
        empty_cell.row + 1,
        empty_cell.col
    ]

    all_moves = []

    for i in range(0, 8, 2):        # iterate 2 at a time to get each x,y pair of moves we can make, 4 possible total
        copy = deepcopy(position)   # need all data to be a clean copy for each new generated move

        row = move_coordinates[i]
        col = move_coordinates[i+1]

        if row < copy[0] and row >= 0 and col < copy[0] and col >= 0:     # if move is legal
            # swapping values for each cell
            temp = copy[3][row][col].value
            copy[3][row][col].value = copy[3][empty_cell.row][empty_cell.col].value
            copy[3][empty_cell.row][empty_cell.col].value = temp
            
            if not position[4] or copy[3] not in position[4]:       # if the parent is empty or the generated move isnt already in the parent list
                copy[1] = position[1] + 1
                all_moves.append(copy)

    return all_moves

# This function checks if a given board state is solved or not
def is_solved(position:list) -> bool:
    # the way this works is, we iterate the board row by row, we should see all the numbers incrementing by 1, if the current cell doesnt == the expected incremented value the board is not solved
    board = position[3] 
    max = position[0]*position[0]       # the maximum number of cells
    count = 1           # index 1 has the number 1
    for row in board:
        for cell in row:
            if cell.value == 'X':       #if we are on the 'X' but we are not on the last cell of the board then it is not solved
                if count == max: return True
                else: return False
            if int(cell.value) != count: return False       # if the current cell isnt holding the count then we know the cells value is in the wrong spot
            count += 1
    return True

# This function finds where the empty cell is/the cell holding the 'X'
def find_empty(position:list) -> Cell:
        board = position[3]
        for row in board:
            for cell in row:
                if cell.value == 'X': return cell       # hey we found it, also we know it will ALWAYS be on the board

# This function returns the cell that is currently holding the target value for a board of any inputted size
def find_position(position:list, target:int) -> Cell:
    board = position[3]
    for row in board:
        for cell in row:
            if cell.value == str(target):       # if our input value is at the current state return the current cell
                return cell

# This function returns the cell that should hold the inputted value for a board of any inputted size
def find_goal_pos(size:int, value:int) -> Cell:
    # this calculates a given values goal position for a board of a given size
    count = 1
    for i in range(size):
        for j in range(size):
            if count == value:      # if our input value is at the current state return the current cell
                return Cell(value, i, j)
            count += 1

# This function calculates the number of misplaced tiles for a given board state. This heuristics explanation is in the write up, I didnt want to write it here.
def misplaced(position:list) -> int:
    # Heuristic from class -> # of tiles in the wrong spot
    board = position[3]
    current = 1     # start at 1 because there is no '0' value tile
    count = 0
    for row in board:
        for cell in row:
            if cell.value == 'X':
                pass
            elif int(cell.value) != current:    # basically so long as the current index == the current cell value then the cell value is in the right spot
                count += 1      # if the cell value doesnt == the current then we have a mispalaced tile
            current += 1
    return count
    
# This function calculates the total manhattan distance for a given board state. This heuristics explanation is in the write up, I didnt want to write it here.
def manhattan_distance(position:list) -> int:
    # Heuristic from class -> manhattan distance
    total = 0
    total_cells = position[0]*position[0]

    for i in range(1, total_cells):
        target_cell = find_position(position, i)        # find out where the current index value is on the board
        if target_cell.value != 'X':        # we dont *really* care where the empty cell is, we are not calculating it into the heuristic
            goal_cell = find_goal_pos(position[0], i)        # find where the current index value goal state is
            total = total + abs(target_cell.row - goal_cell.row) + abs(target_cell.col - goal_cell.col)     # this will calculate how many rows and cols away the current indexes
            # value is from its goal position

    return total        # our total manhattan distance

# This function calculates the misplaced rows and columns heuristic for a given board state. This heuristics explanation is in the write up, I didnt want to write it here.
def misplaced_rows_cols(position:list) -> int:
    total = 0
    total_cells = position[0]*position[0]

    for i in range(1, total_cells):
        target_cell = find_position(position, i)        # find where the current index value actually is on the board
        if target_cell.value != 'X':        # we dont *really* care where the empty cell is, we are not calculating it into the heuristic
            goal_cell = find_goal_pos(position[0], i)        # find where the current index should be in the goal state

            row = abs(target_cell.row - goal_cell.row)      # calculate the displacement of the target node
            col = abs(target_cell.col - goal_cell.col)
            if row > 0:     # if there is displacement then +=1 on the total
                total += 1
            if col > 0:     # check for the column as well 
                total += 1

    return total        # return our heuristic for the board

# This is the function that performs the A* algorithm with the misplaced tiles heuristic. It is functionally identical to a_star_manhattan and a_star_rows_cols
# so the explanation for the functionality of those can be found here, the actual heuristic functions are above
def a_star_misplaced(starting_position:list, max:int) -> list[list]:
    open = PriorityQueue()
    closed = []
    heuristic = misplaced(starting_position)        # we dont *really* have to do this here because it is the only node on the frontier, but we use this variable later so i initialized it here
    open.put((heuristic, starting_position))

    while open:
        current_state = open.get()[1]       # we pass in a tuple so we need the actual position hence the [1] at the end here
        current_depth = current_state[1]

        if is_solved(current_state): break      # break if the current state is the solution
        if current_depth == max: return []      # return nothing if the solution isnt found by a certain depth

        moves = generate_moves(current_state)
        for move in moves:
            if move[3] not in closed:       # as long as a newly generated move hasnt been seen before we add it to the frontier and calculate its heuristic
                heuristic = current_depth + misplaced(move)     # add the current depth plus the calculated heuristic function to make the actual heuristic, this way
                # higher nodes with the same heuristic calculated against them will be at the front of the pq
                move[2] = heuristic     # this is never used again but it was helpful for debugging so i kept it
                open.put((heuristic, move))
        
        current_state[4] = []       # just want to remove all the parents from past nodes, this cuts down on execution time as we arent dragging around parent lists at every single node

        closed.append(current_state[3])

    current_state[4].append(current_state[3])   # add initial state to our path
    return current_state[4]         # return our path

# This function performs the A* algorithm with the manhattan distance heuristic, it is functionally identical to a_star_misplaced and a_star_rows_cols, 
# please see the comments on a_star_misplaced for the explanation
def a_star_manhattan(starting_position:list, max:int) -> list[list]:
    open = PriorityQueue()
    closed = []
    heuristic = misplaced(starting_position)
    open.put((heuristic, starting_position))

    while open:
        current_state = open.get()[1]       # we pass in a tuple so we need the actual position hence the [1] at the end here
        current_depth = current_state[1]

        if is_solved(current_state): break      # break if the current state is the solution
        if current_depth == max: return []
        moves = generate_moves(current_state)
        
        for move in moves:
            if move[3] not in closed:       # as long as a newly generated move hasnt been seen before we add it to the frontier and calculate its heuristic
                heuristic = current_depth + manhattan_distance(move)
                move[2] = heuristic     # this is never used again but it was helpful for debugging so i kept it
                open.put((heuristic, move))
        
        current_state[4] = []       # just want to remove all the parents from past nodes, this cuts down on execution time as we arent dragging around parent lists at every single node

        closed.append(current_state[3])

    current_state[4].append(current_state[3])   # add initial state to our path
    return current_state[4]

# This function performs the A* algorithm with the misplaced rows and columns heuristic, it is functionally identical to a_star_manhattan and a_star_misplaced, 
# please see the comments on a_star_misplaced for the explanation
def a_star_rows_cols(starting_position:list, max:int) -> list[list]:
    # the A* algorithm using the misplaced rows and columns heuristic
    open = PriorityQueue()
    closed = []
    heuristic = misplaced(starting_position)
    open.put((heuristic, starting_position))

    while open:
        current_state = open.get()[1]       # we pass in a tuple so we need the actual position hence the [1] at the end here
        current_depth = current_state[1]
        if is_solved(current_state): break      # break if the current state is the solution
        if current_depth == max: return []
        moves = generate_moves(current_state)
        
        for move in moves:
            if move[3] not in closed:       # as long as a newly generated move hasnt been seen before we add it to the frontier and calculate its heuristic
                heuristic = current_depth + misplaced_rows_cols(move)
                move[2] = heuristic     # this is never used again but it was helpful for debugging so i kept it
                open.put((heuristic, move))
        
        current_state[4] = []       # just want to remove all the parents from past nodes, this cuts down on execution time as we arent dragging around parent lists at every single node

        closed.append(current_state[3])

    current_state[4].append(current_state[3])   # add initial state to our path
    return current_state[4]

# This function performs the A* algorithm, it will select what version of the algorithm to run based on the heuristic parameter, all the if-else blocks are identical 
# (except for the heuristic of course) so I will only comment on 1 of them. This algorithm will search to a max depth of 1000 which I think is reasonable seeing as 1000 would take 
# forever to deal with so this can pretty much run indefinitely 
def a_star(starting_position:list, heuristic:int):
    if heuristic == 1:
        print('A* with the misplaced tiles heuristic')
        start =  time.time()
        p = a_star_misplaced(starting_position, 1000)       # max depth of 1000 by default
        end = time.time()
        total = end - start     # elapsed time

        for move in p:
            print_move(move)
        if len(p) > 0:      # if the path is empty then we have not found a solution
            print(f'Solved the puzzle in {total} seconds with {len(p)-1} moves')        # -1 for the initial move
        else:
            print(f'The puzzle could not be solved by the max depth of 1000. Total execution time was {total} seconds\n')

        

    elif heuristic == 2:
        print('A* with the manhattan distance heuristic')
        start =  time.time()
        p = a_star_manhattan(starting_position, 1000)       # max depth of 1000 by default
        end = time.time()
        total = end - start

        for move in p:
            print_move(move)

        if len(p) > 0:
            print(f'Solved the puzzle in {total} seconds with {len(p)-1} moves')        # -1 for the initial move
        else:
            print(f'The puzzle could not be solved by the max depth of 1000. Total execution time was {total} seconds\n')

    elif heuristic == 3:
        print('A* with the misplaced rows and columns heuristic')
        start =  time.time()
        p = a_star_rows_cols(starting_position, 1000)       # max depth of 1000 by default
        end = time.time()
        total = end - start

        for move in p:
            print_move(move)

        if len(p) > 0:
            print(f'Solved the puzzle in {total} seconds with {len(p)-1} moves')        # -1 for the initial move
        else:
            print(f'The puzzle could not be solved by the max depth of 1000. Total execution time was {total} seconds\n')
    else:
        print('Invalid heuristic choice')

# This function performs the Iterative Deepening A* algorithm for a selected heuristic, each block of selected heuristic is the same so I will only make comments on the first one.
def IDA_star(starting_position:list, heuristic:int, max_depth:int):
    solved = False
    if heuristic == 1:
        print('Iteraitive Depth A* with the misplaced tiles heuristic')
        start =  time.time()
        for limit in range(1, max_depth):       # starting at 0 would mean just the initial node, we can skip this because if the initial node is the solution we will return it instantly
            path = a_star_misplaced(starting_position, limit) 
            if path:        # if the path is not empty then we have found a soltution
                print(f'Found a solution at depth: {limit-1}.')     # -1 because if a solution is not found at depth = limit it will break on the first instance of that depth, 
                # however if the solution is at depth = limit then we need to iterate one more time to check them all
                solved = True
                break
        end = time.time()
        total = end - start # elapsed time
        if solved:
            for move in path:
                print_move(move)
            if len(path) > 0:
                print(f'Solved the puzzle in {total} seconds with {len(path)-1} moves\n')        # -1 for the initial move
        else:
            print(f'The puzzle could not be solved by the max depth of {max_depth}. Total execution time was {total} seconds\n')    
        

    elif heuristic == 2:
        print('Iteraitive Depth A* with the manhattan distance heuristic')
        start =  time.time()
        for limit in range(1, max_depth):
            path = a_star_manhattan(starting_position, limit) 
            if path: 
                print(f'Found a solution at depth: {limit-1}.')
                solved = True
                break
        end = time.time()
        total = end - start
        if solved:
            for move in path:
                print_move(move)
            if len(path) > 0:
                print(f'Solved the puzzle in {total} seconds with {len(path)-1} moves\n')        # -1 for the initial move
        else:
            print(f'The puzzle could not be solved by the max depth of {max_depth}. Total execution time was {total} seconds\n')      
        
    elif heuristic == 3:
        print('Iteraitive Depth A* with the misplaced rows and columns heuristic')
        start =  time.time()
        for limit in range(1, max_depth):
            path = a_star_rows_cols(starting_position, limit) 
            if path: 
                print(f'Found a solution at depth: {limit-1}.')
                solved = True
                break
        end = time.time()
        total = end - start
        if solved:
            for move in path:
                print_move(move)
            if len(path) > 0:
                print(f'Solved the puzzle in {total} seconds with {len(path)-1} moves\n')        # -1 for the initial move
        else:
            print(f'The puzzle could not be solved by the max depth of {max_depth}. Total execution time was {total} seconds')    

    else:
        print('Invalid heuristic choice')

# This function performs a depth first search to a limit, if a solution is found it will return that solution otherwise it will return an empty list
def DFS(starting_position:list, max:int) -> list[list]:
    open = []
    closed = []

    open.append(starting_position)
    while open:
        current_state = open.pop(0)     # front item of the list
        current_depth = current_state[1]
        
        if is_solved(current_state): break      # we have solved the puzzle
        if current_depth == max: return []      # we have reached the maximum depth
        moves = generate_moves(current_state)
        
        for move in moves:
            if move[3] not in closed:       # as long as a newly generated move hasnt been seen before we add it to the frontier
                open.append(move)
        
        current_state[4] = []       # just want to remove all the parents from past nodes, this cuts down on execution time as we arent dragging around parent lists at every single node, only the ones that need it
        
        closed.append(current_state[3]) # we have now processed this node

    current_state[4].append(current_state[3])   # add initial state to our path
    return current_state[4]     # return the path

# This function runs the Iterative Deepening Depth First Search algorithm (IDDFS for short) and will compute the run time of the algorithm once completed
def IDDFS(starting_position:list, max:int):
    solved = False
    start =  time.time()
    for limit in range(1, max):
        print(f'Checking to depth: {limit-1}')      # it will technically check 1 move below for the current iteration accounting for the initial state 
        path = DFS(starting_position, limit)
        if path: 
            print(f'Found a solution at depth: {limit-1}.')
            solved = True
            break
    end = time.time()
    total = end - start     # elapsed time
    if solved:
        for move in path:
            print_move(move)        # print each board state in the path, strictly the board
        if len(path) > 0:
            print(f'Solved the puzzle in {total} seconds with {len(path)-1} moves\n')        # -1 for the initial move
    else:
        print(f'The puzzle could not be solved by the max depth of {max}. Total execution time was {total} seconds\n')

# This function will read a file and generate the gameboard and all its properties from that file
def start_game() -> list:
    starting_position = [0,0,0,[],[]]         # size, depth, heuristic value, board, parent/path list IN THAT ORDER
    lines = read_file()

    size = int(lines[0][0])         # just wanted a nice variable name so you can see what value this is
    starting_position[0] = size
    board = []

    row_index = 0
    for row in lines[1:]:       # skip the header
        numbers = row.split(' ')        # split along each number  
        temp = []    
        col_index = 0
        for num in numbers:
            temp.append(Cell(num, row_index, col_index))
            col_index += 1
        board.append(temp)
        row_index += 1
        
    starting_position[3] = board
    return starting_position

# This function opens the easygui file box and alows the user to select a file
def read_file():
    file = open(gui.fileopenbox()).readlines()
    return [line.strip() for line in file]      # returns the file with cleaned up lines for easy traversal later

# Prints the entire position, its size, heuristic score and depth
def print_board(position:list):
    print(f'Size: {position[0]}|Depth: {position[1]}|Heuristic: {position[2]}')
    print_move(position[3]) # the board itself is stored at this index

# Prints the just the board of the current move        
def print_move(move:list):
    for row in move:
        print('|', end="")      # niceish formatting
        for cell in row:
            print(f'{cell.value}|', end="")
        print()
    print()

# this function is the main ui part of the program, here user input will determine what algorithm is used, if A* is selected then a heuristic selection window will appear, There is also an option to select a new file
def main():
    print("Hello there! Provided all the requirements from 'requirements.txt' have been installed correctly, you should see a pop up window promting you to select a file. Please select it now!")
    gameboard = start_game()
    continue_game = True
    while continue_game:   
        try:
            print('Please select what algorithm you would like to solve your puzzle with:\n1 for Iterative Deepening Depth First Search\n2 for A*\n3 for IDA*\n0 to quit')
            selection = int(input('Enter your selection: '))
        except ValueError:
            print('Invalid value. Please enter an integer between 1-3 or 0 to quit.\n')
            continue
        if selection > 3 or selection < 0:
            print('Invalid integer. Please enter an integer between 1-3 or 0 to quit.\n')
            continue
        
        if selection == 0:
            print('Goodbye!')
            break
        
        elif selection == 1:
            print('You have chosen Iterative Deepening Depth First Search!')
            while True:
                try:
                    max_depth = int(input('Please enter your maximum depth: '))
                except ValueError:
                    print('Invalid value. Please enter an integer.\n')
                    continue
                if max_depth < 0:
                    print('Invalid value. Please enter a positive integer.\n')
                    continue
                else:
                    break
            IDDFS(gameboard, max_depth)
            print()
        
        elif selection == 2:
            print('You have chosen A* Search!')
            while True:
                try:
                    heuristic = int(input('Please enter the heuristic you would like to solve with.\n1 for misplaced tiles\n2 for manhattan distance\n3 for misplaced rows and columns\nEnter your selection: '))
                except ValueError:
                    print('Invalid value. Please enter an integer.\n')
                    continue
                if heuristic < 0 or heuristic > 3:
                    print('Invalid value. Please enter an integer between 1-3.\n')
                    continue
                else:
                    break
            a_star(gameboard, heuristic)
            print()
        
        elif selection == 3:
            print('You have chosen Iterative Deepening A* Search!')
            while True:
                try:
                    heuristic = int(input('Please enter the heuristic you would like to solve with.\n1 for misplaced tiles\n2 for manhattan distance\n3 for misplaced rows and columns\nEnter your selection: '))
                except ValueError:
                    print('Invalid value. Please enter an integer.\n')
                    continue
                if heuristic < 0 or heuristic > 3:
                    print('Invalid value. Please enter an integer between 1-3\n')
                else:
                    break
            while True:
                try:
                    max_depth = int(input('Please enter your maximum depth: '))
                except ValueError:
                    print('Invalid value. Please enter an integer.\n')
                    continue
                if max_depth < 0:
                    print('Invalid value. Please enter a positive integer.\n')
                    continue
                else:
                    break
            IDA_star(gameboard, heuristic, max_depth)
            print()
        while True:
            try:
                value = int(input('Enter 1 for the same file\nEnter 2 to choose a different file\nPress 0 to quit\nEnter your choice: '))
            except ValueError:
                print('Invalid value. Please enter a valid selection.\n')
                continue
            if value < 0 or value > 2:
                print('Invalid value. Please enter a valid selection\n')
                continue
            if value == 0:
                print('Goodbye!')
                continue_game = False
                break
            elif value == 2:
                print()
                gameboard = start_game()
                break
            else:
                print()
                break

# Start the program
if __name__ == "__main__":
    main()