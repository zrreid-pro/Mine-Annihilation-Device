#This file holds the implementation of the Minesweeper game
import random as rand

class Minefield:

    def __init__(self, difficulty):
        #1: Beginner(9*9 field with 10 mines)
        #2: Intermediate(16*16 field with 40 mines)
        #3: Expert(24*24 field with 99 mines)
        self.difficulty = difficulty
        self.n = 0
        self.mine_total = 0
        if difficulty == 1:
            self.n = 9
            self.mine_total = 10
        elif difficulty == 2:
            self.n = 16
            self.mine_total = 40
        else:
            self.n = 24
            self.mine_total = 99
        self.cell_total = self.n**2
        self.field_dict = {}
        self.mine_list = []

        self.fill_minefield()


        pass

    #cell value = [isMine, visited, isFlagged, neighborMines, probabilityOfMine]
    def fill_minefield(self):
        for i in range(self.n):
            for j in range(self.n):
                self.field_dict[(i,j)] = [False, False, False, 0, 1.0]

        a = 0
        b = 0
        while len(self.mine_list) <= self.mine_total:
            a = rand.randint(0, self.n-1)
            b = rand.randint(0, self.n-1)
            if (a,b) not in self.mine_list:
                self.field_dict[(a,b)][0] = True
                self.mine_list.append((a,b))
                self.addNeighborMine((a,b))

    def addNeighborMine(self, cell):
        if cell[0] != 0:
           self.field_dict[(cell[0]-1,cell[1])][3] += 1
        if cell[0] != self.n-1:
           self.field_dict[(cell[0]+1,cell[1])][3] += 1
        if cell[1] != 0:
           self.field_dict[(cell[0],cell[1]-1)][3] += 1
        if cell[1] != self.n-1:
           self.field_dict[(cell[0],cell[1]+1)][3] += 1
        if cell[0] != 0 and cell[1] != 0:
            self.field_dict[(cell[0]-1,cell[1]-1)][3] += 1
        if cell[0] != self.n-1 and cell[1] != 0:
            self.field_dict[(cell[0]+1,cell[1]-1)][3] += 1
        if cell[0] != 0 and cell[1] != self.n-1:
            self.field_dict[(cell[0]-1,cell[1]+1)][3] += 1
        if cell[0] != self.n-1 and cell[1] != self.n-1:
            self.field_dict[(cell[0]+1,cell[1]+1)][3] += 1

    def isMine(self, r, c):
        return self.field_dict[(r,c)][0]

    def isVisited(self, r, c):
        return self.field_dict[(r,c)][1]

    def visit(self, r, c):
        self.field_dict[(r,c)][1] = True

    def isFlagged(self, r, c):
        return self.field_dict[(r,c)][2]

    def flag(self, r, c):
        self.field_dict[(r,c)][2] = True

    def neighbor_mine_count(self, r, c):
        return self.field_dict[(r,c)][3]

    def isEmpty(self, r, c):
        return (self.neighbor_mine_count(r,c) == 0 and not self.isMine(r,c))

    def fill_empties(self, r, c):
        if r != 0:
            if (self.isEmpty(r-1,c) and not self.isVisited(r-1,c)) or (not self.isMine(r-1,c) and not self.isVisited(r-1,c)):
                self.visit(r-1,c)
                self.fill_empties(r-1,c)
        if r != self.n-1:
            if (self.isEmpty(r+1,c) and not self.isVisited(r+1,c)) or (not self.isMine(r+1,c) and not self.isVisited(r+1,c)):
                self.visit(r+1,c)
                self.fill_empties(r+1,c)
        if c != 0:
            if (self.isEmpty(r,c-1) and not self.isVisited(r,c-1)) or (not self.isMine(r,c-1) and not self.isVisited(r,c-1)):
                self.visit(r,c-1)
                self.fill_empties(r,c-1)
        if c != self.n-1:
            if (self.isEmpty(r,c+1) and not self.isVisited(r,c+1)) or (not self.isMine(r,c+1) and not self.isVisited(r,c+1)):
                self.visit(r,c+1)
                self.fill_empties(r,c+1)
        #if r != 0 and c != 0:
        #    if self.isEmpty(r-1,c-1) and not self.isVisited(r-1,c-1):
        #        self.visit(r-1,c-1)
        #        self.fill_empties(r-1,c-1)
        #if r != self.n-1 and c != 0:
        #    if self.isEmpty(r+1,c-1) and not self.isVisited(r+1,c-1):
        #        self.visit(r+1,c-1)
        #        self.fill_empties(r+1,c-1)
        #if r != 0 and c != self.n-1:
        #    if self.isEmpty(r-1,c+1) and not self.isVisited(r-1,c+1):
        #        self.visit(r-1,c+1)
        #        self.fill_empties(r-1,c+1)
        #if r != self.n-1 and c != self.n-1:
        #    if self.isEmpty(r+1,c+1) and not self.isVisited(r+1,c+1):
        #        self.visit(r+1,c+1)
        #        self.fill_empties(r+1,c+1)


    def dig(self, r, c):
        if self.isEmpty(r,c):
            self.visit(r,c)
        pass

    def print_minefield(self):
        print(self.mine_list)
        print("\n\n")
        print(" " + "----"*self.n + "-")
        for r in range(self.n):
            line = " |"
            for c in range(self.n):
                line += " "
                if self.isFlagged(r,c):
                    line += "F"
                elif self.isMine(r,c):
                    line += "M"
                elif not self.isVisited(r,c):
                    line += " "                
                else:
                    line += str(self.neighbor_mine_count(r,c))
                line += " "


                #if self.isFlagged(r,c):
                #    line += "F"
                #elif not self.isVisited(r,c):
                #    line += " "
                #elif self.isMine(r,c):
                #    line += "M"
                #else:
                #    if self.neighbor_mine_count(r,c) == 0:
                #        line += "V" #for visited because it's different than just a blank
                #    else:
                #        line += str(self.neighbor_mine_count(r,c))
                #line += " "
                line += "|"
            print(line)
            print(" " + "----"*self.n + "-")
        print("\n\n")