#This is the file that will run the Minesweeper game
import Minesweeper as game
import Mine_Annihilation_Device as mad


#######################################################
print("What difficulty would you like the M.A.D. to try?")
difficulty = input()
print("And how many games would you like the M.A.D. to play?")
iterations = int(input())

if(difficulty == "Beginner"):
    difficulty = 1

if(difficulty == "Intermediate"):
    difficulty = 2

if(difficulty == "Expert"):
    difficulty = 3

#######################################################

wins = 0
loses = 0
flukes = 0



for i in range(iterations):
    mf = game.Minefield(difficulty)
    bot = mad.MAD()
    outcome = bot.survey_minefield(mf)
    
    
    if outcome == 1:
        wins += 1
    elif outcome == 2:
        loses += 1
    else:
        flukes += 1


if difficulty == 1:
    print("Difficulty: Beginner")
elif difficulty == 2:
    print("Difficulty: Intermediate")
else:
    print("Difficulty: Expert")

print("Total Number of Games: " + str(iterations))
print("Number of Wins: " + str(wins))
print("Number of Loses: " + str(loses))
print("Number of Flukes: " + str(flukes))
if((iterations - flukes) != 0):
    print("Win Percentage: " + str((wins/(iterations - flukes))*100))



    