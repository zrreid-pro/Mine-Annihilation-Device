#This file holds the implementation of the Minesweeper game
import random as rand
import numpy as np


class Minefield:

    def __init__(self, difficulty):
        """This is a class of Minefield to be solved by our AI.

        It takes the desired difficulty of the game as an integer.
        Difficulty options are given as integers with the following meaning:
            1: Beginner(9*9 field with 10 mines)
            2: Intermediate(16*16 field with 40 mines)
            3: Expert(24*24 field with 99 mines)
        """
        self.solver = None
        self.difficulty = difficulty
        self.game_over = False
        self.size = 0
        self.mine_total = 0
        if difficulty == 1:
            self.size = 9
            self.mine_total = 10
        elif difficulty == 2:
            self.size = 16
            self.mine_total = 40
        else:
            self.size = 24
            self.mine_total = 99
        #self.field = np.zeros((self.size, self.size), dtype=str)
        self.field = np.zeros((self.size, self.size), dtype=int)
        #self.player_field = np.full((self.size, self.size), "*", dtype=str)
        self.working_field = np.zeros((self.size, self.size), dtype=int)

        #self.cell_total = self.size**2
        self.field_dict = {}

        self.mine_list = set([])

        self.fill_minefield()


        pass

    #cell value (row, column) = [visited, probabilityOfMine]
    #currently is: cell value (row, column) = visited
    #cell value legend:
        #0 = empty
        #-1 = mine
        #1-8 = numbered cell
        #9 = flagged cell
    def fill_minefield(self):
        #For the dictionary parts
        for i in range(self.size):
            for j in range(self.size):
                self.field_dict[(i,j)] = False
        
        #self.mine_list.add((0,3))
        #self.field[0][3] = -1
        #self.add_dangerous_neighbor((0,3))
        #self.mine_list.add((1,3))
        #self.field[1][3] = -1
        #self.add_dangerous_neighbor((1,3))
        #self.mine_list.add((2,3))
        #self.field[2][3] = -1
        #self.add_dangerous_neighbor((2,3))
        #self.mine_list.add((3,3))
        #self.field[3][3] = -1
        #self.add_dangerous_neighbor((3,3))
        #self.mine_list.add((3,0))
        #self.field[3][0] = -1
        #self.add_dangerous_neighbor((3,0))
        #self.mine_list.add((3,1))
        #self.field[3][1] = -1
        #self.add_dangerous_neighbor((3,1))
        #self.mine_list.add((3,2))
        #self.field[3][2] = -1
        #self.add_dangerous_neighbor((3,2))

        #self.mine_list.add((3,4))
        #self.field[3][4] = -1
        #self.add_dangerous_neighbor((3,4))
        #self.mine_list.add((4,3))
        #self.field[4][3] = -1
        #self.add_dangerous_neighbor((4,3))
        #self.mine_list.add((4,4))
        #self.field[4][4] = -1
        #self.add_dangerous_neighbor((4,4))

        row = 0
        col = 0
        i = 0
        
        while i < self.mine_total:
            row = rand.randint(0, self.size-1)
            col = rand.randint(0, self.size-1)
            self.mine_list.add((row,col))
            i += 1
            if i != len(self.mine_list):
                i -= 1
            else:
                self.field[row][col] = -1
                self.add_dangerous_neighbor((row,col))
                
                #self.field_dict[(b,a)][0] = True
                #self.addNeighborMine((a,b))
                
            
            
    
    def add_dangerous_neighbor(self, cell):
        """Adds to the count of each of a mine's neighbors excluding those that are also mines."""
        neighbors = self.get_neighbors(cell)
        for n in neighbors:
            if self.field[n[0]][n[1]] >= 0: #less than 0 means that the cell is already a mine
                self.field[n[0]][n[1]] += 1

    def get_field_size(self):
        """Returns the total number of cells in the minefield"""
        return self.size*self.size

    

    def set_solver(self, solver):
        self.solver = solver

    def get_neighbors(self, cell):
        """Returns a list of all the neighbors of the argument cell."""
        neighbors = []
        if cell[1] != 0: #left
            neighbors.append((cell[0], cell[1]-1))
        if cell[1] != self.size-1: #right
            neighbors.append((cell[0], cell[1]+1))
        if cell[0] != 0: #up
            neighbors.append((cell[0]-1, cell[1]))
        if cell[0] != self.size-1: #down
            neighbors.append((cell[0]+1, cell[1]))
        if cell[0] != 0 and cell[1] != 0: #upper-left
            neighbors.append((cell[0]-1, cell[1]-1))
        if cell[0] != 0 and cell[1] != self.size-1: #upper-right
            neighbors.append((cell[0]-1, cell[1]+1))
        if cell[0] != self.size-1 and cell[1] != 0: #lower-left
            neighbors.append((cell[0]+1, cell[1]-1))
        if cell[0] != self.size-1 and cell[1] != self.size-1: #lower-right
            neighbors.append((cell[0]+1, cell[1]+1))

        return neighbors

    def get_unvisited_neighbors(self, cell):
        """Returns a list of all the unvisited neighbors of the argument cell."""
        #Might need to use is_empty instead
        neighbors = []
        if cell[1] != 0: #left
            if not self.is_visited((cell[0], cell[1]-1)):
                neighbors.append((cell[0], cell[1]-1))            
        if cell[1] != self.size-1: #right
            if not self.is_visited((cell[0], cell[1]+1)):
                neighbors.append((cell[0], cell[1]+1))
        if cell[0] != 0: #up
            if not self.is_visited((cell[0]-1, cell[1])):
                neighbors.append((cell[0]-1, cell[1]))
        if cell[0] != self.size-1: #down
            if not self.is_visited((cell[0]+1, cell[1])):
                neighbors.append((cell[0]+1, cell[1]))
        if cell[0] != 0 and cell[1] != 0: #upper-left
            if not self.is_visited((cell[0]-1, cell[1]-1)):
                neighbors.append((cell[0]-1, cell[1]-1))
        if cell[0] != 0 and cell[1] != self.size-1: #upper-right
            if not self.is_visited((cell[0]-1, cell[1]+1)):
                neighbors.append((cell[0]-1, cell[1]+1))
        if cell[0] != self.size-1 and cell[1] != 0: #lower-left
            if not self.is_visited((cell[0]+1, cell[1]-1)):
                neighbors.append((cell[0]+1, cell[1]-1))
        if cell[0] != self.size-1 and cell[1] != self.size-1: #lower-right
            if not self.is_visited((cell[0]+1, cell[1]+1)):
                neighbors.append((cell[0]+1, cell[1]+1))

        return neighbors

    #def get_simpler_neighbors(self, cell):
    #    """Returns a list of the neighbors of the argument cell that are in the four main directions.
    #    This is a helper function to be used with get_empty_neighbors.
    #    """
    #    neighbors = []
    #    if cell[1] != 0: #left
    #        neighbors.append((cell[0], cell[1]-1))
    #    if cell[1] != self.size-1: #right
    #        neighbors.append((cell[0], cell[1]+1))
    #    if cell[0] != 0: #up
    #        neighbors.append((cell[0]-1, cell[1]))
    #    if cell[0] != self.size-1: #down
    #        neighbors.append((cell[0]+1, cell[1]))

    #    return neighbors

    def is_mine(self, cell):
        """Returns whether the argument cell is a mine."""
        return self.field[cell[0]][cell[1]] == -1

    def is_known_mine(self, cell):
        return self.working_field[cell[0]][cell[1]] == -1

    def is_visited(self, cell):
        """Returns whether the argument cell has been visited."""
        #return (self.field_dict[(cell[0],cell[1])] and not self.is_flagged(cell))
        return self.field_dict[(cell[0],cell[1])]

    def valid_search(self, cell):
        """Returns whether the argument cell is a valid move for searching."""
        return (not self.field_dict[(cell[0],cell[1])] and not self.is_flagged(cell))

    def search(self, cell):
        """Performs a normal search of the cell."""
        if not self.field_dict[(cell[0],cell[1])]:
            self.solver.update_history(cell)
            self.field_dict[(cell[0],cell[1])] = True
            self.working_field[cell[0]][cell[1]] = self.field[cell[0]][cell[1]]
            if self.working_field[cell[0]][cell[1]] == -1:
                self.game_over = True
                self.solver.boom(cell)
            if self.working_field[cell[0]][cell[1]] == 0:
                self.clear_empties(cell)
            
        

    #def visit(self, cell):
    #    """A helper function for clear_empties. Simply visits a cell."""
    #    self.field_dict[(cell[0],cell[1])] = True
    #    self.working_field[cell[0]][cell[1]] = self.field[cell[0]][cell[1]]
        

    def is_flagged(self, cell):
        """Returns whether the argument cell has been flagged."""
        return self.working_field[cell[0]][cell[1]] == 9

    def flag(self, cell):
        """Flags the argument cell."""
        self.working_field[cell[0]][cell[1]] = 9

    def count_neighbor_mines(self, cell):
        """Returns the displayed number of neighboring mines for the argument cell."""
        return self.field[cell[0]][cell[1]]

    #Might not be needed but keeping it here just in case for now
    def is_empty(self, cell):
        """Returns whether the cell is an unvisited and unflagged cell with no mine neighbors."""
        return (self.count_neighbor_mines(cell) == 0 and not self.is_flagged(cell) and not self.is_visited(cell))

    def is_nervous(self, cell):
        """Returns whether the cell has been visited and has at least one neighboring mine."""
        return (self.is_visited(cell) and self.count_neighbor_mines(cell) > 0)

    #def get_empty_neighbors(self, cell):
    #    """Returns a list of the argument cell's neighbors that are also empty."""
    #    neighbors = self.get_simpler_neighbors(cell)
    #    empties = []
    #    for n in neighbors:
    #        if self.is_empty(n):
    #            empties.append(n)
    #    return empties

    def clear_empties(self, cell):
        """Flood fills the empty cells that neighbor the argument cell."""
        #neighbors = self.get_empty_neighbors(cell)
        neighbors = self.get_neighbors(cell)
        if len(neighbors) > 0:
            for n in neighbors:
                self.search(n)
                #self.visit(n)
                #self.clear_empties(n)

        pass

    def get_valid_moves(self):
        """Returns a list of the valid moves given the current state of the working minefield"""
        move_list = []
        for row in range(self.size):
            for col in range(self.size):
                if self.valid_search((row,col)):
                    move_list.append((row,col))
        return move_list

    def print_answer_minefield(self):
        """Prints the current minefield with the mines revealed."""
        print("\n\n")
        print(" " + "----"*self.size + "-")
        for row in range(self.size):
            line = " |"
            for col in range(self.size):
                line += " "

                if self.is_mine((row,col)): #the cell contains a mine
                    if self.is_flagged((row,col)): #the cell's mine has been flagged and therefore defused
                        line += "D"
                    else: #the cell's mine has not been flagged
                        line += "M"
                elif self.is_flagged((row,col)): #the cell is not a mine but was flagged
                    line += "F"              
                else:
                    line += str(self.count_neighbor_mines((row,col))) #the cell is not a mine
                    
                line += " "

                line += "|"
            print(line)
            print(" " + "----"*self.size + "-")
        print("\n\n")

    def print_working_minefield(self):
       """Prints the current minefield as seen by the AI at its current progress."""
<<<<<<< HEAD
       print(self.mine_list)
       print("\n\n")
=======
       #print(self.mine_list)
       print()
       outcome = self.solver.report_outcome()
       if len(outcome) == 1:
           print("Win!")
       elif outcome[0] == 2:
           print("Lose!")
           print("Boomed at cell: " + str(outcome[1]))
       else:
           print("Fluke!")
           print("Boomed at cell: " + str(outcome[1]))
       print("Found Mine Cells: " + str(self.solver.mine_cells))
       print("Mines Remaining: " + str(self.solver.mines_remaining))
       print("\n")
>>>>>>> f4f541ba4c182fc7cc4c2993e6f5f063a1cd6d38
       print(" " + "----"*self.size + "-")
       for row in range(self.size):
           line = " |"
           for col in range(self.size):
               line += " "

               if self.is_flagged((row,col)): #the cell has been flagged
                   line += "F"
               elif not self.is_visited((row,col)): #the cell has not been visited
                   line += " "
               elif self.is_mine((row,col)): #the cell contains a mine
                   line += "M"
               else:
<<<<<<< HEAD
                   if self.neighbor_mine_count((row,col)) == 0:
                       line += "V" #the cell has been visited but does not have neighboring mines
                   else:
                       line += str(self.neighbor_mine_count((row,col))) #the cell has been visited but it has at least one neighboring mine
               line += " "

               line += "|"
           print(line)
           print(" " + "----"*self.size + "-")
       print("\n\n")
=======
                   if self.count_neighbor_mines((row,col)) == 0:
                       line += "V" #the cell has been visited but does not have neighboring mines
                   else:
                       line += str(self.count_neighbor_mines((row,col))) #the cell has been visited but it has at least one neighboring mine
               line += " |"
           print(line)
           print(" " + "----"*self.size + "-")
       print("\n\n----------------------------------------------------------------------------------------------")
       pass

    def temp_way_to_check_for_game_over(self):
       moves = self.get_valid_moves()
       if len(moves) == 0:
           self.game_over = True
>>>>>>> f4f541ba4c182fc7cc4c2993e6f5f063a1cd6d38
