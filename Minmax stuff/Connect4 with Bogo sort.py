# IMPORT LIBRARIES
import pygame
import numpy as np
import random # for bogo sort :D

# Constants
Red = (255, 0, 0)  # for counter
Yellow = (255, 255, 0)  # for counter
Frame_Blue = (72, 160, 255)  # for the frame
Background_White = (255, 255, 255)


# classes to use:
# board(constructor(rows and columns), display, placepiece, checkifvalid) literally just the board!
# player (inputting a counter postion)
# game(checking for a win!, actually running stuff, taking in the moves--> implementing them)

class Board:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.Rows = dimensions[0] - 1

    def Create_Board(self):
        self.board = np.zeros(self.dimensions)

    def Display_Board(self):
        x = self.board
        print(x[::-1])

    def New_Place_Piece(self, playerturn):
        rowcount = 0
        PiecePlaced = False
        for rows in self.board:
            if not PiecePlaced:
                if rows[self.Column_Place] == 0:
                    self.Update_Board((rowcount, self.Column_Place), playerturn)
                    PiecePlaced = True
                    self.Update_row_place(rowcount)
            rowcount = rowcount + 1

    def Update_row_place(self, newPlace):
        self.Row_place = newPlace

    def Get_Row_Place(self):
        return self.Row_place

    def Update_Board(self, position, value):
        self.board[position] = value

    def Check_Column_Not_Full(self):
        if self.board[(self.Rows, self.Column_Place)] != 0:
            print("Move is invalid")
            return False
        else:
            return True

    def Check_Move_Valid(self):
        InBounds = self.CheckInBounds(0, self.Column_Place)
        if not InBounds:
            print("This isn't a column that exists, try again")
            return False
        FullColumn = self.Check_Column_Not_Full()
        if not FullColumn:
            print("Column is full, try again")
            return False
        if InBounds and FullColumn:
            print("move valid")
            return True

    def GetColumnPlace(self):
        return self.Column_Place

    def UpdateColumnPlace(self, column):
        self.Column_Place = column

    def CheckBoardFull(self):
        ZeroExists = False

        for row in self.board:
            for place in row:
                if place == 0:
                    ZeroExists = True

        if ZeroExists:
            return False
        elif not ZeroExists:
            print("Board is full")
            self.GameEnd = True
            return True

    def GetInSquare(self, RowToCheck, ColumnToCheck):
        return self.board[RowToCheck, ColumnToCheck]


    def CheckInBounds(self, Row, Column):  # Returns False if the cells are out of bounds, and True if it is fine
        if Row >= self.dimensions[0]:
            return False
        elif Row < 0:
            return False

        if Column >= self.dimensions[1]:
            return False
        elif Column < 0:
            return False

        else:
            return True

    def GetBoard(self):
        return self.board

    def GetDimensions(self):
        return self.dimensions



class Player:
    def __init__(self):
        self.playerturn = 1

    def Update_Turn(self):
        if self.playerturn == 1:
            self.playerturn = 2

        elif self.playerturn == 2:
            self.playerturn = 1

    def Get_Move(self):  # outputs the move that the player wants for other classes to use
        Correct_Input = False
        while not Correct_Input:
            try:
                mycolumn = int(input("Press number of the column you want to place it in, or '0' to go back a move: "))
                self.Column_Place = mycolumn - 1
                Correct_Input = True
            except:
                print("Enter an integer, try again!")

        return self.Column_Place

    def Get_Turn(self): # outputs the playerturn, for other classes to use
        return self.playerturn

    def AIBogoSort(self, dimensions):
        columns = dimensions[1]
        AIChoice = random.randint(1, columns)
        print("AI picked to place it in", AIChoice)
        self.Column_Place = AIChoice - 1
        return self.Column_Place

    def AIMinMax(self):
        print("OOOOH")


class Game:
    def __init__(self, dimensions):
        self.board = Board(dimensions)
        self.board.Create_Board()
        self.player = Player()
        self.MoveList = []
        self.GameEnd = False

    def Make_Move(self, turn):
        move = self.player.Get_Move()
        GoneBack = False
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
            mymove = self.board.GetColumnPlace() + 1
            self.Update_Move_List(mymove)

    def Update_Move_List(self, ValToAdd):  # NEED TO FIX THIS  - OUTPUT LIST IS TOO SMALL D:
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

            IgnoreValue = False
            ValueSkipped = False

            try:
                value = int(value)
            except:
                print("tried to do the value", '"' + str(value) + '"')
                print("Continuing with rest of input data")
                IgnoreValue = True
                ValueSkipped = True

            if not IgnoreValue:
                self.Column_Place = value - 1
                self.board.UpdateColumnPlace(self.Column_Place)

                if self.Column_Place == - 1: # works here!
                    self.GoBackMove()
                    self.board.Display_Board()
                    ValueSkipped = True

                elif not self.board.CheckInBounds(0, self.Column_Place): # works here!
                    print(value, "is not a valid column, skipping this!")
                    ValueSkipped = True



                if not ValueSkipped:
                    self.board.New_Place_Piece(self.player.Get_Turn())
                    self.Update_Move_List(value)
                    self.player.Update_Turn()
                    if self.CheckWin():
                        return True

            # print("\n Displaying board") # for debugging
            # print("gone around", times, "times") # for debugging
            # self.Display_Board() # for debugging
            # print("") # for debugging


        print("State Loaded")
        return True

    def CheckWin(self):
        self.CheckDiagonal_DL_to_UR()
        # print("Diagonal DL to UR Checked", self.GameEnd)
        if not self.GameEnd:
            self.CheckDiagonal_UL_to_DR()
            # print("Diagonal UL to DR checked", self.GameEnd)
        if not self.GameEnd:
            self.CheckVerticalLine()
            # print("Vertical Checked", self.GameEnd)
        if not self.GameEnd:
            self.CheckHorizontalLine()
            # print("Horizontal Checked", self.GameEnd)

    def CheckDiagonal_DL_to_UR(self):
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

        # print("amount of DL to UR in a row:", amountinrow)  # for debugging
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO DL-->UR")  # for debugging
        else:
            self.GameEnd = False

    def CheckDiagonal_UL_to_DR(self):  # no works :(
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

        # print("UL to DR amount in row:", amountinrow)  # for debugging
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO UL-->DR")  # for debugging
        else:
            self.GameEnd = False

    def CheckHorizontalLine(self):
        ValToCheckFor = self.board.GetInSquare(self.Row_place, self.Column_Place)
        SameThing = True
        amountinrow = 0

        # print("start position is", self.Row_place, self.Column_Place)  # for debugging
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

        # print("Horizontal amount in row", amountinrow)  # for debugging
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO HORIZONTAL")  # for debugging
        else:
            self.GameEnd = False

    def CheckVerticalLine(self):  # working!
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

        # print("Vertical amount in row:", amountinrow) # for debugging
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO VERTICAL")  # for debugging
        else:
            self.GameEnd = False

    def DisplayWinner(self):
        if (self.enemy == 1) and (self.player.Get_Turn() == 2):
            print("AI wins!")
        else:
            print("Player", self.player.Get_Turn(), "Wins!")

    def MoveListPop(self):
        poppedvalue = self.MoveList.pop()
        return poppedvalue

    def GoBackMove(self):
        if len(self.MoveList) == 0:
            print("Can't go back, no moves made!")
            return False

        PosToRemove = self.MoveListPop() - 1
        # print("column to Remove:", PosToRemove) # for debugging
        rowcount = 0

        for rows in self.board.GetBoard():
            # print("found", rows[PosToRemove], "at position", rowcount, PosToRemove) # for debugging
            if rows[PosToRemove] == 0:
                # print("Removed the value at", (rowcount-1), PosToRemove, "Value was", self.board[rowcount-1, PosToRemove]) # for debugging
                self.board.Update_Board((rowcount - 1, PosToRemove), 0)
                self.player.Update_Turn()
                return True
            rowcount += 1
            if rowcount == 6:
                self.board.Update_Board((rowcount - 1, PosToRemove), 0)
                self.player.Update_Turn()
                return True

    def DisplayMoves(self):
        print("list of moves(columns that it was placed in):", self.MoveList)

    def ChooseOpponent(self):
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
        if choice == 2:
            print("human enemy chosen")
        self.enemy = choice

    def AI_Make_Move(self, turn):
        move = self.player.AIBogoSort(self.board.dimensions)
        GoneBack = False
        if move == -1:
            GoneBack = self.GoBackMove()

        if GoneBack:
            return GoneBack
        else:
            self.board.UpdateColumnPlace(move)
            MoveValid = self.board.Check_Move_Valid()
            while not MoveValid:
                self.Column_Place = self.player.AIBogoSort(self.board.dimensions)
                self.board.UpdateColumnPlace(self.Column_Place)
                if self.Column_Place == -1:
                    GoneBack = self.GoBackMove()
                    return GoneBack

                MoveValid = self.board.Check_Move_Valid()
            self.board.New_Place_Piece(turn)
            mymove = self.board.GetColumnPlace() + 1
            self.Update_Move_List(mymove)

    def MainGame(self):
        LoadState = input("Would you like to load from a previous state? (y/n): ")
        self.board.Display_Board()
        print("Board displayed") # for debugging
        GameLoaded = False
        boardfull = False
        if LoadState == "y":  #
            while not GameLoaded:
                StateToLoad = input("Enter a list of the previous state to load: ")
                GameLoaded = self.LoadGame(StateToLoad)
                self.board.Display_Board()


        self.ChooseOpponent()


        while not self.GameEnd:
            playerturn = self.player.Get_Turn()
            print("It is your turn player", playerturn)
            if playerturn == 2 and self.enemy == 1:
                HasGoneBack = self.AI_Make_Move(playerturn)
            else:
                HasGoneBack = self.Make_Move(playerturn)
            if HasGoneBack:
                print("Gone back a move")
            else:
                self.CheckWin()
                self.player.Update_Turn()
            self.board.Display_Board()
            boardfull = self.board.CheckBoardFull()

        if boardfull:
            print("No one wins")
        elif self.GameEnd:
            self.player.Update_Turn()
            self.DisplayWinner()
            self.DisplayMoves()

    def TestCombos(self, RowOffset, ColumnStart, WhichTest):
        print("running test")
        CurrentRow = 0
        while CurrentRow != RowOffset:
            Column = 0
            currentboard = self.board.GetBoard()
            for value in currentboard[CurrentRow]:
                self.board.Update_Board((CurrentRow, Column), 5)
                Column += 1
            CurrentRow += 1
        if WhichTest == 1: # checks for DL to UR
            testdata = [1, 2, 2, 4, 4, 4, 4, 3, 3, 1, 3]
        elif WhichTest == 2: # checks for UL to DR
            testdata = [1, 1, 1, 1, 3, 3, 2, 4, 2, 2]
        elif WhichTest == 3: # testing for horizontal
            testdata = [1, 1, 2, 2, 3, 3, 4]
        elif WhichTest == 4: # testing for vertical
            testdata = [1, 2, 1, 2, 1, 2, 1]
        elif WhichTest == 5:
            testdata = [2, 1, 2, 1, 2, 1, 2]

        newtestdata = []
        for value in testdata:
            newtestdata.append(value + (ColumnStart - 1))
        newertestdata = str(newtestdata)
        IsCorrect = self.LoadGame(newertestdata)
        self.board.Display_Board()
        if IsCorrect:
            print("starting at", RowOffset, ColumnStart, "is working")
            output = "Working"
        else:
            output = "Not Working"
            raise Exception("NOT WORKING AT", RowOffset, ColumnStart)
        print("")
        return output


# TEST ALL COMBOS WORKING!!!!
def TestAllCombos(totrows, totcolumns):
    workinglist = []
    mydimensions = [totrows, totcolumns]
    for StartRow in range(0, totrows - 3): # using for DL to UR
        for StartColumn in range(1,totcolumns - 2):
            rungame = Game(mydimensions)
            workinglist.append(rungame.TestCombos(StartRow, StartColumn, 1))
    print("END OF DL->UR TESTING")

    for StartRow in range(0, totrows - 3): # using for UL to DR
        for StartColumn in range(1,totcolumns - 2):
            rungame = Game(mydimensions)
            workinglist.append(rungame.TestCombos(StartRow, StartColumn, 2))
    print("END OF UL->DR TESTING")

    for StartRow in range(0, totrows): # using for Horizontal
        for StartColumn in range(1,totcolumns - 2):
            rungame = Game(mydimensions)
            workinglist.append(rungame.TestCombos(StartRow, StartColumn, 3))
    print("END OF HORIZONTAL TESTING")

    for StartRow in range(0, totrows - 3): # using for Vertical
        for StartColumn in range(1,totcolumns):
            rungame = Game(mydimensions)
            workinglist.append(rungame.TestCombos(StartRow, StartColumn, 4))

    for StartRow in range(0, totrows - 3): # testing end column
        StartColumn = totcolumns -1
        rungame = Game(mydimensions)
        workinglist.append(rungame.TestCombos(StartRow, StartColumn, 5))

    print("END OF VERTICAL TESTING")

    amountofhorizontal = (totrows * (totcolumns-3))
    print(amountofhorizontal, "horizontal things")  # should be right

    amountofvertical = (totcolumns * (totrows - 3))
    print(amountofvertical, "vertical things") # should be right

    amountofULDL = 2*((totcolumns-3) * (totrows-3))
    print(amountofULDL, "ULDL things") # should be right
    x = amountofhorizontal + amountofvertical + amountofULDL
    print("should have:", x ,"things working")
    print(len(workinglist), "things working")

def MainGame():
    HaveValue = False
    while not HaveValue:
        try:
            rows = int(input("enter how many rows you want there to be(normally 6):"))
            columns = int(input("enter how many rows you want there to be(normally 7):"))
            HaveValue = True
        except:
            print("I require an integer, try again")

    mydimensions = [rows, columns]
    rungame = Game(mydimensions)
    #TestAllCombos(rows,columns)
    rungame.MainGame()
    print("end of Game!")

MainGame()
# I also need to implement the minmax into it
# connect 4 game is working! - i think? - need to now interface it using pygame
# make it work with the keyboard button presses?

# Krish wants me to add previous games(aka NOT FROM CODE THING) - tf is this gonna work?!


class pygam_interface:
    def __init__(self, dimensions, frame_colour, p1_colour, p2_colour, Background_colour):
        self.dimensions = dimensions
        self.FrameColour = frame_colour
        self.p1Colour = p1_colour
        self.p2Colour = p2_colour
        self.BackgroundColour = Background_colour





