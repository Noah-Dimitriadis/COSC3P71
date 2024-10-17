from Cell import Cell
import easygui as gui
from queue import PriorityQueue
from copy import deepcopy
import time

'''
TODO optimise move generation and compare with closed list in generate function?


TODO implement other heurstics and create heuristic selection functionality

'''

def generate_moves(position:list) -> list[list]:
    position[4].append(deepcopy(position[3]))
    empty_cell = find_empty(position)
    move_coordinates = [
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

    for i in range(0, 8, 2):
        copy = deepcopy(position)

        row = move_coordinates[i]
        col = move_coordinates[i+1]

        if row < copy[0] and row >= 0 and col < copy[0] and col >= 0:     # if move is legal
            temp = copy[3][row][col].value
            copy[3][row][col].value = copy[3][empty_cell.row][empty_cell.col].value
            copy[3][empty_cell.row][empty_cell.col].value = temp
            
            if not position[4] or copy[3] not in position[4]:   
                copy[1] = position[1] + 1
                all_moves.append(copy)

    return all_moves

def is_solved(position:list) -> bool:
    board = position[3] 
    max = position[0]*position[0]
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
    count = 1
    for i in range(size):
        for j in range(size):
            if count == value:
                return Cell(value, i, j)
            count += 1

def misplaced(position:list) -> int:
    # Heuristic from class -> # of tiles in the wrong spot
    board = position[3]         # this is where the current game board is located
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
        if target_cell.value != 'X':
            goal_cell = goal_pos(position[0], i)
            total = total + abs(target_cell.row - goal_cell.row) + abs(target_cell.col - goal_cell.col)

    return total

def heuristic_self(position:list) -> int:
    # Heuristic not covered in class TBD

    pass

def a_star(starting_position:list) -> list[list]:
    solved = False
    path = []
    open = PriorityQueue()
    closed = []
    heuristic = misplaced(starting_position)
    open.put((heuristic, starting_position))

    while open:
        current_state = open.get()[1]
        solved = is_solved(current_state)
        current_depth = current_state[1]

        if solved: break
        if current_depth == 50: break
        moves = generate_moves(current_state)
        
        for move in moves:
            if move[3] not in closed:
                heuristic = current_depth + manhattan_distance(move)
                move[2] = heuristic
                open.put((heuristic, move))
        if not solved:
            current_state[4] = []
        closed.append(current_state[3])

    if not solved: return []
    path = current_state[4]
    path.append(current_state[3])
    return path

def DFS(starting_position:list, max:int) -> list[list]:
    solved = False
    path = []
    open = []
    closed = []
    open.append(starting_position)

    while open: 
        current_state = open.pop(0)
        solved = is_solved(current_state)
        current_depth = current_state[1]
        if solved: break
        if current_depth == max: break
        moves = generate_moves(current_state)
        
        for move in moves:
            if move[3] not in closed:
                open.append(move)
        if not solved:
            current_state[4] = []
        closed.append(current_state[3])

    if not solved: return []
    path = current_state[4]
    path.append(current_state[3])
    return path

def start_game() -> list:
    starting_position = [0,0,0,[],[]]         # size, depth, heuristic value, board, parent
    lines = read_file()

    size = int(lines[0][0]) 
    starting_position[0] = size
    board = []
    parent = []

    row_index = 0
    for row in lines[1:]:
        numbers = row.split(' ')    
        temp = []    
        col_index = 0
        for num in numbers:
            temp.append(Cell(num, row_index, col_index))
            col_index += 1
        board.append(temp)
        row_index += 1
        

    starting_position[3] = board
    starting_position[4] = parent
    return starting_position

def read_file():
    file = open(gui.fileopenbox()).readlines()
    return [line.strip() for line in file]

def print_board(position:list):
    print_move(position[3]) # the board itself is stored at this index
    print(f'Size: {position[0]}|Depth: {position[1]}|Heuristic: {position[2]}')
        
def print_move(move:list):
    for row in move:
        print('|', end="")
        for cell in row:
            print(f'{cell.value}|', end="")
        print()
    print()

if __name__ == "__main__":
    gb = start_game()
    start =  time.time()
    p = a_star(gb)
    end = time.time()

    total = end-start
    for move in p:
        print_move(move)

    print(f'Solved the puzzle in {total} seconds with {len(p)-1} moves')        # -1 for the initial move
