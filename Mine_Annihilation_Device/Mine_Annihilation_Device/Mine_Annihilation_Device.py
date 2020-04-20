#This is the file that will hold the implementation of the solver AI
import Minesweeper #might not need this import statement, revisit and evaluate later
import random as rand

class MAD:
    def __init__(self):
        """This is a class of minesweeper solving AI.

        Options for current strategy are given as integers with the following meaning:
            1: Random Selection Strategy
            2: Multisquare Algorithm
            3: Tank Algorithm
        """
        self.minefield = None
        self.moves_made = None
        self.current_strategy = 0

    def survey_minefield(self, minefield):
        self.minefield = minefield
        self.moves_made = []
        #do the work
        pass

    def random_move(self, valid_moves):
        while(True):
            row = rand.randint(0, self.minefield.get_field_size()-1)
            col = rand.randint(0, self.minefield.get_field_size()-1)
            if (row,col) in valid_moves:
                return (row, col)


    def show_work(self):
        """Prints the AI's current working Minefield"""
        self.minefield.print_working_minefield()
