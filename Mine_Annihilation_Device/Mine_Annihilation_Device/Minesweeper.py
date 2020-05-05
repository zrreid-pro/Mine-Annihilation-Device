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
        self.field = np.zeros((self.size, self.size), dtype=int)
        self.working_field = np.zeros((self.size, self.size), dtype=int)
        self.field_dict = {}
        self.mine_list = set([])
        self.fill_minefield()

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

    def get_visited_neighbors(self, cell):
        neighbors = []
        if cell[1] != 0: #left
            if self.is_visited((cell[0], cell[1]-1)):
                neighbors.append((cell[0], cell[1]-1))            
        if cell[1] != self.size-1: #right
            if self.is_visited((cell[0], cell[1]+1)):
                neighbors.append((cell[0], cell[1]+1))
        if cell[0] != 0: #up
            if self.is_visited((cell[0]-1, cell[1])):
                neighbors.append((cell[0]-1, cell[1]))
        if cell[0] != self.size-1: #down
            if self.is_visited((cell[0]+1, cell[1])):
                neighbors.append((cell[0]+1, cell[1]))
        if cell[0] != 0 and cell[1] != 0: #upper-left
            if self.is_visited((cell[0]-1, cell[1]-1)):
                neighbors.append((cell[0]-1, cell[1]-1))
        if cell[0] != 0 and cell[1] != self.size-1: #upper-right
            if self.is_visited((cell[0]-1, cell[1]+1)):
                neighbors.append((cell[0]-1, cell[1]+1))
        if cell[0] != self.size-1 and cell[1] != 0: #lower-left
            if self.is_visited((cell[0]+1, cell[1]-1)):
                neighbors.append((cell[0]+1, cell[1]-1))
        if cell[0] != self.size-1 and cell[1] != self.size-1: #lower-right
            if self.is_visited((cell[0]+1, cell[1]+1)):
                neighbors.append((cell[0]+1, cell[1]+1))

        return neighbors

    def count_flagged_neighbors(self, cell):
        flagged = 0
        if cell[1] != 0: #left
            if self.is_flagged((cell[0], cell[1]-1)):
                flagged += 1           
        if cell[1] != self.size-1: #right
            if self.is_flagged((cell[0], cell[1]+1)):
                flagged += 1
        if cell[0] != 0: #up
            if self.is_flagged((cell[0]-1, cell[1])):
                flagged += 1
        if cell[0] != self.size-1: #down
            if self.is_flagged((cell[0]+1, cell[1])):
                flagged += 1
        if cell[0] != 0 and cell[1] != 0: #upper-left
            if self.is_flagged((cell[0]-1, cell[1]-1)):
                flagged += 1
        if cell[0] != 0 and cell[1] != self.size-1: #upper-right
            if self.is_flagged((cell[0]-1, cell[1]+1)):
                flagged += 1
        if cell[0] != self.size-1 and cell[1] != 0: #lower-left
            if self.is_flagged((cell[0]+1, cell[1]-1)):
                flagged += 1
        if cell[0] != self.size-1 and cell[1] != self.size-1: #lower-right
            if self.is_flagged((cell[0]+1, cell[1]+1)):
                flagged += 1

        return flagged

    def get_constraining_neighbors(self, cell):
        neighbors = []
        if cell[1] != 0: #left
            if self.is_flagged((cell[0], cell[1]-1)) or self.effective_count((cell[0], cell[1]-1)) > 0:
                neighbors.append((cell[0], cell[1]-1))            
        if cell[1] != self.size-1: #right
            if self.is_flagged((cell[0], cell[1]+1)) or self.effective_count((cell[0], cell[1]+1)) > 0:
                neighbors.append((cell[0], cell[1]+1))
        if cell[0] != 0: #up
            if self.is_flagged((cell[0]-1, cell[1])) or self.effective_count((cell[0]-1, cell[1])) > 0:
                neighbors.append((cell[0]-1, cell[1]))
        if cell[0] != self.size-1: #down
            if self.is_flagged((cell[0]+1, cell[1])) or self.effective_count((cell[0]+1, cell[1])) > 0:
                neighbors.append((cell[0]+1, cell[1]))
        if cell[0] != 0 and cell[1] != 0: #upper-left
            if self.is_flagged((cell[0]-1, cell[1]-1)) or self.effective_count((cell[0]-1, cell[1]-1)) > 0:
                neighbors.append((cell[0]-1, cell[1]-1))
        if cell[0] != 0 and cell[1] != self.size-1: #upper-right
            if self.is_flagged((cell[0]-1, cell[1]+1)) or self.effective_count((cell[0]-1, cell[1]+1)) > 0:
                neighbors.append((cell[0]-1, cell[1]+1))
        if cell[0] != self.size-1 and cell[1] != 0: #lower-left
            if self.is_flagged((cell[0]+1, cell[1]-1)) or self.effective_count((cell[0]+1, cell[1]-1)) > 0:
                neighbors.append((cell[0]+1, cell[1]-1))
        if cell[0] != self.size-1 and cell[1] != self.size-1: #lower-right
            if self.is_flagged((cell[0]+1, cell[1]+1)) or self.effective_count((cell[0]+1, cell[1]+1)) > 0:
                neighbors.append((cell[0]+1, cell[1]+1))

        return neighbors

    def is_chained(self, cell_1, cell_2):
        if cell_1[1] != 0: #left
            if self.compare_cells((cell_1[0],cell_1[1]-1),cell_2):
                return True            
        if cell_1[1] != self.size-1: #right
            if self.compare_cells((cell_1[0],cell_1[1]+1),cell_2):
                return True
        if cell_1[0] != 0: #up
            if self.compare_cells((cell_1[0]-1,cell_1[1]),cell_2):
                return True
        if cell_1[0] != self.size-1: #down
            if self.compare_cells((cell_1[0]+1,cell_1[1]),cell_2):
                return True
        if cell_1[0] != 0 and cell_1[1] != 0: #upper-left
            if self.compare_cells((cell_1[0]-1,cell_1[1]-1),cell_2):
                return True
        if cell_1[0] != 0 and cell_1[1] != self.size-1: #upper-right
            if self.compare_cells((cell_1[0]-1,cell_1[1]+1),cell_2):
                return True
        if cell_1[0] != self.size-1 and cell_1[1] != 0: #lower-left
            if self.compare_cells((cell_1[0]+1,cell_1[1]-1),cell_2):
                return True
        if cell_1[0] != self.size-1 and cell_1[1] != self.size-1: #lower-right
            if self.compare_cells((cell_1[0]+1,cell_1[1]+1),cell_2):
                return True

        return False

    def compare_cells(self, cell_1, cell_2):
        return (cell_1[0] == cell_2[0] and cell_1[1] == cell_2[1])

    def is_irrelevant(self, cell):
        neighbors = self.get_neighbors(cell)
        for n in neighbors:
            if self.effective_count(n) != 0:
                return False
        return True

    def effective_count(self, cell):
        if self.is_flagged(cell):
            return 9
        elif not self.is_visited(cell):
            return 0
        else:
            return self.working_field[cell[0]][cell[1]] - self.count_flagged_neighbors(cell)

    def is_mine(self, cell):
        """Returns whether the argument cell is a mine."""
        return self.field[cell[0]][cell[1]] == -1

    def is_visited(self, cell):
        """Returns whether the argument cell has been visited."""
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

    def is_border_cell(self, cell):
        return (cell[0] == 0 or cell[0] == self.size-1 or cell[1] == 0 or cell[1] == self.size-1)

    def is_interesting(self, cell):
        if cell[1] != 0: #left
            if self.is_visited((cell[0], cell[1]-1)):
                return True            
        if cell[1] != self.size-1: #right
            if self.is_visited((cell[0], cell[1]+1)):
                return True
        if cell[0] != 0: #up
            if self.is_visited((cell[0]-1, cell[1])):
                return True
        if cell[0] != self.size-1: #down
            if self.is_visited((cell[0]+1, cell[1])):
                return True
        if cell[0] != 0 and cell[1] != 0: #upper-left
            if self.is_visited((cell[0]-1, cell[1]-1)):
                return True
        if cell[0] != 0 and cell[1] != self.size-1: #upper-right
            if self.is_visited((cell[0]-1, cell[1]+1)):
                return True
        if cell[0] != self.size-1 and cell[1] != 0: #lower-left
            if self.is_visited((cell[0]+1, cell[1]-1)):
                return True
        if cell[0] != self.size-1 and cell[1] != self.size-1: #lower-right
            if self.is_visited((cell[0]+1, cell[1]+1)):
                return True

        return False       

    def is_flagged(self, cell):
        """Returns whether the argument cell has been flagged."""
        return self.working_field[cell[0]][cell[1]] == 9

    def flag(self, cell):
        """Flags the argument cell."""
        self.working_field[cell[0]][cell[1]] = 9

    def count_neighbor_mines(self, cell):
        """Returns the displayed number of neighboring mines for the argument cell."""
        return self.field[cell[0]][cell[1]]

    def is_nervous(self, cell):
        """Returns whether the cell has been visited and has at least one neighboring mine."""
        return (self.is_visited(cell) and self.count_neighbor_mines(cell) > 0)

    def clear_empties(self, cell):
        """Flood fills the empty cells that neighbor the argument cell."""
        neighbors = self.get_neighbors(cell)
        if len(neighbors) > 0:
            for n in neighbors:
                self.search(n)

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
       print("Mine Locations: " + str(self.mine_list))
       #print("Engaged Tank: " + str(self.solver.tanked))
       print()
       if self.game_over:
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