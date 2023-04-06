import random

def LazorBoard(filename):
    '''
    This function reads in the contents of the .bff file and creates a representative board where each cell represents a position on the block
    and contains information about the block located there.
    '''
    # Split the contents of the file into lines
    with open(filename, 'r') as bff:
        lines = bff.readlines()
     
    # Create the board with a step size of a half block, so odd numbers are space between the blocks and even numbers are the actual block
    pre_board = []
    board = []
    for line in lines:
        line = line.strip()
        
        if line.startswith("GRID START"):
            continue
        elif line.startswith("GRID STOP"):
            break
        else:
            row = []
            for char in line:
                if char in ["o", "x", "A", "B", "C"]:
                    row.append(char)
                else:
                    row.append(" ")
            pre_board.append(row)
            
    rows = (len(pre_board) * 2) - 1
    index = 0
    for row in range(rows):
        if row == 0:
            board.append(pre_board[row])
            index += 1
        elif row % 2 == 0:
            board.append(pre_board[index])
            index += 1
        else:
            empty_row = [" "] * len(pre_board[0])
            board.append(empty_row) 
            
    return board

board = LazorBoard("yarn_5.bff")

def board_state(filename, board):
    '''
    This function stores the current state of the board as a 2D array, where each cell represents a position on the 
    board and contains information about the blocks located there.
    '''
    # Split the contents of the file into lines
    with open(filename, 'r') as bff:
        lines = bff.readlines()
    
    new_board = [row[:] for row in board]
    start_parsing = False
    
    for line in lines:
        line = line.strip()
        
        if line == "GRID STOP":
            start_parsing = True
            continue
            
        if start_parsing and (line.startswith("A") or line.startswith("B") or line.startswith("C")):
            # Parse the block type and amount
            block_type, amount = line[0], int(line[2])
            
            # Find the empty spots where blocks are allowed
            print(board)
            empty_spots = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == "o"]
            print(empty_spots)
            if len(empty_spots) < int(amount):
                raise ValueError(f"Warning: Not enough empty spots for {block_type}")
            
            # Add blocks to the board through random distribution
            random.shuffle(empty_spots)
            for i in range(amount):
                x, y = empty_spots[i]
                new_board[x][y] = block_type       
                
    return new_board

board_state("yarn_5.bff", board)

class Block:
    '''
    This class object to represent each block within the game. The block object contains information 
    about the block type (reflect, opaque, or refract), its position on the board and its orientation
    '''
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.block_type = block_type
        
    def get_position(self):
        '''
        Returns the current position of the block as a tuple (x, y)
        '''
        return (self.x, self.y)
    
    def set_position(self, x, y):
        '''
        Updates the position of the block to (x, y)
        '''
        self.x = x
        self.y = y
    
    def get_type(self):
        '''
        Returns the type of the block (reflect, opaque, or refract)
        '''
        return self.block_type
    
    def set_type(self, block_type):
        '''
        Updates the type of the block to block_type
        '''
        self.block_type = block_type
        
    def __str__(self):
        '''
        Returns a string representation of the block
        '''
        return f"Block at ({self.x}, {self.y}) of type '{self.block_type}'"