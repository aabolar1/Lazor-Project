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
        parse = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("GRID STOP"):
                parse = True
                continue
            if parse:
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
            
        return [(int(x), int(y)) for line in lines if not line.startswith("#") and line.startswith("P ") for x, y in [line.strip()[2:].split(" ")]]

def pt_chk(x, y, board_state):
    
    '''
    Check if the coordinates specified (x and y) are out of the boundaries of the board.

    Parameters
    ----------
    x: *int*
        An x coordinate to check if it resides ouside the board.
    y: *int*
        A y coordinate to check if it resides outside the board.
    board_state: *list of lists*
        The board we are looking into?

    Returns
    -------
        *bool*
            Whether the coordiantes are out of bound (True) or not (False).
    '''
    return (x < 0 or x >= len(board_state[0])) or (y < 0 or y >= len(board_state))

def Lazer_paths(filename,board_state,start_points):
    '''
    Determines the laser path(s) for the given board state (block configuration on the board).
    
    Parameters
    ----------
    filename : *str*
        Name of board file.
    board_state : *List of Lists*
        Board state with blocks positioned.
    lazors: *list of lists*
        All laser starting points (their coordinates and their vectors).

    Returns
    -------
    lazer_paths : *list of lists*
        All points the laser passes through.

    '''    
    lazer_paths = []      
    for list in start_points:
        lazer_path = [(list[0],list[1])]
        lazer_direction = [(list[2],list[3])]
        
        end_flag = 0
        while end_flag == 0:
            current_pt = lazer_path[-1] # Current laser point in laser path.
            current_dir = lazer_direction[-1] # Current laser point direction is laser path.
            
            if current_pt[0]%2 == 0: 
            # When lazer is in the vertical intersection of boards, investigate the board left and right the lazer points.
                inv_pt1 = (current_pt[0]+current_dir[0],current_pt[1]) # Investigating point 1: board location the lazer or pointing towards.
                inv_pt2 = (current_pt[0]-current_dir[0],current_pt[1]) # Investigating point 2: board location next to the investigating point.
                reflected_dir = (-current_dir[0], current_dir[1])
            else: 
            # When lazer is in the horizontal intersection of boards, investigate the board above and below the lazer points.
                inv_pt1 = (current_pt[0],current_pt[1]+current_dir[1]) # Investigating point 1: board location the lazer or pointing towards.
                inv_pt2 = (current_pt[0],current_pt[1]-current_dir[1]) # Investigating point 2: board location next to the investigating point.
                reflected_dir = (current_dir[0], -current_dir[1])    
           
            if pt_chk(inv_pt1[0], inv_pt1[1], board_state): 
            # When investing position 1 is out of the board region, append current laser path to laser paths list and end path.
                lazer_paths.append(lazer_path)
                break 
            elif board_state[inv_pt1[1]][inv_pt1[0]] == "B": 
            # When investing position 1 is an opaque block (B), append current laser path to laser paths list and end path. 
                lazer_paths.append(lazer_path)
                break
            elif board_state[inv_pt1[1]][inv_pt1[0]] == "o" or board_state[inv_pt1[1]][inv_pt1[0]] == "x": 
            # When investigating position 1 is either an available (o) or unavailable blank (x)
                lazer_direction.append(current_dir) # Next laser point would have the same direction.
                lazer_path.append((current_pt[0]+current_dir[0], current_pt[1]+current_dir[1])) # Next laser point position.
            else: # When investigating position 1 has either a reflective (A) of refractive (C) block
                
                if board_state[inv_pt1[1]][inv_pt1[0]] == "C":
                # When investigating position is a refractive block (C), create a new start point as a new laser path branch is formed.
                # The new starting point would be the next position in the current direction with the direction inchanged.
                    start_points.append([current_pt[0] + current_dir[0], current_pt[1] + current_dir[1], current_dir[0], current_dir[1]])
                    
                if pt_chk(inv_pt2[0], inv_pt2[1], board_state):
                # When investigating position 2 is out of the board region, append current laser path to laser paths list and end path.
                    lazer_paths.append(lazer_path)
                    break
                elif board_state[inv_pt2[1]][inv_pt2[0]] == "A" or board_state[inv_pt2[1]][inv_pt2[0]] == "B":
                # When investigating position 2 has either a reflective (A) or an opaque (B) block, append current laser path to laser paths list and end path.
                    lazer_paths.append(lazer_path)
                    break
                else: 
                # When investigating position 2 either is blank (o or x) or a refractive (C) block
                    lazer_direction.append(reflected_dir) # Next laser point would have the reflected direction.
                    lazer_path.append((current_pt[0]+lazer_direction[-1][0], current_pt[1]+lazer_direction[-1][1])) # Next laser point position.
                    
    return lazer_paths                   
                
def target_pt_chk(filename, lazer_paths, target_points):
    '''
    A function to check if the laser path(s) goes through the target points
    
    Parameters
    ----------
    filename : *str*
        Name of board file.
    lazer_paths : *list of lists*
        Laser path(s) to be checked.
    target_points : *list of tuples*
        Target points to be checked if they are all included in the laser path(s).
    
    Returns
    -------
    not result : *bool*
        False: If all targets points are included in the laser path(s).
        True: If any one of the targets are not included in the lase path(s).
        
    '''
    lazer_pts =[]
    for list in lazer_paths:
        for tuple in list:
            lazer_pts.append(tuple)
           
    result = all(tuple in lazer_pts for tuple in target_points)
    
    return  not result

def Lazor_solver(filename):
    '''
    Solves the Lazor game of the given board format with 'filename'.
    
    Parameters
    ----------
    filename : *str*
        Name of board file.

    Returns
    -------
    curr_board : *list of lists*
        The answer board state with the configured blocks.
    "board_name"+"_answer.txt": Saves the answer in a text file.

    '''
    board = Board(filename)
    target_points = board.get_targets()

    iteration = 0
    result = True 
    while result: # Result will be changed to false when the answer board is found and the while loop ends.
        curr_board = board.get_board()
        starting_points = board.get_lazors()
        lazer_paths = Lazer_paths(filename, curr_board, starting_points)
        result = target_pt_chk(filename, lazer_paths, target_points)
        iteration += 1
        # print(iteration)
        
    filename = filename.split('.')[0]    
    with open(filename +'_answer.txt', 'w') as answer_file:           
        for list in curr_board:
            for i in list:
                answer_file.write(i)
            answer_file.write('\n')           
    return curr_board

    
if __name__ == "__main__":     
    answer = Lazor_solver("yarn_4.bff")

    