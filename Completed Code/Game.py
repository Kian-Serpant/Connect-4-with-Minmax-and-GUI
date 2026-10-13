# IMPORT LIBRARIES
from Display import Display
from Board import Board
from Player import Player
from Writer import Writer


class Game:
    def __init__(self, dimensions, TerminalGame):
        self.board = Board(dimensions)
        if not TerminalGame:
            self.displayer = Display(dimensions)
        self.board.Create_Board()
        self.player = Player()
        self.MoveList = []
        self.GameEnd = False
        self.TerminalGame = TerminalGame
        self.writer = Writer("PreviousGames")

    def Make_Move(self, turn, HumPlayer="yes"):
        '''
        This code is for if the player wants to play in the terminal instead of with a display.
        This will take in the turn, and a parameter called HumPlayer. If it is the AI move, HumPlayer is input as the
        column that the AI wants to play in. It will then place it in that column. If the player is human, then it will
        get a move from the player, and then do it.
        This is also used for the AI to test different game states, so that it can make moves, then evaluate the position
        and the moves that could come from playing certain things.
        '''
        try:
            temp = int(HumPlayer)
            isHuman = False
        except:
            isHuman = True

        if isHuman:
            move = self.player.Get_Move()

        else:
            move = HumPlayer
        GoneBack = False
        while move == -2:
            self.DisplayMoves()
            move = self.player.Get_Move()
        if move == -1:
            GoneBack = self.GoBackMove()


        if GoneBack:
            return GoneBack
        else:
            self.board.UpdateColumnPlace(move)
            MoveValid = self.board.Check_Move_Valid()
            while not MoveValid:
                self.Column_Place = self.player.Get_Move()
                self.board.UpdateColumnPlace(self.Column_Place)
                if self.Column_Place == -1:
                    GoneBack = self.GoBackMove()
                    return GoneBack

                MoveValid = self.board.Check_Move_Valid()
            self.board.New_Place_Piece(turn)
            Themove = self.board.GetColumnPlace() + 1
            self.Update_Move_List(Themove)
            self.MoveMade = Themove

    def Display_Make_Move(self, turn, NextPosition):
        '''
        This is an adaptation of Make_Move, which it will use the pygame display in order to get a move for the human.
        If it is an AI, then this won't be run. After getting the position, it will then check if that move is alright
        if the move is not alright, it will get the player to play again. It will also go back a move if the player
        wants to go back a move. If the player is playing against an AI, it will go back two moves, or until the last
        move of the player, otherwise the AI just plays the same move again.
        '''
        Column = self.displayer.GetPlacement(turn, NextPosition, self.enemy) - 1
        while (len(self.MoveList) == 0) and (Column == -1):
            print("Try again")
            Column = self.displayer.GetPlacement(turn, NextPosition, self.enemy) - 1

        if Column == -1:
            SameColumn = False
            firstMoveRemove = self.MoveList[-1]
            GoneBackMove = True
            self.displayer.PlaceCounter(NextPosition, self.MoveList[-1] - 1, 3)
            self.GoBackMove()
            if self.enemy == 1: # for if against AI, it will go back 2 moves
                if firstMoveRemove == self.MoveList[-1]:
                    SameColumn = True
                self.displayer.PlaceCounter(NextPosition, self.MoveList[-1] - 1, 3, SameColumn)
                self.GoBackMove()
        else:
            GoneBackMove = False
            self.board.UpdateColumnPlace(Column)

            MoveValid = self.board.Check_Move_Valid()
            while not MoveValid:
                print("You can't place it there!")
                self.Column_Place = self.displayer.GetPlacement(turn, NextPosition, self.enemy) - 1
                self.board.UpdateColumnPlace(self.Column_Place)
                if self.Column_Place == -1:
                    self.GoBackMove()
                    GoneBackMove = True

                MoveValid = self.board.Check_Move_Valid()
            self.player.UpdateColumnPlace(Column)
            self.board.New_Place_Piece(turn)
            Themove = self.board.GetColumnPlace() + 1
            self.Update_Move_List(Themove)
            self.MoveMade = Themove

        return GoneBackMove

    def Update_Move_List(self, ValToAdd):
        '''
        This will take in a parameter of ValToAdd, which is the last move made. It will then append it to the list of
        moves that have been made so far.
        '''
        self.MoveList.append(ValToAdd)

    def LoadGame(self, PrevState):
        '''
        This will load in whatever is input as the parameter PrevState. It will then remove and brackets and spaces so
        that it can be turned into a list. After doing so, it will turn it into a list by splitting it at the commas.
        It will then iterate through this newly created list and play each move input in each column.
        '''
        previousState = PrevState
        UpdateList = previousState.strip("[")
        UpdateList = UpdateList.strip("]")
        UpdateList = UpdateList.strip(")")
        UpdateList = UpdateList.strip("(")
        UpdateList = UpdateList.replace(" ", "")
        StateList = UpdateList.split(",")


        for value in StateList:

            ValueSkipped = False

            try:
                value = int(value)

                self.Column_Place = value - 1
                NextPosition = self.board.GetNextColumnCell()
                CurrentRow = NextPosition[self.Column_Place][0]
                self.displayer.PlaceCounter(NextPosition, value-1, self.player.Get_Turn())
                self.board.UpdateColumnPlace(self.Column_Place)


                if self.Column_Place == - 1:
                    self.displayer.PlaceCounter(NextPosition, self.MoveList[-1] - 1, 3)
                    self.GoBackMove()
                    ValueSkipped = True

                elif not self.board.CheckInBounds(CurrentRow - 1, self.Column_Place):
                    print(value, "is not a valid column to place in right now, skipping this!")
                    ValueSkipped = True



                if not ValueSkipped:
                    self.board.New_Place_Piece(self.player.Get_Turn())
                    self.Update_Move_List(value)
                    self.player.Update_Turn()
                    if self.CheckWin():
                        return True
            except:
                print("tried to do the value", '"' + str(value) + '"')
                print("Continuing with rest of input data")

        print("State Loaded")
        return True

    def CheckWin(self):
        '''
        This will call all of the check functions, and will run them. If any of the check's are true, aka if the someone
        has won, then it will return True. If none of them return True, then CheckWin will return False, indicating that
        the current state is not a winning one.
        '''
        OutVal = self.CheckDiagonal_DL_to_UR()
        if OutVal:
            return True

        OutVal = self.CheckDiagonal_UL_to_DR()
        if OutVal:
            return True

        OutVal = self.CheckVerticalLine()
        if OutVal:
            return True

        OutVal = self.CheckHorizontalLine()
        if OutVal:
            return True

        return False

    def CheckDiagonal_DL_to_UR(self):
        '''
        This will check if the current position forms a diagonal line that goes upwards and to the right(or downwards to
        the left). It will check if the move is either in the middle of the line, or at the end of the line. It works by
        checking down left of the move, and up right of the move, and if any combination of these add up to there being
        4(or more) in a row, then it will return True, indicating a player has won. Otherwise it will return False,
        indicating that no winning combination has been found in this way.
        '''
        self.Row_place = self.board.Get_Row_Place()
        self.Column_Place = self.board.GetColumnPlace()
        ValToCheckFor = self.board.GetInSquare(self.Row_place, self.Column_Place)
        SameThing = True
        amountinrow = 0

        for valuepos in range(0, 4):
            updatedrow = self.Row_place + valuepos
            updatedcolumn = self.Column_Place + valuepos

            if self.board.CheckInBounds(updatedrow, updatedcolumn):
                if self.board.GetInSquare(updatedrow, updatedcolumn) != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1, 5):
            updatedrow2 = self.Row_place - valuepos
            updatedcolumn2 = self.Column_Place - valuepos

            if self.board.CheckInBounds(updatedrow2, updatedcolumn2):
                if self.board.GetInSquare(updatedrow2, updatedcolumn2) != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        if amountinrow >= 4:
            self.GameEnd = True
            return True
        else:
            self.GameEnd = False
            return False

    def CheckDiagonal_UL_to_DR(self):
        '''
        This will check if the current position forms a diagonal line that goes downwards and to the left(or upwards to
        the right). It will check if the move is either in the middle of the line, or at the end of the line. It works by
        checking down right of the move, and up left of the move, and if any combination of these add up to there being
        4(or more) in a row, then it will return True, indicating a player has won. Otherwise it will return False,
        indicating that no winning combination has been found in this way.
        '''
        ValToCheckFor = self.board.GetInSquare(self.Row_place, self.Column_Place)
        SameThing = True
        amountinrow = 0

        for valuepos in range(0, 4):
            updatedrow = self.Row_place + valuepos
            updatedcolumn = self.Column_Place - valuepos

            if self.board.CheckInBounds(updatedrow, updatedcolumn):
                if self.board.GetInSquare(updatedrow, updatedcolumn) != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1, 5):
            updatedrow2 = self.Row_place - valuepos
            updatedcolumn2 = self.Column_Place + valuepos

            if self.board.CheckInBounds(updatedrow2, updatedcolumn2):
                if self.board.GetInSquare(updatedrow2, updatedcolumn2) != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        if amountinrow >= 4:
            self.GameEnd = True
            return True
        else:
            self.GameEnd = False
            return False

    def CheckHorizontalLine(self):
        '''
        This will check if the current position forms a horizontal line that wins. It will check if the move is either
        in the middle of the line, or at the end of the line. It works by checking to the left and right of the move,
        and if any combination of these add up to there being 4(or more) in a row, then it will return True, indicating
        a player has won. Otherwise it will return False, indicating that no winning combination has been found in this
        way.
        '''
        ValToCheckFor = self.board.GetInSquare(self.Row_place, self.Column_Place)
        SameThing = True
        amountinrow = 0

        for valuepos in range(0, 4):
            newColumn = self.Column_Place + valuepos

            if self.board.CheckInBounds(self.Row_place, newColumn):
                if self.board.GetInSquare(self.Row_place, newColumn) != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1, 5):
            newNegColumn = self.Column_Place - valuepos

            if self.board.CheckInBounds(self.Row_place, newNegColumn):
                if self.board.GetInSquare(self.Row_place, newNegColumn) != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        if amountinrow >= 4:
            self.GameEnd = True
            return True
        else:
            self.GameEnd = False
            return False

    def CheckVerticalLine(self):
        '''
        This will check if the current position forms a vertical line that wins. It will check if the move is either
        in the middle of the line, or at the end of the line. It works by checking above and below the move, and if any
        combination of these add up to there being 4(or more) in a row, then it will return True, indicating a player
        has won. Otherwise it will return False, indicating that no winning combination has been found in this way.
        '''
        ValToCheckFor = self.board.GetInSquare(self.Row_place, self.Column_Place)
        SameThing = True
        amountinrow = 0

        for valuepos in range(0, 4):
            newRow = self.Row_place + valuepos
            if self.board.CheckInBounds(newRow, self.Column_Place):
                if self.board.GetInSquare(newRow, self.Column_Place) != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1, 5):
            newNegRow = self.Row_place - valuepos
            if self.board.CheckInBounds(newNegRow, self.Column_Place):
                if self.board.GetInSquare(newNegRow, self.Column_Place) != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        if amountinrow >= 4:
            self.GameEnd = True
            return True
        else:
            self.GameEnd = False
            return False

    def DisplayWinner(self, turn):
        '''
        This will take in a parameter of whose turn it is. If the enemy is 1(representing AI), and player 2 wins(AI),
        then it will say that the AI wins. Otherwise, it will print and display which player wins.
        '''
        if (self.enemy == 1) and (turn == 2):
            print("AI wins!")
        else:
            print("Player", self.player.Get_Turn(), "Wins!")

    def MoveListPop(self):
        '''
        This will pop the last value off of the moves made, and will return it.
        '''
        poppedvalue = self.MoveList.pop()
        return poppedvalue

    def GoBackMove(self):
        '''
        This will check if moves have been played. If no moves have been made, then it will tell the player it can't go
        back and will return False, indicating this. If moves have been made, then it will take the last move off the
        movelist. After doing so, it will then iterate through each row in the board. If it finds that the value at the
        position of one above the popped move is empty, then it will update the board state, so that it has gone back.
        If it doesn't find a move there, then it will continue going through the rows, and will check the other columns.
        If it reaches the last row, then it will undo move in the top row.
        '''
        if len(self.MoveList) == 0:
            print("Can't go back, no moves made!")
            return False

        PosToRemove = self.MoveListPop() - 1
        rowcount = 0

        amountofrows = (self.board.GetDimensions())[0]
        for rows in self.board.GetBoard():
            if rows[PosToRemove] == 0:
                self.board.Update_Board((rowcount - 1, PosToRemove), 0)
                self.player.Update_Turn()
                return True
            rowcount += 1
            if rowcount == amountofrows:
                self.board.Update_Board((rowcount - 1, PosToRemove), 0)
                self.player.Update_Turn()
                return True

    def DisplayMoves(self):
        '''
        This will print a list of moves that have been made so far, and display it in terminal. This is useful in case
        the player wants to continue a game later.
        '''
        print("list of moves(columns that it was placed in):", self.MoveList)

    def ChooseOpponent(self):
        '''
        This will get the user to input whether they want to play against an AI, or a human. It will keep asking the
        user until they enter a choice. If the user chooses to play against an AI, then it will ask the user to enter a
        depth they want the AI to be. This is equivalent to picking the difficulty, with the difficulty being exponential
        It will also get the player to decide whether to play first, or if they want the AI to play first if an AI enemy
        is chosen.
        '''
        choice = 0
        isvalidinteger = False
        while not isvalidinteger:
            integerchosen = False
            while not integerchosen:
                try:
                    choice = int(input("enter an opponent, 1 for AI, 2 for human enemy:"))
                    integerchosen = True
                except:
                    print("try again, enter an integer")
            if choice == 1 or choice == 2:
                isvalidinteger = True
            else:
                print("need 1 or 2 as the integer input")


        if choice == 1:
            print("AI enemy chosen")
            integerchosen = False
            while not integerchosen:
                try:
                    depth = int(input("Enter a depth of moves you want the AI to go to(higher number is harder, but will also take longer)"))
                    integerchosen = True
                except:
                    print("try again, enter an integer")

            self.AI_Depth = depth

            WhoGoesFirst = input("Do you want to go first, y for yes: ")
            if WhoGoesFirst != "y":
                self.player.Update_Turn()

        if choice == 2:
            print("human enemy chosen")
        self.enemy = choice

        print("")

    def AI_Make_Move(self, turn):
        '''
        This will take in the turn, and will call the function for the AI to pick a move from the player class. After
        doing so, it will then play that move by placing it on the board. If, for whatever reason, the AI chooses to go
        back a move(which shouldn't be possible), then it will go back a move. It will then add whatever move is made
        to the movelist, and it will also update MoveMade
        '''
        move = self.player.NEWAI_Get_Move(self.board.dimensions, self.board.GetTotalScoreBoard(), self, self.board, self.AI_Depth)
        NextPosition = self.board.GetNextColumnCell()
        GoneBack = False
        if move == -1:
            if not self.TerminalGame:
                self.displayer.PlaceCounter(NextPosition, self.MoveList[-1] - 1, 3)
            self.GoBackMove()
            GoneBack = self.GoBackMove()

        if GoneBack:
            return GoneBack

        else:
            self.board.UpdateColumnPlace(move)
            self.board.New_Place_Piece(turn)
            if not self.TerminalGame:
                self.displayer.PlaceCounter(NextPosition, move, turn)
            mymove = self.board.GetColumnPlace() + 1
            self.Update_Move_List(mymove)
        self.MoveMade = move + 1


    def SaveGame(self, BoardFull):
        '''
        This will save the game to a file, alongside if it was played against an AI, Who won, and the depth
        '''
        if self.enemy == 1:
            PlayedAgainst = "the AI at depth of " + str(self.AI_Depth)
            if self.player.Get_Turn() == 2:
                Winner = "the AI"
            else:
                Winner = "Human Player"
        else:
            PlayedAgainst = "a Human"
            Winner = "player " + str(self.player.Get_Turn())

        if BoardFull:
            self.writer.WriteFile(self.MoveList, (" - Ended due to Board being full, played against " + PlayedAgainst))
        else:
            self.writer.WriteFile(self.MoveList, (" - Ended due to " + Winner + " winning, played against " + PlayedAgainst))

    def MainGame(self):
        '''
        MainGame will do numerous things. First it checks if the player would like to load a game, and if they do, then
        it will display the board, get the game to load in, load in said game, and then display the board after loading
        in the game. After doing this, it will then run get the opponent from the player. It will then continuously run
        through a loop until the GameEnd condition is True. This loop will get the player to make a move, or the AI to
        make a move dependent on which player's turn it is. After doing so, it will then check if either player has won
        and then update the turn. Then the Board is displayed, and the move made is printed in terminal. It will then
        also check for if the board is full, if it is, GameEnd is set to True. After exiting the loop, it will first
        check if either player has won. If they have, it will print the winner, print the moves made, and then display
        the winner on the interface. If this condition is not met, and the board is full, then it will print that the
        board was full, and display this message on the interface.
        '''
        PlayerWon = False
        LoadState = input("Would you like to load from a previous state? (y/n): ")
        self.board.Display_Board()
        self.board.GetTotalScoreBoard()
        GameLoaded = False
        boardfull = False

        self.ChooseOpponent()

        if LoadState == "y":
            while not GameLoaded:
                StateToLoad = input("Enter a list of the previous state to load: ")
                GameLoaded = self.LoadGame(StateToLoad)
                self.board.Display_Board()


        while not self.GameEnd:
            NextPosition = self.board.GetNextColumnCell()
            playerturn = self.player.Get_Turn()
            if playerturn == 2 and self.enemy == 1:
                HasGoneBack = self.AI_Make_Move(playerturn)
            else:
                print("It is your turn player", playerturn, "Press R to go back moves")
                if self.TerminalGame:
                    HasGoneBack = self.Make_Move(playerturn, NextPosition)
                    if HasGoneBack and (self.enemy == 1): # for if playing against an AI in terminal
                        self.GoBackMove()
                else:
                    HasGoneBack = self.Display_Make_Move(playerturn, NextPosition)
            if HasGoneBack:
                print("Gone back a move")
            else:
                PlayerWon = self.CheckWin()
                self.player.Update_Turn()
            self.board.Display_Board()
            print("Move made was:", self.MoveMade)
            boardfull = self.board.CheckBoardFull()
            if boardfull:
                self.GameEnd = True
            print("\n")

        if PlayerWon:
            self.player.Update_Turn()
            self.DisplayWinner(playerturn)
            self.SaveGame(False)
            self.DisplayMoves()
            if not self.TerminalGame:
                self.displayer.GameOver(playerturn)

        elif boardfull:
            print("No one wins")
            self.SaveGame(True)
            if not self.TerminalGame:
                self.displayer.GameOver(5) # tells players the game has ended

