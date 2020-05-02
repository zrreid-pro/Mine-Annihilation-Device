#This is the file that will hold the implementation of the solver AI
import Minesweeper #might not need this import statement, revisit and evaluate later
import random as rand

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

    def boom(self, cell):
        """
        Is called when the AI finds a mine.
        This is meant for debugging purposes
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
            move = self.random_move(self.current_valid_moves)
            if(move not in self.mine_cells) and (move not in self.moves_made):
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
