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
        self.minefield = None
        self.moves_made = None
        self.mines_remaining = 0
        self.current_strategy = 0

    def survey_minefield(self, minefield):
        self.minefield = minefield
        self.mines_remaining = minefield.mine_total
        self.moves_made = []
        self.find_mines()
        pass

    def random_move(self, valid_moves):
        while(True):
            row = rand.randint(0, self.minefield.get_field_size()-1)
            col = rand.randint(0, self.minefield.get_field_size()-1)
            if (row,col) in valid_moves:
                return (row, col)

    def search_cell(self, cell):
        self.minefield.search(cell)

    def show_work(self):
        """Prints the AI's current working Minefield"""
        self.minefield.print_working_minefield()

    def find_mines(self):
        """This is the overall solving method."""
        #do the work
        move = None
        valid = self.minefield.get_valid_moves()
        if self.current_strategy == 0: #random move
            move = self.random_move(valid)
        elif self.current_strategy == 1: #straightfoward
            pass
        elif self.current_strategy == 2: #multisquare
            pass
        else: #tank
            pass

        pass
