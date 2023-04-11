# Lazor-Project
This is a Python program that solves the Lazors puzzle. The program reads a .bff file that contains the game board, blocks, lazors, and targets. It then outputs the solution to the puzzle.
## Requirements
- Python 3.9
## Usage
To use this program, clone this repository and navigate to the lazor_project.
Next, run the programm with the name of the .bff file as an argument:
## Features
 - Reads in the contents of a .bff file to generate the game board, blocks, lazors and targets
 - Finds the solution by iterating over randomly generated game boards based on block assignments
 - Outputs the solutions in a text file showinf the correct position of each block
 ## Code Overview 
 The program consists of the following segments:
 - class Board: This class object represents the game board, the blocks on the board, the lazors and targets.
 - __init__ function: Initializes a new Board object from a .bff file
 - get_board function: This function reads in the contents of the .bff file and creates a corresponding board via randome distribution of the assigned blocks
 - get_lazors function: This function reads in the contents of the .bff file and creates a list of lazors that exist on the board, with their starting position and velocity
 - get_targets function: This function reads in the contents of the .bff file and identifies the targets the lazors must pass through to solve the game.
 - pt_chk function:
 - Lazer_paths function:
 - target_point_chk function:
 - lazor_solution function:
