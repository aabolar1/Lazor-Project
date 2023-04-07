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
        
        if line.startswith("L"):
            lazor_point
            
            
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
            empty_spots = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == "o"]
            if len(empty_spots) < int(amount):
                raise ValueError(f"Warning: Not enough empty spots for {block_type}")
            
            # Add blocks to the board through random distribution
            random.shuffle(empty_spots)
            for i in range(amount):
                x, y = empty_spots[i]
                new_board[x][y] = block_type       
                
    return new_board

board_state = board_state("yarn_5.bff", board)

# Adding blanks around the board (Temporary, can be added to the board_state function)
empty_row = [" "] * (len(board[0])+2)
for list in board_state:
    list.insert(0," ")
    list.append(" ")
board_state.insert(0,empty_row)
board_state.append(empty_row)
board_state[3][5] = "C"

def pt_chk(x, y, board_state):
    '''
    Validate if the coordinates specified (x and y) are out of the boundaries of the board.

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the maze.
        y: *int*
            A y coordinate to check if it resides within the maze.
        board_state: *list of lists*
            The board we are looking into?

    **Returns**

        valid: *bool*
            Whether the coordiantes are out of bound (True) or not (False).
    '''
    return (x < 0 or x >= len(board_state[0])) or (y < 0 or y >= len(board_state))

def Lazer_paths(filename,board_state):
    '''
    
    Parameters
    ----------
    filename : TYPE
        DESCRIPTION.
    board_state : TYPE
        DESCRIPTION.

    Returns
    -------
    lazer_paths : *List of Lists*
        All points the laser passes through.

    '''

    with open(filename, 'r') as bff:
        lines = bff.readlines()
    
    start_points = []
    for line1 in lines:
        line1 = line1.strip()
        
        if line1.startswith("L"):
            start_point = [line1[2],line1[4],line1[6],line1[8]]
            start_point = [int(i) for i in start_point]
        else:   # Why are these 'else' lines neccessary?
            continue
        
        start_points.append(start_point)        
    
    #start_points.append([4,2,1,1])  
    lazer_paths = []      
    for list in start_points:
        lazer_path = [(list[0],list[1])]
        lazer_direction = [(list[2],list[3])]
        
        end_flag = 0
        while end_flag == 0:
            current_pt = lazer_path[-1]
            current_dir = lazer_direction[-1]
            
            if current_pt[0]%2 == 0:
                inv_pt1 = (current_pt[0]+current_dir[0],current_pt[1]) # Investigating point 1: board location the lazer or pointing towards
                #print(board_state[inv_pt1[1]][inv_pt1[0]])
                if pt_chk(inv_pt1[0], inv_pt1[1], board_state):
                    lazer_paths.append(lazer_path)
                    break 
                elif board_state[inv_pt1[1]][inv_pt1[0]] == "B":
                    lazer_paths.append(lazer_path)
                    break
                elif board_state[inv_pt1[1]][inv_pt1[0]] == "o" or board_state[inv_pt1[1]][inv_pt1[0]] == "x":
                    lazer_direction.append(current_dir)
                    lazer_path.append((current_pt[0]+current_dir[0], current_pt[1]+current_dir[1]))
                else: # If block is "A" or "C"
                    
                    if board_state[inv_pt1[1]][inv_pt1[0]] == "C":
                        start_points.append([list[0]+list[2],list[1]+list[3],list[2],list[3]])
                        
                    inv_pt2 = (current_pt[0]-current_dir[0],current_pt[1]) # Investigating point 2: board location next to the investigating point
                    if pt_chk(inv_pt2[0], inv_pt2[1], board_state):
                        lazer_paths.append(lazer_path)
                        break
                    elif board_state[inv_pt2[1]][inv_pt2[0]] == "A" or board_state[inv_pt2[1]][inv_pt2[0]] == "B":
                        lazer_paths.append(lazer_path)
                        break
                    else:
                        lazer_direction.append((-current_dir[0], current_dir[1]))
                        lazer_path.append((current_pt[0]-current_dir[0], current_pt[1]+current_dir[1]))
            else:
                inv_pt1 = (current_pt[0],current_pt[1]+current_dir[1]) # Investigating point 1: board location the lazer or pointing towards
                #print(board_state[inv_pt1[1]][inv_pt1[0]])
                if pt_chk(inv_pt1[0], inv_pt1[1], board_state):
                    lazer_paths.append(lazer_path)
                    break 
                elif board_state[inv_pt1[1]][inv_pt1[0]] == "B":
                    lazer_paths.append(lazer_path)
                    break
                elif board_state[inv_pt1[1]][inv_pt1[0]] == "o" or board_state[inv_pt1[1]][inv_pt1[0]] == "x":
                    lazer_direction.append(current_dir)
                    lazer_path.append((current_pt[0]+current_dir[0], current_pt[1]+current_dir[1]))
                else: # If block is "A" or "C"
                    
                    if board_state[inv_pt1[1]][inv_pt1[0]] == "C":
                        start_points.append([current_pt[0] + current_dir[0], current_pt[1] + current_dir[1], current_dir[0], current_dir[1]])
                        
                    inv_pt2 = (current_pt[0],current_pt[1]-current_dir[1]) # Investigating point 2: board location next to the investigating point
                    if pt_chk(inv_pt2[0], inv_pt2[1], board_state):
                        lazer_paths.append(lazer_path)
                        break
                    elif board_state[inv_pt2[1]][inv_pt2[0]] == "A" or board_state[inv_pt2[1]][inv_pt2[0]] == "B":
                        lazer_paths.append(lazer_path)
                        break
                    else:
                        lazer_direction.append((current_dir[0], -current_dir[1]))
                        lazer_path.append((current_pt[0]+current_dir[0], current_pt[1]-current_dir[1]))
                
    return lazer_paths

Lazer_Paths = Lazer_paths("yarn_5.bff", board_state)                   
                
def target_point_chk(filename, lazer_paths): # Not done yet...
    '''
    A function to check if the laser path goes through the target points
    
    Parameters
    ----------
    filename : TYPE
        DESCRIPTION.
    lazer_paths : TYPE
        DESCRIPTION.

    Returns
    -------
    target_points : TYPE
        DESCRIPTION.

    '''
    with open(filename, 'r') as bff:
        lines = bff.readlines()
    
    target_points = []
    for line1 in lines:
        line1 = line1.strip()
        
        if line1.startswith("P"):
            target_point = (int(line1[2]),int(line1[4]))
        else:   # Why are these 'else' lines neccessary?
            continue
        
        target_points.append(target_point)
    return target_points

T = target_point_chk("yarn_5.bff",Lazer_Paths)





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
    