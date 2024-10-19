'''
Noah Dimitriadis
Student number: 7558224
Email: nd22zr@brocku.ca

This is a very basic cell class I made so I could easily grab the row and column numbers of a value
'''
class Cell:
    def __init__(self, value:str, row:int, col:int) -> None:
        self.value = value
        self.row = row
        self.col = col

    def __str__(self):      # to make printing when debugging easier
        return f'Value: {self.value}|Row:  {self.row}|Col: {self.col}'

    # The following functions I had to implement for the PriorityQueue class as it had no way of comparing the gameboard lists otherwise

    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __gt__(self, other):
        return self.value > other.value