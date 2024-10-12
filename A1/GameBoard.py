import easygui as gui

class Cell:
    def __init__(self, value:str, row:int, col:int) -> None:
        self.value = value
        self.row = row
        self.col = col

class GameBoard:
    def __init__(self) -> None:
        self.depth = 0
        self.heuristic = 0
        lines = self.read_file()
        self.size = int(lines[0][0])
        self.board = []
        self.parent = None
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

    def __lt__(self, other):
        return self.depth < other.depth
    
    def __eq__(self, other) -> bool:
        row = 0
        col = 0
        for i in self.board:
            for cell in i:
                if cell.value != other.board[row][col].value: return False
                col += 1
            row += 1
            col = 0
        return True
    
    def __ne__(self, other):
        row = 0
        col = 0
        for i in self.board:
            for cell in i:
                if cell.value != other.board[row][col].value: return True
                col += 1
            row += 1
            col = 0
        return False