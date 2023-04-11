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

#board = LazorBoard("yarn_5.bff")

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
                
    # Adding blanks around the board (Temporary, can be added to the board_state function)            
    empty_row = [" "] * (len(board[0])+2)
    for list in new_board:
        list.insert(0," ")
        list.append(" ")
    new_board.insert(0,empty_row)
    new_board.append(empty_row)
    #board_state[3][5] = "C"
            
    return new_board

#board_state = board_state("yarn_5.bff", board)

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
    for line in lines:
        line = line.strip()
        
        if line.startswith("L"):
            data = line[2:].split(" ")
            start_point = [int(i) for i in data]
        else:   # Why are these 'else' lines neccessary?
            continue
        start_points.append(start_point)
        print(start_points)        
    
    #start_points.append([4,2,1,1])  
    lazer_paths = []      
    for list in start_points:
        lazer_path = [(list[0],list[1])]
        lazer_direction = [(list[2],list[3])]
        
        end_flag = 0
        while end_flag == 0:
            current_pt = lazer_path[-1]
            current_dir = lazer_direction[-1]
            
            if current_pt[0]%2 == 0: # When lazer is in the vertical intersection of boards, investigate the board left and right the lazer points
                inv_pt1 = (current_pt[0]+current_dir[0],current_pt[1]) # Investigating point 1: board location the lazer or pointing towards
                inv_pt2 = (current_pt[0]-current_dir[0],current_pt[1]) # Investigating point 2: board location next to the investigating point
                reflected_dir = (-current_dir[0], current_dir[1])
            else: # When lazer is in the horizontal intersection of boards, investigate the board above and below the lazer points
                inv_pt1 = (current_pt[0],current_pt[1]+current_dir[1]) # Investigating point 1: board location the lazer or pointing towards
                inv_pt2 = (current_pt[0],current_pt[1]-current_dir[1]) # Investigating point 2: board location next to the investigating point
                reflected_dir = (current_dir[0], -current_dir[1])    
           
            if pt_chk(inv_pt1[0], inv_pt1[1], board_state): # When investing positions is out of the board region
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
                    
                if pt_chk(inv_pt2[0], inv_pt2[1], board_state):
                    lazer_paths.append(lazer_path)
                    break
                elif board_state[inv_pt2[1]][inv_pt2[0]] == "A" or board_state[inv_pt2[1]][inv_pt2[0]] == "B":
                    lazer_paths.append(lazer_path)
                    break
                else: # "o" or "x" or "C"
                    lazer_direction.append(reflected_dir)
                    lazer_path.append((current_pt[0]+lazer_direction[-1][0], current_pt[1]+lazer_direction[-1][1]))
     
    return lazer_paths

#Lazer_Paths = Lazer_paths("yarn_5.bff", board_state)                   
                
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
               
    #print(target_points)
    
    # #lazer_paths = [[(6,9)],[(9,2)]]
    # lazer_paths = [[(1,2),(5,4)], [(6,3)]]
    
    lazer_pts =[]
    for list in lazer_paths:
        for tuple in list:
            lazer_pts.append(tuple)
    #print(lazer_pts)        
    result = all(tuple in lazer_pts for tuple in target_points)
    
    #print(result)   
    return  not result

# board = LazorBoard("yarn_5.bff")
# board_state = board_state("yarn_5.bff", board)
# Lazer_Paths = Lazer_paths("yarn_5.bff", board_state)
# result = target_point_chk("yarn_5.bff",Lazer_Paths)

def Lazor_solution(filename):

    # filename = "yarn_5.bff"
    board = LazorBoard(filename)

# curr_board = board_state(filename, board)
# # curr_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'A', ' ', 'o', ' ', 'A', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'o', ' ', 'o', ' ', 'o', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'A', ' ', 'C', ' ', 'o', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
# lazer_paths = Lazer_paths(filename, curr_board)
# flag = target_point_chk(filename, lazer_paths)

    iteration = 0
    result = True
    while result:
        curr_board = board_state(filename, board) # board is coming out eith missing blocks
        lazer_paths = Lazer_paths(filename, curr_board)
        result = target_point_chk(filename, lazer_paths)
        iteration += 1
        print(iteration)
        
    with open(filename +'_answer.txt', 'w') as answer_file:
            
        for list in curr_board:
            for i in list:
                answer_file.write(i)
            answer_file.write('\n')
    return curr_board

answer = Lazor_solution("tiny_5.bff")


    
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
    