import random

class Board:
    '''
    This class object represents the game board, including its dimensions and the blocks, and lazors.
    '''
    def __init__(self, filename):
        '''
        Initializes a new Board object from a .bff file.
        '''
        self.filename = filename
        self.board = self.read_Board()
        self.lazors = self.get_lazors() 
        self.targets = self.get_targets()
    
    def read_Board(self):
        '''
        This function reads in the contents of the .bff file and creates a representative board where each cell represents a position on the 
        block and contains information about the block located there.
        '''
        # Split the contents of the file into lines
        with open(self.filename, 'r') as bff:
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

    def board_state(self):
        '''
        This function stores the current state of the board as a 2D array, where each cell represents a position on the 
        board and contains information about the blocks located there.
        '''
        # Split the contents of the file into lines
        with open(self.filename, 'r') as bff:
            lines = bff.readlines()

        # Cope the board to a new list to not modify the original board
        new_board = [row[:] for row in self.board]
        
        # Flag to start parsing the blocks in the file
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
                empty_spots = [(i, j) for i in range(len(self.board)) for j in range(len(self.board[0])) if self.board[i][j] == "o"]
                if len(empty_spots) < int(amount):
                    raise ValueError(f"Warning: Not enough empty spots for {block_type}")

                # Add blocks to the board through random distribution
                random.shuffle(empty_spots)
                for i in range(amount):
                    x, y = empty_spots[i]
                    new_board[x][y] = block_type       

        # Adding blanks around the board to ensure block positions are correct
        empty_row = [" "] * (len(self.board[0])+2) 
        new_board = [empty_row] + [[" "] + row + [" "] for row in new_board] + [empty_row]
         
        return new_board
    
    def get_lazors(self):
        '''
        This function reads in the contents of the .bff file and creates a list of lazors that exist on the board, with their starting 
        position and velocity.
        '''
        with open(self.filename, 'r') as bff:
            lines = bff.readlines()

        lazors = []

        for line in lines:
            line = line.strip()

            if line.startswith("L "):
                # Parse the lazor information
                data = line[2:].split(" ")
                x, y, vx, vy = [int(i) for i in data]

                # Create a dictionary to represent the lazor
                lazor = {
                    "Laser position": [x, y],
                    "Laser velocity": [vx, vy]
                }

                lazors.append(lazor)

        return lazors
    
    def get_targets(self):
        '''
        This function reads in the contents of the .bff file and creates a list of target positions we need the lazers to intersect
        '''
        with open(self.filename, 'r') as bff:
            lines = bff.readlines()

        targets = []

        for line in lines:
            line = line.strip()

            if line.startswith("P "):
                # Parse the lazor information
                data = line[2:].split(" ")
                x, y = [int(i) for i in data]

                # Create a dictionary to represent the lazor
                target = {
                    "Target position": [x, y],
                }

                targets.append(target)

        return targets
    
if __name__ == "__main__":    
    board = Board("dark_1.bff")
    curr_board = board.board_state()
    lazors = board.lazors
    targets = board.targets
    print(curr_board)
    print(lazors)
    print(targets)

    