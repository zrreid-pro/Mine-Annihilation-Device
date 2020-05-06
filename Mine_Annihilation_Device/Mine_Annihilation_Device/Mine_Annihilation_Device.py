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
        self.initial_stage_break_condition = 0 #Beginner (12), Intermediate (38), Expert (86) this changed
        self.initial_stage_break = False
        self.tank_standby_condition = 0 
        self.tank_on_standby = False
        self.endgame_threshold = 8 #Needed for tank
        self.mines_remaining = 0 #Needed for tank
        self.current_strategy = 0 #Probably isnt needed anymore
        self.mine_cells = set([]) #This is the set of mine spaces
        self.outcome = 1 #This tells if the AI has won (1), lost (2), or fluked (3)
        self.boom_cell = None #This is the mine cell that the AI accidentally picked
        self.current_tank_configurations = set([])
        self.current_valid_moves = [] #These are the moves left to make
        self.tanked = False
        self.tank_field = None
        self.ignore = set([])
        self.retreaded = False
        self.tank_neighbor_dict = {}

    def survey_minefield(self, minefield):
        """Takes an argument minefield and initializes the important attribute of the MAD AI in preparation for solving the game."""
        self.minefield = minefield
        self.mines_remaining = minefield.mine_total
        self.initial_stage_break_condition = int(minefield.get_field_size()*0.2)
        self.tank_standby_condition = int(minefield.get_field_size()*0.2)
        self.current_valid_moves = self.minefield.get_valid_moves()
        self.moves_made = []
        self.minefield.set_solver(self)
        self.find_mines()
        self.show_work()
        return self.outcome

    def random_move(self, valid_moves):
        """Returns a valid random move from the argument list of valid moves."""
        while(True):
            row = rand.randint(0, self.minefield.get_field_size()-1)
            col = rand.randint(0, self.minefield.get_field_size()-1)
            if (row,col) in valid_moves:
                return (row, col)

    def search_cell(self, cell):
        """Uses the argument cell as an input to make a move for the current game."""
        self.minefield.search(cell)        
        if self.initial_stage_break:
            self.turn += 1
        try:
            self.current_valid_moves.remove(cell)
        except:
            pass

    def flag_cell(self, cell):
        """Uses the argument cell as an input to flag a cell for the current game."""
        if cell not in self.mine_cells:
            self.minefield.flag(cell)
            self.mine_cells.add(cell)
            self.mines_remaining -= 1
            try:
                self.current_valid_moves.remove(cell)
            except:
                pass

    def update_history(self, cell):
        """Is called from the current game. It updates the moves made attribute with the argument cell."""
        self.moves_made.append(cell)
        try:
            self.current_valid_moves.remove(cell)
        except:
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
        
    def traverse_helper(self, cell):
        """This is a helper for the traverse field method. If the number of unvisited neighbor
        cells equals the cell's number, then it flags all neighboring unvisited cells."""
        count = 0
        if not self.minefield.is_nervous(cell):
            return
        else:
            count = self.minefield.count_neighbor_mines(cell)
        neighbors = self.minefield.get_unvisited_neighbors(cell)
        if len(neighbors) == count:
            for n in neighbors:
                self.flag_cell(n)

    def traverse_field(self):
        """This is the straightforward algorithm. It traverses the field
        flagging in the obvious places where there is a mine."""
        for i in range(self.minefield.size):
            for j in range(self.minefield.size):
                self.traverse_helper((i,j))

    def multisquare_helper(self, cell):
        """This is a helper for the multisquare algorithm. It checks for the safe moves neighboring the argument cell and returns the list."""
        if not self.minefield.is_nervous(cell):
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
            return []

    def multisquare(self):
        """This is the multisquare algorithm. It takes into account multiple
        different numbered cells to return a list of cells that are safe to visit."""
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

    def generate_relevant_field(self):
        """Part of the Tank algorithm.
        Returns a copy of the working minefield with the irrelevant cells and their numbers phased out."""
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
        return field

    def identify_relevant_area(self, focus_cells):
        """Part of the Tank algorithm. Returns the disjointed regions of the argument focus cells."""
        all_areas = []
        addressed = []

        while(True):
            queue = []
            finished = []

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

    def validate_placement(self, tank_field, cell, area, ignore):
        """Part of the Tank algorithm.
        It attempts to place a pseudo mine at the location of the argument cell on the argument tank field.
        Returns the field with the pseudo mine successfully placed or an empty list if the placement fails."""
        new_field = np.copy(tank_field)
        new_field[cell[0]][cell[1]] = 11

        if cell in self.tank_neighbor_dict.keys():
            neighbors = self.tank_neighbor_dict[cell]
        else:
            neighbors = self.minefield.get_neighbors(cell)
            self.tank_neighbor_dict[cell] = neighbors
        
        for n in neighbors:
            if not n in ignore and new_field[n[0]][n[1]] != 11 and new_field[n[0]][n[1]] != 9 and not n in area:
                new_field[n[0]][n[1]] -= 1
                if new_field[n[0]][n[1]] < 0:
                    return []

        return new_field

    def convert_field(self, area, field):
        """Part of the Tank algorithm.
        Converts the argument relevant field into a hashable
        tuple to be stored in the current tank configurations attribute.
        At their respective indeces, either a 1 is placed to represent a pseudo mine being placed in that cell
        or a 0 to represent a cell that didn't receive one."""
        summary = []
        for cell in area:
            if field[cell[0]][cell[1]] == 11:
                summary.append(1)
            else:
                summary.append(0)
        return tuple(summary)    
    
    def generate_possible_solution(self, tank_field, area, total_area, mines):
        """Part of the Tank algorithm. Recurses through the argument area to place pseudo mines in all potential configurations and adds each
        finished one to the current tank configurations attribute."""
        if mines == 0:
            self.current_tank_configurations.add(self.convert_field(total_area, tank_field))
            return
        elif len(area) == 0:
            self.current_tank_configurations.add(self.convert_field(total_area, tank_field))
            return

        if not self.ignore:
            for i in range(len(tank_field)):
                for j in range(len(tank_field)):
                    if tank_field[i][j] == 0 and not (i,j) in area:
                        self.ignore.add((i,j))

        next_field = self.validate_placement(tank_field, area[0], total_area, self.ignore)
        if len(next_field) == 0:
            self.generate_possible_solution(tank_field, area[1:], total_area, mines)
        else:
            self.generate_possible_solution(next_field, area[1:], total_area, mines-1)
            self.generate_possible_solution(tank_field, area[1:], total_area, mines)

        return

    def crunch_the_numbers(self, area):
        """Part of the Tank algorithm. It takes the cells in the argument area and tallies the number of times
        a pseudo mine was placed in that cell for each generated tank configuration.
        Returns the results as a list of percentages with indeces respective to the indeces of the argument area."""
        total_configs = 0
        results = np.zeros(len(area), dtype=int)
        percentage_results = np.zeros(len(area), dtype=float)
        for config in self.current_tank_configurations:
            for n in range(len(area)):
                if config[n] == 11:
                    results[n] += 1
            total_configs += 1

        for result in range(len(results)):
            percentage_results[result] = results[result]/total_configs

        return percentage_results

    def determine_best_move(self, area):
        """Part of the Tank algorithm. Based of the argument area, the method determines the cell with the least
        probability of being a mine. If multiple probabilities are tied for the lowest,
        a portion of the Tank algorithm is rerun focusing on the cells with the least probability while assuming
        that the ones with the highest probility are potential mines."""
        self.tank_field = self.generate_relevant_field()
        max_mines = self.mines_remaining
        self.current_tank_configurations.clear()
        self.generate_possible_solution(self.tank_field, area, area, max_mines)
        results = self.crunch_the_numbers(area)

        min_percentage = 2
        max_percentage = -1
        min_index = 0
        max_index = 0
        min_moves = []
        max_moves = []
        for i in range(len(area)):
            if results[i] < min_percentage:
                min_percentage = results[i]
                min_index = i
                min_moves = []
                min_moves.append(area[i])
            elif results[i] == min_percentage:
                min_moves.append(area[i])
            if results[i] > max_percentage:
                max_percentage = results[i]
                max_index = i
                max_moves = []
                max_moves.append(area[i])
            elif results[i] == max_percentage:
                max_moves.append(area[i])

        if len(min_moves) < 2:
            min_index = np.argmin(results)
            return (area[min_index], min_percentage)
        else:
            results = self.tank_refine(min_moves, max_moves)
        min_index = np.argmin(results)
        return (min_moves[min_index], results[min_index])

    def tank(self):
        """This is the Tank algorithm. It narrows the number of valid moves to the ones that the AI has knowledge about
        and by generating the possible configurations of cells that could potentially hold mines, it is able to determine
        the cell with the least likelihood of being a mine. It does so by placing hypothetical mines, called pseudo mines,
       on a minefield with only the relevant cells remaining on it. Returns the move with the lowest probability of being a mine."""
        self.tanked = True
        focus_cells = []
        for cell in self.current_valid_moves:
            if self.minefield.is_interesting(cell):
                focus_cells.append(cell)

        endgame = False
        if ((len(self.current_valid_moves)-len(focus_cells)) > self.endgame_threshold):
            endgame = True
        
        separate = []
        if not endgame:
            separate.append(focus_cells)
        else:
            separate = self.identify_relevant_area(focus_cells)

        possible_moves = []
        for section in separate:
            possible_moves.append(self.determine_best_move(section))

        min_percentage = 1
        min_index = 0

        for i in range(len(possible_moves)):
            if possible_moves[i][1] < min_percentage:
                min_percentage = possible_moves[i][1]
                min_index = i

        return possible_moves[min_index][0]

    def tank_refine(self, focus_area, assumed_mines):
        """Part of the Tank algorithm. This method runs a smaller scale version of the Tank algorithm in the case that
        there is a tie for the cell with the lowest probability for being a mine. Returns the move from the new lowest
        calculated probability."""
        self.retreaded = True
        self.current_tank_configurations.clear()
        next_field = self.validate_placement(self.tank_field, assumed_mines[0], assumed_mines, self.ignore)
        max_mines = self.mines_remaining-1

        if len(assumed_mines) != 1:
            assumed_mines = assumed_mines[1:]
        for mine in assumed_mines:
            temp_field = self.validate_placement(next_field, mine, assumed_mines, self.ignore)
            if len(temp_field) == 0:
                continue
            else:
                next_field = temp_field
                max_mines -= 1

        self.generate_possible_solution(next_field, focus_area, focus_area, max_mines)
        return self.crunch_the_numbers(focus_area)

    def tank_reset(self):
        """To be called after the Tank algorithm concludes. It resets all of the relevant attributes used by the Tank
        algorithm so that it can be used again should the need arrise."""
        self.current_tank_configurations.clear()
        self.ignore.clear()
        self.tank_field = None
        self.retreaded = False
        return

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
        """This is the overall solving method. It starts out making random moves until enough of the board is cleared
        to be able to start algorithmically locating the rest of the hidden mines. The algorithmic phase of the method begins
        with the Multisquare algorithm and moves on to the Tank algorithm if it fails to identify a safe move to make."""
        ##########################################################################
        #Beginning Stage
        ##########################################################################
        while(not self.initial_stage_break and not self.minefield.game_over):
            move = self.random_move(self.current_valid_moves)
            if(move not in self.mine_cells) and (move not in self.moves_made):
                self.search_cell(move)
                self.turn += 1
                self.minefield.temp_way_to_check_for_game_over()
            self.traverse_field()            

            if len(self.moves_made) + len(self.mine_cells) >= self.initial_stage_break_condition:
                break

        ##########################################################################
        #Algorithmic Stage
        ##########################################################################
        self.initial_stage_break = True

        while(not self.minefield.game_over and self.mines_remaining > 0):
            if not self.tank_on_standby:
                if len(self.moves_made) > self.tank_standby_condition:
                    self.tank_on_standby = True

            moves = self.multisquare()
            if not moves:
                if self.tank_on_standby:
                    move = self.tank()
                    self.search_cell(move)
                else:
                    move = self.current_valid_moves[0]
                    self.search_cell(move)
            else:
                while len(moves) > 0:
                    move = moves.pop()
                    self.search_cell(move)
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
