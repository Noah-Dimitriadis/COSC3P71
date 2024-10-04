import easygui as gui

class Cell:
    def __init__(self, value:str, x:int, y:int) -> None:
        self.value = value
        self.x = x
        self.y = y

class GameBoard:
    def __init__(self) -> None:
        lines = self.read_file()
        self.size = int(lines[0][0])
        self.board = []
        for row in range(self.size):
            temp = []
            for col in range(self.size):
                temp.append(Cell(lines[row+1][col], row, col))
            self.board.append(temp)

    def read_file(self):
        file = open(gui.fileopenbox()).readlines()
        return [line.replace(" ", "").strip() for line in file]
    
    def print_board(self):
        for row in self.board:
            for cell in row:
                print(cell.value, end="")
            print()

    def find_empty(self) -> Cell:
        for row in self.board:
            for cell in row:
                if cell.value == 'X': return cell

    def generate_moves(self):
        empty_cell = self.find_empty()
        # move up down left right
        # determine cells to be swapped with empty cells values
        # pass in copies of the board and create dummy cells to do so

        pass

    def move(self, cell1:Cell, cell2:Cell):
        if cell1.value == 'X' or cell2.value == 'X':
            temp = cell1.value
            cell1.value = cell2.value
            cell2.value = temp
        else:
            print('invalid move')

    def is_solved(self) -> bool:
        count = 1           # index 1 has the number 1
        for row in self.board:
            for cell in row:
                if cell.value == 'X':
                    if count == 9: return True
                    else: return False
                if int(cell.value) != count: return False
                count += 1
        return True

    def heuristic_class_1(self) -> int:
        # Heuristic from class -> # of tiles in the wrong spot
        current = 1
        count = 0
        for row in self.board:
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

if __name__ == "__main__":
    gb = GameBoard()
    gb.print_board()