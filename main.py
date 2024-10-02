import easygui as gui

class Cell:
    def __init__(self, value:int, x:int, y:int) -> None:
        self.value = value
        self.x = x
        self.y = y

class GameBoard:
    def __init__(self) -> None:
        lines = self.read_file()
        self.size = int(lines[0][0])
        self.board = [[lines[row+1][col] for col in range(self.size)] for row in range(self.size)]      # +1 to skip the header row

    def read_file(self):
        file = open(gui.fileopenbox()).readlines()
        return [line.replace(" ", "").strip() for line in file]
    
    def move(self):
        # a = self.board[ax][ay]
        # b = self.board[bx][by]
        # self.board[bx][by] = a
        # self.board[ax][ay] = b
        
        # if one of the indices we are swapping is the X we are good if it isnt then the move is illegal
        pass

    def is_solved(self) -> bool:
        count = 1
        for line in self.board:
            for item in line:
                if item == 'X':
                    if count == 9: return True
                    else: return False
                if int(item) != count: return False
                count += 1
        return True


if __name__ == "__main__":
    gb = GameBoard()
    print(gb.is_solved())
