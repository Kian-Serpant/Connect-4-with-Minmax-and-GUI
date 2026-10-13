# IMPORT LIBRARIES
import pygame
import numpy as np

# Constants
Red = (255, 0, 0)  # for counter
Yellow = (255, 255, 0)  # for counter
Frame_Blue = (72, 160, 255)  # for the frame
Background_White = (255, 255, 255)

Rows = 6
Columns = 7

# classes to use:
# board(constructor(rows and columns), display, placepiece, checkifvalid) literally just the board!
# player (inputting a counter postion)
# game(checking for a win!, actually running stuff, taking in the moves--> implementing them)

class Game:

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.Rows = dimensions[0] - 1
        self.playerturn = 1  # player 1 is "r" and player 2 is "y"
        self.GameEnd = False
        self.MoveList = []
        pygame.init()

    def Create_Board(self):
        self.board = np.zeros(self.dimensions)

    def Update_Turn(self):
        if self.playerturn == 1:
            self.playerturn = 2

        elif self.playerturn == 2:
            self.playerturn = 1

    def Display_Board(self):
        x = self.board
        print(x[::-1])

    def Get_Move_WKeyboard(self):  # need to test - this is for pygame interfacing
        print("Press number of the column you want to place it in")
        NeedMove = True
        while NeedMove:  # runs until a column to place it in is pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                self.Column_Place = 0
                NeedMove = False
            elif keys[pygame.K_2]:
                self.Column_Place = 1
                NeedMove = False
            elif keys[pygame.K_3]:
                self.Column_Place = 2
                NeedMove = False
            elif keys[pygame.K_4]:
                self.Column_Place = 3
                NeedMove = False
            elif keys[pygame.K_5]:
                self.Column_Place = 4
                NeedMove = False
            elif keys[pygame.K_6]:
                self.Column_Place = 5
                NeedMove = False
            elif keys[pygame.K_7]:
                self.Column_Place = 6
                NeedMove = False

    def Get_Move(self):  # working
        Correct_Input = False
        while not Correct_Input:
            try:
                mycolumn = int(input("Press number of the column you want to place it in, or '0' to go back a move: "))
                self.Column_Place = mycolumn - 1
                Correct_Input = True
            except:
                print("Enter an integer, try again!")

    def Check_Column_Not_Full(self):
        if self.board[(self.Rows, self.Column_Place)] != 0:  # does row then column
            print("Move is invalid")
            return False
        else:
            return True

    # place Piece is old - delete / use for things that I have tried
    def Place_Piece(self):
        rowcount = self.dimensions[0] - 1
        for row in self.board:
            # debugging
            print("")
            print("Rowcount", rowcount)
            print("Playerturn:", self.playerturn, "type:", type(self.playerturn))
            print("HERE IS MY LOCATION", rowcount, self.Column_Place)
            print("HERE IS MY VALUE", row[self.Column_Place])

            if rowcount != -1:
                if row[self.Column_Place] != 0:
                    self.Row_place = 5 - rowcount
                    print("Row place:", self.Row_place)
                    if self.playerturn == 1:
                        self.board[rowcount, self.Column_Place] = "2"
                    elif self.playerturn == 0:
                        self.board[rowcount, self.Column_Place] = "1"
                    else:
                        self.board[rowcount, self.Column_Place] = "?"
                    rowcount = 1

            rowcount = rowcount - 1
            if rowcount == -1:
                self.Row_place = 5
                if self.playerturn == 1:
                    self.board[5, self.Column_Place] = "2"
                elif self.playerturn == 0:
                    self.board[5, self.Column_Place] = "1"
                else:
                    self.board[0, self.Column_Place] = "?"

    def New_Place_Piece(self):
        rowcount = 0
        PiecePlaced = False
        for rows in self.board:
            if not PiecePlaced:
                if rows[self.Column_Place] == 0:
                    self.Update_Board((rowcount, self.Column_Place), self.playerturn)
                    PiecePlaced = True
                    self.Update_row_place(rowcount)
            rowcount = rowcount + 1

    def Update_row_place(self, newPlace):
        self.Row_place = newPlace

    def Update_Board(self, position, value):
        self.board[position] = value

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

    def Make_Move(self):
        self.Get_Move()
        GoneBack = False
        if self.Column_Place == -1:
            GoneBack = self.GoBackMove()

        if GoneBack:
            return GoneBack
        else:
            MoveValid = self.Check_Move_Valid()
            while not MoveValid:
                self.Get_Move()
                if self.Column_Place == -1:
                    GoneBack = self.GoBackMove()
                    return GoneBack

                MoveValid = self.Check_Move_Valid()
            self.New_Place_Piece()
            mymove = self.Column_Place + 1
            self.Update_Move_List(mymove)

    def Update_Move_List(self, ValToAdd):  # NEED TO FIX THIS  - OUTPUT LIST IS TOO SMALL D:
        self.MoveList.append(ValToAdd)

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

    def CheckDiagonal_DL_to_UR(self):  # Works
        ValToCheckFor = self.board[self.Row_place, self.Column_Place]
        SameThing = True
        amountinrow = 0

        for valuepos in range(0, 4):
            updatedrow = self.Row_place + valuepos
            updatedcolumn = self.Column_Place + valuepos

            if self.CheckInBounds(updatedrow, updatedcolumn):
                if self.board[updatedrow, updatedcolumn] != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1, 5):
            updatedrow2 = self.Row_place - valuepos
            updatedcolumn2 = self.Column_Place - valuepos

            if self.CheckInBounds(updatedrow2, updatedcolumn2):
                if self.board[updatedrow2, updatedcolumn2] != ValToCheckFor:
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
        ValToCheckFor = self.board[self.Row_place, self.Column_Place]
        SameThing = True
        amountinrow = 0

        for valuepos in range(0, 4):
            updatedrow = self.Row_place + valuepos
            updatedcolumn = self.Column_Place - valuepos

            if self.CheckInBounds(updatedrow, updatedcolumn):
                if self.board[updatedrow, updatedcolumn] != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1, 5):
            updatedrow2 = self.Row_place - valuepos
            updatedcolumn2 = self.Column_Place + valuepos

            if self.CheckInBounds(updatedrow2, updatedcolumn2):
                if self.board[updatedrow2, updatedcolumn2] != ValToCheckFor:
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
        ValToCheckFor = self.board[self.Row_place, self.Column_Place]
        SameThing = True
        amountinrow = 0

        # print("start position is", self.Row_place, self.Column_Place)  # for debugging
        for valuepos in range(0, 4):
            newColumn = self.Column_Place + valuepos

            if self.CheckInBounds(self.Row_place, newColumn):
                if self.board[self.Row_place, newColumn] != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1, 5):
            newNegColumn = self.Column_Place - valuepos

            if self.CheckInBounds(self.Row_place, newNegColumn):
                if self.board[self.Row_place, newNegColumn] != ValToCheckFor:
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
        ValToCheckFor = self.board[self.Row_place, self.Column_Place]
        SameThing = True
        amountinrow = 0

        for valuepos in range(0, 4):
            newRow = self.Row_place + valuepos
            if self.CheckInBounds(newRow, self.Column_Place):
                if self.board[newRow, self.Column_Place] != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1, 5):
            newNegRow = self.Row_place - valuepos
            if self.CheckInBounds(newNegRow, self.Column_Place):
                if self.board[newNegRow, self.Column_Place] != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        # print("Vertical amount in row:", amountinrow) # for debugging
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO VERTICAL")  # for debugging
        else:
            self.GameEnd = False

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

                if self.Column_Place == - 1: # works here!
                    self.GoBackMove()
                    self.Display_Board()
                    ValueSkipped = True

                elif not self.CheckInBounds(0, self.Column_Place): # works here!
                    print(value, "is not a valid column, skipping this!")
                    ValueSkipped = True



                if not ValueSkipped:
                    self.New_Place_Piece()
                    self.Update_Move_List(value)
                    self.Update_Turn()
                    if self.CheckWin():
                        return True

            # print("\n Displaying board") # for debugging
            # print("gone around", times, "times") # for debugging
            # self.Display_Board() # for debugging
            # print("") # for debugging


        print("State Loaded")
        return True

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

        for rows in self.board:
            # print("found", rows[PosToRemove], "at position", rowcount, PosToRemove) # for debugging
            if rows[PosToRemove] == 0:
                # print("Removed the value at", (rowcount-1), PosToRemove, "Value was", self.board[rowcount-1, PosToRemove]) # for debugging
                self.Update_Board((rowcount - 1, PosToRemove), 0)
                self.Update_Turn()
                return True
            rowcount += 1
            if rowcount == 6:
                self.Update_Board((rowcount - 1, PosToRemove), 0)
                self.Update_Turn()
                return True

    def DisplayMoves(self):
        print("list of moves(columns that it was placed in):", self.MoveList)

    def DisplayWinner(self):
        print("Player", self.playerturn, "Wins!")

    def MainGame(self):
        LoadState = input("Would you like to load from a previous state? (y/n): ")
        self.Create_Board()
        self.Display_Board()
        GameLoaded = False
        boardfull = False
        if LoadState == "y":  #
            while not GameLoaded:
                StateToLoad = input("Enter a list of the previous state to load: ")
                GameLoaded = self.LoadGame(StateToLoad)
                self.Display_Board()

        while not self.GameEnd:
            print("It is your turn player", self.playerturn)
            HasGoneBack = self.Make_Move()
            if HasGoneBack:
                print("Gone back a move")
            else:
                self.CheckWin()
                self.Update_Turn()
            self.Display_Board()
            boardfull = self.CheckBoardFull()

        if boardfull:
            print("No one wins")
        elif self.GameEnd:
            self.Update_Turn()
            self.DisplayWinner()
            self.DisplayMoves()

    # TESTER FOR ALL COMBOS! - add into testing section!
    def TestCombos(self, RowOffset, ColumnStart, WhichTest):
        print("running test")
        self.Create_Board()
        CurrentRow = 0
        while CurrentRow != RowOffset:
            Column = 0
            for value in self.board[CurrentRow]:
                self.Update_Board((CurrentRow, Column), 5)
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

        newtestdata = []
        for value in testdata:
            newtestdata.append(value + (ColumnStart - 1))
        newertestdata = str(newtestdata)
        IsCorrect = self.LoadGame(newertestdata)
        self.Display_Board()
        if IsCorrect:
            print("starting at", RowOffset, ColumnStart, "is working")
        else:
            raise Exception("NOT WORKING AT", RowOffset, ColumnStart)
        print("")



# connect 4 game is working! - i think? - need to now interface it using pygame
# I also need to implement the minmax into it
# make it work with the keyboard button presses?

# Place_Piece needs to be removed for final version - it is old code that didn't work - I changed it to fix file

# Krish wants me to add previous games(aka NOT FROM CODE THING) - tf is this gonna work?!

class pygam_interface:
    def __init__(self, dimensions, frame_colour, p1_colour, p2_colour, Background_colour):
        self.dimensions = dimensions
        self.FrameColour = frame_colour
        self.p1Colour = p1_colour
        self.p2Colour = p2_colour
        self.BackgroundColour = Background_colour

# Code the interface last!!!

Dimensions = [Rows, Columns]
mytestgame = Game(Dimensions)

# TEST ALL COMBOS WORKING!!!!
def TestAllCombos():
    for StartRow in range(0, 4): # using for DL to UR
        for StartColumn in range(1,5):
            mytestgame.TestCombos(StartRow, StartColumn, 1)

    for StartRow in range(0, 4): # using for UL to DR
        for StartColumn in range(1,5):
            mytestgame.TestCombos(StartRow, StartColumn, 2)

    for StartRow in range(0, 6): # using for Horizontal
        for StartColumn in range(1,5):
            mytestgame.TestCombos(StartRow, StartColumn, 3)

    for StartRow in range(0, 4): # using for Vertical
        for StartColumn in range(1,7):
            mytestgame.TestCombos(StartRow, StartColumn, 4)


mytestgame.MainGame()
