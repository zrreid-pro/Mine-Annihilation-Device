# Mine_Annihilation_Device
Our project, titled M.A.D. or Mine Annihilation Device is to create an AI that uses different algorithms at different points in a game of Minesweeper. The goal is to create an AI that will be able to successfully play a game of Minesweeper.

Our project contains Python packages that you will need in order to run our project.

You will need: NumPy and random

# Our Implementation of Minesweeper
Our implementation of Minesweeper is almost exactly alike to the normal game of Minesweeper. The differences are that you cannot "chord", and our game is text based.

# Our A.I.
Our A.I. utilized two alorithms, the multi-square algorithm and the tank algorithm. For more detial on those see our paper.
The way it plays a game of Minesweeper is through stages. It starts the game by making random moves until a good portion of
the board is revealed, once it gets past this stage it will move on to employing the alogorithms. It will first use the multi-square and if it finds moves it'll make those moves and use multi-square again until it cannot find moves. When this happens, tank is brought out and used. When these two are combined it is able to win a good amount of games.

# Running Our A.I.
Our A.I. is very easy to run. Simply go to the "Game_Driver.py" file and run it. You will then be asked what difficulty you want the A.I. to try ("Beginner", "Intermediate", or "Expert") and how many games you would like the A.I. to play. After running our   A.I. the results will be printed out to the terminal. You will get number of wins, flukes, losses and the percentage of games won with flukes not counted in the total. A fluke is a game that was lost because while the A.I. was trying to reveal a good portion of the board, it hit a mine. Flukes are not counted as losses as the A.I. never had a chance to play.

# Authors
- Evan Brinckman
- Zachary Reid