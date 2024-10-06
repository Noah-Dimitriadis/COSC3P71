from GameBoard import GameBoard
from queue import PriorityQueue
from copy import deepcopy

def generate_moves(board:GameBoard) -> list[GameBoard]:
    empty_cell = board.find_empty()
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
            temp = copy.board[row][col]
            copy.board[row][col] = copy.board[empty_cell.row][empty_cell.col]
            copy.board[empty_cell.row][empty_cell.col] = temp
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
    
def heuristic_class_2(self) -> int:
    # Heuristic from class -> manhattan distance

    

    pass

def heuristic_self(self) -> int:
    # Heuristic not covered in class TBD

    pass

def a_star(initial_board:GameBoard) -> list[GameBoard]:
    path = []
    pq = PriorityQueue()

    pq.put((heuristic_class_1(initial_board), initial_board))
    current = None
    while pq:
        current = pq.get()
        current[1].print_board()
        print(f'Current depth: {current[1].depth}')
        if current[1].depth == 5: break
        if is_solved(current[1]): break
        current_moves = generate_moves(current[1])
        for move in current_moves:
            
            heuristic = move.depth + heuristic_class_1(move)
            move.heuristic = heuristic

            pq.put((heuristic, move))

    curr = current[1]
    while curr.parent is not None:
        path.append(curr)
        curr = curr.parent
    
    path.append(curr)
    return path

if __name__ == "__main__":
    gb = GameBoard()
    
    # for move in generate_moves(gb):
    #     move.print_board()

    path = a_star(gb)

    # count = 0
    # for p in path:
    #     if count == 25: break
    #     p.print_board()
    #     print()
    #     count += 1