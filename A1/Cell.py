class Cell:
    def __init__(self, value:str, row:int, col:int) -> None:
        self.value = value
        self.row = row
        self.col = col

    def __str__(self):
        return f'Value: {self.value}|Row:  {self.row}|Col: {self.col}'

    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __gt__(self, other):
        return self.value > other.value