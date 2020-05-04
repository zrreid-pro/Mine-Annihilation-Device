#This is the file that will run the Minesweeper game
import Minesweeper as game
import Mine_Annihilation_Device as mad

#IMPORTANT: ALTER TO USE USER INPUT RATHER THAN WHAT IT'S CURRENTLY DOING

#Not currently set up for more than for debugging puposes

#######################################################
#Change variables in this section for different results
difficulty = 3
iterations = 5
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
print("Win Percentage: " + str((wins/(iterations - flukes))*100))
print(bot.initial_stage_break_condition)

#bot.show_work()

#print("\n\nAnswer Minefield")
#mf.print_answer_minefield()

#print("Mines Remaining: " + str(bot.mines_remaining))
#print("Moves Made:")
#print(bot.moves_made)


    