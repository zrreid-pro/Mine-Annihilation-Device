#This is the file that will run the Minesweeper game
import Minesweeper as game
import Mine_Annihilation_Device as mad







mf = game.Minefield(1)
bot = mad.MAD()
bot.survey_minefield(mf)
bot.show_work()
mf.print_answer_minefield()


    