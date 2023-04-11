import random

class Board:
    '''
    This class object represents the game board, the blocks on the board, the lazors and targets.
    '''
    def __init__(self, filename):
        '''
        Initializes a new Board object from a .bff file.
        '''
        self.filename = filename
        self.board = self.get_board() # call get_board method to create game board
        self.lazors = self.get_lazors() # call get_lazors method to create lazor list
        self.targets = self.get_targets() # call get_targets method to create target list

    def get_board(self):
        '''
        This function reads in the contents of the .bff file and creates a representative board where each 
        cell represents a position on the block and contains relevant information
        '''
        # Split the contents of the bff file into lines
        with open(self.filename, 'r') as bff:
            lines = bff.readlines()

        # Parse through the bff and create the board, blocks are on even indices.
        board = []
        parse = False
        for line in lines:
            line = line.strip()

            if line.startswith("GRID START"):
                parse = True
                continue 
            elif line.startswith("GRID STOP"):
                break
                
            if parse:
                row = []
                for char in line:
                    if char in ["o", "x", "A", "B", "C"]:
                        row.append(char)
                    else:
                        row.append(" ")
                board.append(row)
                board.append([" "] * len(row))
        
        # Remove the last blank row that was appeneded   
        board.pop()
        
        # Modify the board based on the blocks specified in the file
        start_parsing = False   

        for line in lines:
            line = line.strip()

            if line.startswith(("A", "B", "C")):
                # Parse the block type and amount
                block_type, amount = line[0], int(line[2])

                # Find the empty spots where blocks are allowed
                empty_spots = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == "o"]
                if len(empty_spots) < int(amount):
                    raise ValueError(f"Warning: Not enough empty spots for {block_type}")

                # Add blocks to the board through random distribution
                random.shuffle(empty_spots)
                for i in range(amount):
                    x, y = empty_spots[i]
                    board[x][y] = block_type       

        # Adding blanks around the board to ensure block positions are correct
        empty_row = [" "] * (len(board[0])+2) 
        new_board = [empty_row] + [[" "] + row + [" "] for row in board] + [empty_row]
         
        return new_board
    
    def get_lazors(self):
        '''
        This function reads in the contents of the .bff file and creates a list of lazors that exist on the board, with their starting 
        position and velocity.
        '''
        lazors = []
        with open(self.filename, 'r') as bff:
            for line in bff:
                line = line.strip()
                if line.startswith("L"):
                    # Parse the lazor information
                    x, y, vx, vy = map(int, line[2:].split())
                    lazors.append([x, y, vx, vy])

        return lazors
    
    def get_targets(self):
        '''
        This function reads in the contents of the .bff file and creates a list of target positions we need the lazers to intersect
        '''
        with open(self.filename, 'r') as bff:
            lines = bff.readlines()
            
        return [[int(x), int(y)] for line in lines if not line.startswith("#") and line.startswith("P ") for x, y in [line.strip()[2:].split(" ")]]

if __name__ == '__main__':
    board = Board("mad_1.bff")
    game_board = board.board
    lazor = board.lazors
    targets = board.targets
    print(game_board)
    print(lazor)
    print(targets)