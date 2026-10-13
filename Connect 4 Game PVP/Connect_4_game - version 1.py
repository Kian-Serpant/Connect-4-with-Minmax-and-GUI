# IMPORT LIBRARIES
import pygame
import numpy as np



# Constants
Red = (255, 0, 0) # for counter
Yellow = (255, 255, 0) # for counter
Frame_Blue = (72, 160, 255) # for the frame
Background_White = (255,255,255)

Rows = 6
Columns = 7

class Game:

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.Rows = dimensions[0] - 1
        self.playerturn = 1 # player 1 is "r" and player 2 is "y"
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

    def Get_Move_WKeyboard(self): # need to test - this is for pygame interfacing
        print("Press number of the column you want to place it in")
        NeedMove = True
        while NeedMove: # runs until a column to place it in is pressed
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

    def Get_Move(self): # working
        Correct_Input = False
        while not Correct_Input:
            try:
                mycolumn = int(input("Press number of the column you want to place it in: "))
                self.Column_Place = mycolumn - 1
                Correct_Input = True
            except:
                print("Enter an integer, try again!")

    def Check_Column_Not_Full(self):
        if self.board[(self.Rows, self.Column_Place)] != 0: # does row then column
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
                    self.Row_place = 5-rowcount
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
        MoveValid = self.Check_Move_Valid()
        while not MoveValid:
            self.Get_Move()
            MoveValid = self.Check_Move_Valid()
        self.New_Place_Piece()
        mymove = self.Column_Place + 1
        self.Update_Move_List(mymove)

    def Update_Move_List(self, ValToAdd): # NEED TO FIX THIS  - OUTPUT LIST IS TOO SMALL D:
        self.MoveList.append(ValToAdd)

    def CheckWin(self):
        self.CheckDiagonal_DL_to_UR()
        #print("Diagonal DL to UR Checked", self.GameEnd)
        if not self.GameEnd:
            self.CheckDiagonal_UL_to_DR()
            #print("Diagonal UL to DR checked", self.GameEnd)
        if not self.GameEnd:
            self.CheckVerticalLine()
            #print("Vertical Checked", self.GameEnd)
        if not self.GameEnd:
            self.CheckHorizontalLine()
            #print("Horizontal Checked", self.GameEnd)

    def CheckInBounds(self, Row, Column): # Returns False if the cells are out of bounds, and True if it is fine
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


    def CheckDiagonal_DL_to_UR(self): # Works
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


        print("amount of DL to UR in a row:", amountinrow) # for debugging
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO DL-->UR") # for debugging
        else:
            self.GameEnd = False

    def CheckDiagonal_UL_to_DR(self): # no works :(
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

        print("UL to DR amount in row:", amountinrow) # for debugging
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO UL-->DR") # for debugging
        else:
            self.GameEnd = False

    def CheckHorizontalLine(self): # still no work D:
        ValToCheckFor = self.board[self.Row_place, self.Column_Place]
        SameThing = True
        amountinrow = 0

        #print("start position is", self.Row_place, self.Column_Place)  # for debugging
        for valuepos in range(0, 4):
            newColumn = self.Column_Place + valuepos

            if self.CheckInBounds(self.Row_place, newColumn):
                if self.board[self.Row_place, newColumn] != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        SameThing = True
        for valuepos in range(1,5):
            newNegColumn = self.Column_Place - valuepos

            if self.CheckInBounds(self.Row_place, newNegColumn):
                if self.board[self.Row_place, newNegColumn] != ValToCheckFor:
                    SameThing = False
                if SameThing:
                    amountinrow = amountinrow + 1

        print("Horizontal amount in row", amountinrow) # for debugging
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO HORIZONTAL") # for debugging
        else:
            self.GameEnd = False

    def CheckVerticalLine(self): # working!
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


        print("Vertical amount in row:", amountinrow)
        if amountinrow >= 4:
            self.GameEnd = True
            print("ENDED DUE TO VERTICAL") # for debugging
        else:
            self.GameEnd = False

    def LoadGame(self, PrevState): # need to make this work for an input like "1,2,3,45,6,7)
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
            try:
                value = int(value)
            except:
                print("input list is not made of correct things")
                return False
            self.Column_Place = value - 1
            if not self.CheckInBounds(0, self.Column_Place): # fix this!
                print("not a valid format input, please make it comma separated")
                return False
            self.New_Place_Piece()
            self.Update_Move_List(value)
            self.Update_Turn()
        self.CheckWin()
        print("State Loaded")
        return True

    def CheckBoardFull(self): # need to create this - make it check if board is full for a tie
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


    def DisplayMoves(self):
        print("list of moves(columns that it was placed in):", self.MoveList)

    def DisplayWinner(self):
        print("Player", self.playerturn, "Wins!")

    def MainGame(self):
        LoadState = input("Would you like to load from a previous state? (y/n): ")
        self.Create_Board()
        self.Display_Board()
        GameLoaded = False
        if LoadState == "y": #
            while not GameLoaded:
                StateToLoad = input("Enter a list of the previous state to load: ")
                GameLoaded = self.LoadGame(StateToLoad)
                self.Display_Board()

        while not self.GameEnd:
            print("It is your turn player", self.playerturn)
            self.Make_Move()
            self.Display_Board()
            self.CheckWin()
            self.Update_Turn()
            boardfull = self.CheckBoardFull()
        if boardfull:
            print("No one wins")
        elif self.GameEnd:
            self.Update_Turn()
            self.DisplayWinner()
            self.DisplayMoves()


# connect 4 game is working! - i think? - need to now interface it using pygame
# I also need to implement the minmax into it
# make it work with the keyboard button presses?
# Place_Piece needs to be removed for final version - it is old code that didn't work - I changed it to fix file
#

class pygam_interface:
    def __init__(self, dimensions, frame_colour, p1_colour, p2_colour, Background_colour):
        self.dimensions = dimensions
        self.FrameColour = frame_colour
        self.p1Colour = p1_colour
        self.p2Colour = p2_colour
        self.BackgroundColour = Background_colour


Dimensions = [Rows, Columns]
mytestgame = Game(Dimensions)
mytestgame.MainGame()
