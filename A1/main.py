from GameBoard import GameBoard,Cell
from queue import PriorityQueue
from copy import deepcopy
import time

'''
TODO remove gameboard class dependency
TODO optimise pq insertion in a_star
TODO optimise move generation and compare with closed list in generate function?
TODO implement other heurstics and create heuristic selection functionality

'''

def generate_moves(board:GameBoard) -> list[GameBoard]:
    empty_cell = find_empty(board)
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
        copy = deepcopy(board)

        row = move_coordinates[i]
        col = move_coordinates[i+1]
        if row < copy.size and row >= 0 and col < copy.size and col >= 0:     # if move is legal
            temp = copy.board[row][col].value
            copy.board[row][col].value = copy.board[empty_cell.row][empty_cell.col].value
            copy.board[empty_cell.row][empty_cell.col].value = temp
            if board.parent is None or copy != board.parent:
                copy.parent = board
                copy.depth = board.depth + 1
                all_moves.append(copy)
           
    return all_moves

def is_solved(board:GameBoard) -> bool:
    count = 1           # index 1 has the number 1
    for row in board.board:
        for cell in row:
            if cell.value == 'X':
                if count == 9: return True
                else: return False
            if int(cell.value) != count: return False
            count += 1
    return True

def find_empty(board:GameBoard) -> Cell:
        for row in board.board:
            for cell in row:
                if cell.value == 'X': return cell

def heuristic_class_1(board:GameBoard) -> int:
    # Heuristic from class -> # of tiles in the wrong spot
    current = 1
    count = 0
    for row in board.board:
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

def a_star(starting_position:GameBoard) -> list[GameBoard]:
    solved = False
    path = []
    open = PriorityQueue()
    closed = []

    open.put((heuristic_class_1(starting_position), starting_position))
    current_state = None
    while open:
        current_state = open.get()[1]

        if is_solved(current_state): 
            solved = True
            break

        if current_state.depth == 50: break
        moves = generate_moves(current_state)
        for move in moves:
            duplicate = False
            for closed_move in closed:
                if move == closed_move:
                    duplicate = True
            if not duplicate:
                move.heuristic = current_state.depth + heuristic_class_1(move)
                open.put((move.heuristic, move))
        closed.append(current_state)

    if not solved: return []
    while current_state.parent is not None:
        path.append(current_state)
        current_state = current_state.parent
    path.append(starting_position)

    return path

def DFS(starting_position:GameBoard, max:int) -> list[GameBoard]:
    solved = False
    path = []
    closed = []
    open = []

    current_state:GameBoard
    
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
    return pat


if __name__ == "__main__":
    gb = GameBoard()
    start =  time.time()
    p = a_star(gb)
    end = time.time()
    total = end-start
    if len(p) > 0:
        p.reverse()
        print('solution found. printing path:')
    for step in p:
        step.print_board()
        print(step.depth)
        print()
    if len(p) > 0:
        print(f'Solution in {max(step.depth for step in p)} moves')        # minus initial state

    print(f'It took {total} seconds to solve')