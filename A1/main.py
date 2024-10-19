from Cell import Cell
import easygui as gui
from queue import PriorityQueue
from copy import deepcopy
import time

'''
TODO implement other heurstics
'''

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

def is_solved(position:list) -> bool:
    board = position[3] 
    max = position[0]*position[0]       # the maximum number of cells
    count = 1           # index 1 has the number 1
    for row in board:
        for cell in row:
            if cell.value == 'X':
                if count == max: return True
                else: return False
            if int(cell.value) != count: return False
            count += 1
    return True

def find_empty(position:list) -> Cell:
        board = position[3]
        for row in board:
            for cell in row:
                if cell.value == 'X': return cell

def find_position(position:list, target:int) -> Cell:
    board = position[3]
    for row in board:
        for cell in row:
            if cell.value == str(target):
                return cell

def goal_pos(size:int, value:int) -> Cell:
    # this calculates a given values goal position for a board of a given size
    count = 1
    for i in range(size):
        for j in range(size):
            if count == value:
                return Cell(value, i, j)
            count += 1

def misplaced(position:list) -> int:
    # Heuristic from class -> # of tiles in the wrong spot
    board = position[3]
    current = 1
    count = 0
    for row in board:
        for cell in row:
            if cell.value == 'X':
                pass
            elif int(cell.value) != current: 
                count += 1
            current += 1
    return count
    
def manhattan_distance(position:list) -> int:
    # Heuristic from class -> manhattan distance
    total = 0
    total_cells = position[0]*position[0]
    for i in range(1, total_cells):
        target_cell = find_position(position, i)
        if target_cell.value != 'X':        # we dont *really* care where the empty cell is, we are not calculating it into the heuristic
            goal_cell = goal_pos(position[0], i)
            total = total + abs(target_cell.row - goal_cell.row) + abs(target_cell.col - goal_cell.col)

    return total

def heuristic_self(position:list) -> int:
    # Heuristic not covered in class TBD

    return 0

def a_star_misplaced(starting_position:list, max:int) -> list[list]:
    solved = False
    open = PriorityQueue()
    closed = []
    heuristic = misplaced(starting_position)
    open.put((heuristic, starting_position))

    while open:
        current_state = open.get()[1]       # we pass in a tuple so we need the actual position hence the [1] at the end here
        solved = is_solved(current_state)
        current_depth = current_state[1]

        if solved: break
        if current_depth == max: return []      # return nothing if the solution isnt found by a certain depth
        moves = generate_moves(current_state)
        
        for move in moves:
            if move[3] not in closed:       # as long as a newly generated move hasnt been seen before we add it to the frontier and calculate its heuristic
                heuristic = current_depth + misplaced(move)
                move[2] = heuristic     # this is never used again but it was helpful for debugging so i kept it
                open.put((heuristic, move))
        
        current_state[4] = []       # just want to remove all the parents from past nodes, this cuts down on execution time as we arent dragging around parent lists at every single node

        closed.append(current_state[3])

    current_state[4].append(current_state[3])   # add initial state to our path
    return current_state[4]

def a_star_manhattan(starting_position:list, max:int) -> list[list]:
    solved = False
    open = PriorityQueue()
    closed = []
    heuristic = misplaced(starting_position)
    open.put((heuristic, starting_position))

    while open:
        current_state = open.get()[1]       # we pass in a tuple so we need the actual position hence the [1] at the end here
        solved = is_solved(current_state)
        current_depth = current_state[1]

        if solved: break
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

def a_star_PLACEHOLDER(starting_position:list, max:int) -> list[list]:
    solved = False
    open = PriorityQueue()
    closed = []
    heuristic = misplaced(starting_position)
    open.put((heuristic, starting_position))

    while open:
        current_state = open.get()[1]       # we pass in a tuple so we need the actual position hence the [1] at the end here
        solved = is_solved(current_state)
        current_depth = current_state[1]

        if solved: break
        if current_depth == max: return []
        moves = generate_moves(current_state)
        
        for move in moves:
            if move[3] not in closed:       # as long as a newly generated move hasnt been seen before we add it to the frontier and calculate its heuristic
                heuristic = current_depth + heuristic_self(move)
                move[2] = heuristic     # this is never used again but it was helpful for debugging so i kept it
                open.put((heuristic, move))
        
        current_state[4] = []       # just want to remove all the parents from past nodes, this cuts down on execution time as we arent dragging around parent lists at every single node

        closed.append(current_state[3])

    current_state[4].append(current_state[3])   # add initial state to our path
    return current_state[4]

def a_star(starting_position:list, heuristic:int):
    if heuristic == 1:
        print('A* with the misplaced tiles heuristic')
        start =  time.time()
        p = a_star_misplaced(starting_position, 1000)       # max depth of 1000 by default
        end = time.time()
        total = end - start

        for move in p:
            print_move(move)
        if len(p) > 0:
            print(f'Solved the puzzle in {total} seconds with {len(p)-1} moves')        # -1 for the initial move
        

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

    elif heuristic == 3:
        print('A* with the PLACEHOLDER heuristic')
        start =  time.time()
        p = a_star_PLACEHOLDER(starting_position, 1000)       # max depth of 1000 by default
        end = time.time()
        total = end - start

        for move in p:
            print_move(move)
        if len(p) > 0:
            print(f'Solved the puzzle in {total} seconds with {len(p)-1} moves')        # -1 for the initial move

    else:
        print('Invalid heuristic choice')

def IDA_star(starting_position:list, heuristic:int, max_depth:int):
    solved = False
    if heuristic == 1:
        print('Iteraitive Depth A* with the manhattan distance heuristic')
        start =  time.time()
        for limit in range(1, max_depth):
            path = a_star_misplaced(starting_position, limit) 
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
        print('Iteraitive Depth A* with the PLACEHOLDER heuristic')
        start =  time.time()
        for limit in range(1, max_depth):
            path = a_star_PLACEHOLDER(starting_position, limit) 
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

def DFS(starting_position:list, max:int) -> list[list]:
    solved = False
    open = []
    closed = []

    open.append(starting_position)
    while open:
        current_state = open.pop(0)     # front item of the list
        solved = is_solved(current_state)
        current_depth = current_state[1]
        
        if solved: break
        if current_depth == max: return []
        moves = generate_moves(current_state)
        
        for move in moves:
            if move[3] not in closed:       # as long as a newly generated move hasnt been seen before we add it to the frontier
                open.append(move)
        
        current_state[4] = []       # just want to remove all the parents from past nodes, this cuts down on execution time as we arent dragging around parent lists at every single node
        
        closed.append(current_state[3]) # we have now processed this node

    current_state[4].append(current_state[3])   # add initial state to our path
    return current_state[4]

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
    total = end - start
    if solved:
        for move in path:
            print_move(move)
        if len(path) > 0:
            print(f'Solved the puzzle in {total} seconds with {len(path)-1} moves\n')        # -1 for the initial move
    else:
        print(f'The puzzle could not be solved by the max depth of {max}. Total execution time was {total} seconds\n')

def start_game() -> list:
    starting_position = [0,0,0,[],[]]         # size, depth, heuristic value, board, parent/path list
    lines = read_file()

    size = int(lines[0][0]) 
    starting_position[0] = size
    board = []

    row_index = 0
    for row in lines[1:]:       # skip the header
        numbers = row.split(' ')    
        temp = []    
        col_index = 0
        for num in numbers:
            temp.append(Cell(num, row_index, col_index))
            col_index += 1
        board.append(temp)
        row_index += 1
        

    starting_position[3] = board
    return starting_position

def read_file():
    file = open(gui.fileopenbox()).readlines()
    return [line.strip() for line in file]

def print_board(position:list):
    print(f'Size: {position[0]}|Depth: {position[1]}|Heuristic: {position[2]}')
    print_move(position[3]) # the board itself is stored at this index
        
def print_move(move:list):
    for row in move:
        print('|', end="")
        for cell in row:
            print(f'{cell.value}|', end="")
        print()
    print()

if __name__ == "__main__":
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
                    heuristic = int(input('Please enter the heuristic you would like to solve with.\n1 for misplaced tiles\n2 for manhattan distance\n3 for PLACEHOLDER\nEnter your selection: '))
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
                    heuristic = int(input('Please enter the heuristic you would like to solve with.\n1 for misplaced tiles\n2 for manhattan distance\n3 for PLACEHOLDER\nEnter your selection: '))
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

        
    
