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
    # position[4].append(position[3])
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
                # copy[4] = position[4]
                all_moves.append(copy)
    return all_moves

def is_solved(position:list) -> bool:
    board = position[3] 
    count = 1           # index 1 has the number 1
    for row in board:
        for cell in row:
            if cell.value == 'X':
                if count == 9: return True
                else: return False
            if int(cell.value) != count: return False
            count += 1
    return True

def find_empty(position:list) -> Cell:
        board = position[3]
        for row in board:
            for cell in row:
                if cell.value == 'X': return cell

def heuristic_class_1(position:list) -> int:
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
    
def heuristic_class_2() -> int:
    # Heuristic from class -> manhattan distance

    pass

def heuristic_self() -> int:
    # Heuristic not covered in class TBD

    pass

def a_star(starting_position:list) -> list[list]:
    solved = False
    path = []
    open = PriorityQueue()
    closed = []
    heuristic = heuristic_class_1(starting_position)
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
                heuristic = current_depth + heuristic_class_1(move)
                move[2] = heuristic
                open.put((heuristic, move))
        if not solved:
            current_state[4] = []
        closed.append(current_state[3])

    if not solved: return []
    path = current_state[4]
    # path.append(current_state[3])

    return path

def DFS(starting_position:list, max:int) -> list[list]:
    solved = False
    path = []
    closed = []
    open = []

    current_state = []
    
    open.insert(0, starting_position)
    for i in range(0,max):
        print(f'Current depth is {i}')
        if solved: break
        while open:
            current_state = open.pop(0)
            if is_solved(current_state): 
                solved = True
                break
            if current_state.depth > i+2: break

            moves = generate_moves(current_state)
            for move in moves:
                duplicate = False
                for closed_move in closed:
                    if move == closed_move:
                        duplicate = True
                if not duplicate:
                    open.append(move)
            
            closed.append(current_state)
        
    if not solved: return []
    while current_state.parent is not None:
        path.append(current_state)
        current_state = current_state.parent
    path.append(starting_position)
    return path

def start_game() -> list:
    starting_position = [0,0,0,[],[]]         # size, depth, heuristic value, board, parent
    lines = read_file()
    size = int(lines[0][0]) 
    starting_position[0] = size
    board = []
    parent = []
    for row in range(size):
        temp = []
        for col in range(size):
            temp.append(Cell(lines[row+1][col], row, col))
        board.append(temp)

    starting_position[3] = board
    starting_position[4] = parent
    return starting_position

def read_file():
    file = open(gui.fileopenbox()).readlines()
    return [line.replace(" ", "").strip() for line in file]

def print_board(position:list):
    print_move(position[3]) # the board itself is stored at this index
    print(f'Size: {position[0]}|Depth: {position[1]}|Heuristic: {position[2]}')
        
def print_move(move:list):
    for row in move:
        for cell in row:
            print(cell.value, end="")
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

    print(f'Solved the puzzle in {total} seconds with {len(p)} moves')