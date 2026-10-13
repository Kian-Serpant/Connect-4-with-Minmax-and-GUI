# IMPORT LIBRARIES
from Game import Game

def PlayGame():
    '''
    This will take the rows and columns from the user, making sure the values are small enough that there are still
    enough pixels in order to display the board, and also making sure that there are 1 or more rows and columns, in
    order to make sure that the game can actually be "played". It then feeds these parameters to create an instance of
    the Game class, after which it will then run MainGame in order to actually play the game.
    '''
    HaveValue = False
    while not HaveValue:
        try:
            rows = int(input("enter how many rows you want there to be(this is the height, standard size is 6):"))
            columns = int(input("enter how many columns you want there to be(this is the width, standard size is 7):"))
            HaveValue = True
            if rows > 240:
                HaveValue = False
                print("Too many rows, you can't see that many")
            if columns > 280:
                HaveValue = False
                print("Too many columns, you can't see that many")
            if (rows < 1) or (columns < 1):
                HaveValue = False
                print("Can't either rows or columns be 0 or less")
        except:
            print("I require an integer, try again")

    mydimensions = [rows, columns]
    TerminalGame = False
    PlayTerminal = input("Would you like to play in terminal? y for yes: ")
    if PlayTerminal == "y":
        TerminalGame = True

    rungame = Game(mydimensions, TerminalGame)
    rungame.MainGame()

    print("end of Game!")


PlayGame()





