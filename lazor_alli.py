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

def Lazer_paths(filename,board_state,lazors):
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

    # with open(filename, 'r') as bff:
    #     lines = bff.readlines()
    
    # start_points = []
    # for line in lines:
    #     line = line.strip()
        
    #     if line.startswith("L"):
    #         data = line[2:].split(" ")
    #         start_point = [int(i) for i in data]
    #     else:   # Why are these 'else' lines neccessary?
    #         continue
    #     start_points.append(start_point)
        # print(start_points)        
    
    # start_points =[[4,5,-1,-1]]
    start_points = lazors
    # print("start_points1:",start_points) 
    
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
                    
        # print("start_points2:",start_points)                    
    return lazer_paths

#Lazer_Paths = Lazer_paths("yarn_5.bff", board_state)                   
                
def target_point_chk(filename, lazer_paths, targets): # Not done yet...
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
    # with open(filename, 'r') as bff:
    #     lines = bff.readlines()
    
    # target_points = []
    # for line1 in lines:
    #     line1 = line1.strip()
        
    #     if line1.startswith("P"):
    #         target_point = (int(line1[2]),int(line1[4]))
    #     else:   # Why are these 'else' lines neccessary?
    #         continue
        
    #     target_points.append(target_point)
               
    #print(target_points)
    
    # #lazer_paths = [[(6,9)],[(9,2)]]
    # lazer_paths = [[(1,2),(5,4)], [(6,3)]]
    target_points = targets
    
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
    board = Board(filename)

# curr_board = board_state(filename, board)
# # curr_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'A', ' ', 'o', ' ', 'A', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'o', ' ', 'o', ' ', 'o', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'A', ' ', 'C', ' ', 'o', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
# lazer_paths = Lazer_paths(filename, curr_board)
# flag = target_point_chk(filename, lazer_paths)

    iteration = 0
    result = True
    while result:
        # starting_points = []
        curr_board = board.get_board()
        # print(curr_board)
        starting_points = board.get_lazors()
        # print("lazors:",lazors)
        target_points = board.get_targets()
        print(target_points)
        lazer_paths = Lazer_paths(filename, curr_board, starting_points)
        # print(lazer_paths)
        result = target_point_chk(filename, lazer_paths, target_points)
        iteration += 1
        print(iteration)
        
    filename = filename.split('.')[0]    
    with open(filename +'_answer.txt', 'w') as answer_file:
            
        for list in curr_board:
            for i in list:
                answer_file.write(i)
            answer_file.write('\n')
            
    return curr_board

    
if __name__ == "__main__":    
    # board = Board("tiny_5.bff")
    # curr_board = board.board_state()
    # lazors = board.lazors
    # print("lazors2:",lazors)
    # targets = board.targets
    
    answer = Lazor_solution("mad_7.bff")
    
    # print(curr_board)
    # print(lazors)
    # print(targets)

    