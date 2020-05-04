#This is the file that will hold the implementation of the solver AI
import Minesweeper #might not need this import statement, revisit and evaluate later
import random as rand
import numpy as np

class MAD:
    def __init__(self):
        """This is a class of minesweeper solving AI.

        Options for current strategy are given as integers with the following meaning:
            0: Random Selection Strategy
            1: Straightfoward Approach
            2: Multisquare Algorithm
            3: Tank Algorithm
        """
        self.minefield = None #This is the game of minesweeper
        self.moves_made = None #This is move history
        self.turn = 0
        self.initial_stage_break_condition = 0 #Beginner (12), Intermediate (38), Expert (86)
        self.initial_stage_break = False
        self.endgame_threshold = 8 #Needed for tank
        self.mines_remaining = 0 #Needed for tank
        self.current_strategy = 0 #Probably isnt needed anymore
        self.mine_cells = set([]) #This is the set of mine spaces
        self.outcome = 1 #This tells if the AI has won (1), lost (2), or fluked (3)
        self.boom_cell = None #This is the mine cell that the AI accidentally picked

        #I think it might make more sense to have the AI keep track of the working board
        #but need to return to that thought later
        #self.working_field = None

        self.current_valid_moves = [] #These are the moves left to make

    def survey_minefield(self, minefield):
        self.minefield = minefield

        #self.working_field = np.zeros((self.minefield.size, self.minefield.size), dtype=int)

        self.mines_remaining = minefield.mine_total
        self.initial_stage_break_condition = int(minefield.get_field_size()*0.15)
        self.current_valid_moves = self.minefield.get_valid_moves()
        self.moves_made = []
        self.minefield.set_solver(self)
        self.find_mines()
        self.show_work()
        return self.outcome

    #Returns a random move that can still be made, basically your start method
    def random_move(self, valid_moves):
        while(True):
            row = rand.randint(0, self.minefield.get_field_size()-1)
            col = rand.randint(0, self.minefield.get_field_size()-1)
            if (row,col) in valid_moves:
                return (row, col)

    #This method is the one that makes the moves. It removes the made move from the list of valid moves and eventually updates the move history
    def search_cell(self, cell):
        self.minefield.search(cell)
        
        if self.initial_stage_break:
            self.turn += 1

        try:
            self.current_valid_moves.remove(cell)
        except:
            pass

    #Calls flag method from game, adds mine to mine list, lowers remaining mine count, removes move from valid moves
    def flag_cell(self, cell):
        if cell not in self.mine_cells:
            self.minefield.flag(cell)
            #print("Flagged Cell: " + str(cell))
            self.mine_cells.add(cell)
            self.mines_remaining -= 1
            try:
                self.current_valid_moves.remove(cell)
            except:
                pass

    #This is called by the minesweeper game whenever a move is made
    def update_history(self, cell):
        self.moves_made.append(cell)
        try:
            self.current_valid_moves.remove(cell)
        except:
            print("Update Fail")
            pass


    def show_work(self):
        """Prints the AI's current working Minefield."""
        self.minefield.print_working_minefield()

    def report_outcome(self):
        """Returns the outcome of the game."""
        if self.outcome == 1:
            return (self.outcome,)
        else:
            return (self.outcome, self.boom_cell)
        
    #Not in use, currently using other solver, just ignore this
    def do_work(self):
        """This is the overall solving method."""
        #do the work
        move = None

        if self.current_strategy == 0: #random move
            move = self.random_move(self.current_valid_moves)
        elif self.current_strategy == 1: #straightfoward
            pass
        elif self.current_strategy == 2: #multisquare
            pass
        else: #tank
            pass

        pass


    #The equivalent of Evan's find_mines
    def traverse_helper(self, cell):
        count = 0

        if not self.minefield.is_nervous(cell):
            return
        else:
            count = self.minefield.count_neighbor_mines(cell) #Gets the number from the cell

        neighbors = self.minefield.get_unvisited_neighbors(cell) #Gets the unvisited neighbors, it's the functional equivalent of counting *'s

        if len(neighbors) == count:
            for n in neighbors:
                self.flag_cell(n)
                
        pass

    #The equivalent of Evan's find_mine_field
    def traverse_field(self):
        for i in range(self.minefield.size):
            for j in range(self.minefield.size):
                self.traverse_helper((i,j))
        pass


    def multisquare_helper(self, cell):
        if not self.minefield.is_nervous(cell):
            #print("Multisquare First Check")
            return []

        count = self.minefield.count_neighbor_mines(cell)
        temp = self.minefield.get_unvisited_neighbors(cell)
        cells = []
        num_mines = 0

        for cell in temp:
            if cell in self.mine_cells:
                num_mines += 1
            else:
                cells.append(cell)

        if num_mines == count:
            return cells
        else:
            #print("Multisquare Second Check")
            return []


    def multisquare(self):
        moves = set([])

        for i in range(self.minefield.size):
            for j in range(self.minefield.size):
                if self.minefield.is_nervous((i,j)):
                    possible_moves = self.multisquare_helper((i,j))
                    if len(possible_moves) != 0:
                        moves.update(possible_moves)

        moves.difference_update(self.moves_made)

        if len(moves) == 0:
            return False

        return moves


    #Makes an array copy of the field and then fills it with the effective counts
    #Effective count is basically the number the cell usually has - the number of flags around it
    #If a cell isnt visited, it goes in as a 0
    #If a cell is a flag that is only touching numbered cells with effective counts at 0, it's irrelevant and also goes in as a 0
    #If the flagged cell is relevant, it goes in as 9
    def generate_relevant_field(self): #Works
        field = np.copy(self.minefield.working_field)
        for i in range(self.minefield.size):
            for j in range(self.minefield.size):
                e_count = self.minefield.effective_count((i,j))
                if e_count == 9:
                    if self.minefield.is_irrelevant((i,j)):
                        field[i][j] = 0
                    else:
                        field[i][j] = 9
                else:
                    field[i][j] = e_count
        #self.shave_field(field)
        return field
        #return self.shave_field(field)
    
    #Not in use, was an idea to shrink the array I'm working with that didnt pan out
    def shave_field(self, field):
        new_num_rows = len(field)
        new_num_cols = len(field[0])

        row_sum = np.sum(field, axis=1)
        print("Row_sum: " + str(row_sum))

        #for i in range(len(field[0])):
        #    for j in range(len(field[0][0])):

        return

    #This generates the relevant areas. (Think the pictures in the linked site that only show a small portion of the board)
    #I dont have any reason to believe that this doesnt work at the moment
    def identify_relevant_area(self, focus_cells): #works to my knowledge
        all_areas = [] #allRegions
        addressed = [] #covered

        while(True):
            queue = [] #queue
            finished = [] #finishedRegion

            for f_cell in focus_cells:
                if f_cell not in addressed:
                    queue.append(f_cell)
                    break

            if len(queue) == 0:
                break

            while len(queue) > 0:
                current_cell = queue.pop(0)
                finished.append(current_cell)
                addressed.append(current_cell)
                for f_cell in focus_cells:
                    chained = False
                    if f_cell in finished:
                        continue
                    
                    if not self.minefield.is_chained(current_cell,f_cell):
                        chained = False
                    else:
                        for i in range(self.minefield.size):
                            for j in range(self.minefield.size):
                                if self.minefield.count_neighbor_mines((i,j)) > 0:
                                    if self.minefield.is_chained(current_cell,(i,j)) and self.minefield.is_chained(f_cell,(i,j)):
                                        chained = True
                                        break
                                if chained:
                                    break

                        
                    if not chained:
                        continue
                    if not f_cell in queue:
                        queue.append(f_cell)
            all_areas.append(finished)

        return all_areas

    #This places a flag on the tank_field at the place of the cell arg
    #If any of the cell's neighbors' counts becomes a negative, the placement is invalid and it returns an empty list
    #The ignore arg is a list of cells to ignore.
    #These are cells that arent touching the potential mine cells or the numbered cells bordering the potential mine cells
    def validate_placement(self, tank_field, cell, ignore):
        tank_field[cell[0]][cell[1]] = 9
        neighbors = self.minefield.get_neighbors(cell)
        for n in neighbors:
            if not n in ignore:
                tank_field[n[0]][n[1]] -= 1
                if tank_field[n[0]][n[1]] < 0:
                    return []

        return tank_field #The placement works and so the possible placement is accepted


    #This is supposed to generate a possible configuration of mines in the potential cells
    
    def generate_possible_solution(self, tank_field, area, mines, ignore=[]):
        if mines == 0:
            return tank_field
        elif len(area) == 0:
            return tank_field

        if not ignore:
            #ignore = []
            for i in range(len(tank_field)):
                for j in range(len(tank_field)):
                    if tank_field[i][j] == 0 and not (i,j) in area:
                        ignore.append((i,j))


        next_field = self.validate_placement(tank_field, area[0], ignore)

        if len(next_field) == 0:
            solution = self.generate_possible_solution(tank_field, area[1:], mines, ignore)
        else:
            solution = self.generate_possible_solution(next_field, area[1:], mines-1, ignore)




        return solution

    def determine_best_move(self, area):
        tank_field = self.generate_relevant_field()
        print("Tank Field:\n" + str(tank_field))
        possible_solutions = set([])
        max_mines = self.mines_remaining

        solution = self.generate_possible_solution(tank_field,area,max_mines)
        print("Solution:\n" + str(solution))

        #for i in range(self.minefield.size):
        #    for j in range(self.minefield.size):

        #        if tank_field[i][j]==0:
        #            continue

        #        surrounding = 0
        #        if (i == 0 and j == 0) or (i == len(tank_field)-1 and j == len(tank_field)-1):
        #            surrounding = 3
        #        elif (i == 0 or j == 0 or i == len(tank_field)-1 or len(tank_field)-1):
        #            surrounding = 5
        #        else:
        #            surrounding = 8

        #        numflags = self.minefield.count_flagged_neighbors((i,j))

        




        return

    


    def tank(self):
        focus_cells = []
        for cell in self.current_valid_moves: #Narrows it down to border cells
            if self.minefield.is_interesting(cell):
                focus_cells.append(cell)
        print("Tank Cells: " + str(focus_cells))

        endgame = False
        if ((len(self.current_valid_moves)-len(focus_cells)) > self.endgame_threshold):
            endgame = True
        #else: #Not necessary but that's what he did
        #   focus_cells = self.current_valid_moves
        
        separate = [] #supposed to be a list of lists containing cells
        if not endgame:
            separate.append(focus_cells)
        else:
            separate = self.identify_relevant_area(focus_cells)

        print("Separate: " + str(separate))

        for section in separate:
            self.determine_best_move(section)

        #con_cells = []
        #for cell in focus_cells:
        #    con_cells = self.minefield.get_constraining_neighbors(cell)
        #    print("For cell: " + str(cell) + "\nCon Neighbors: " + str(con_cells))

        #area = []
        #for cell in focus_cells:
        #    area = self.identify_relevant_area(cell)

        pass

    def boom(self, cell):
        """
        Is called when the AI finds a mine.
        This is meant for reporting purposes
        """
        self.boom_cell = cell
        if not self.initial_stage_break:
            self.outcome = 3
        else:
            self.outcome = 2

    def find_mines(self):

        ##########################################################################
        #Beginning Stage
        ##########################################################################
        while(self.turn < 2 and not self.minefield.game_over):
            #move = self.random_move(self.current_valid_moves)
            #if(move not in self.mine_cells) and (move not in self.moves_made):
            #    self.search_cell(move)
            #    print("Random Move: " + str(move))
            #    self.turn += 1
            #    self.show_work()
            #self.traverse_field()
            
            move = (0,0)
            self.search_cell(move)
            #print("Random Move: " + str(move))
            self.turn += 1
            #self.show_work()
            self.traverse_field()
            move = (2,3)
            self.search_cell(move)
            #print("Random Move: " + str(move))
            self.turn += 1
            #self.show_work()
            self.traverse_field()

            if len(self.moves_made) >= self.initial_stage_break_condition:
                #Currently doesn't count flagging a cell as making a move so it may be something to adjust later
                break

        ##########################################################################
        #Algorithmic Stage
        ##########################################################################
        self.initial_stage_break = True

        while(not self.minefield.game_over and self.mines_remaining > 0):
            moves = self.multisquare()
            #print("Multi-square Moves: " + str(moves))
            if not moves:
                self.tank()
                move = self.current_valid_moves[0]
                self.search_cell(move)
                #print("Multi-square had squat: " + str(move))
                #self.show_work()
            else:
                while len(moves) > 0:
                    move = moves.pop()
                    self.search_cell(move)
                    #print("Multi-square Move: " + str(move))
                    #self.show_work()
                    if self.minefield.game_over:
                        break

            if not self.minefield.game_over:
                self.traverse_field()
            else:
                break


        ##########################################################################
        #Cleanup Stage
        ##########################################################################
        if self.mines_remaining == 0:
            while len(self.current_valid_moves) > 0:
                self.search_cell(self.current_valid_moves[0])
        ##########################################################################


        pass
