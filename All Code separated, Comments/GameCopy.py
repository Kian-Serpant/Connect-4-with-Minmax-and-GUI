# IMPORT LIBRARIES
import pygame
import numpy as np
import random # for bogo sort :D
import sys
import time

# Constants
Red = (255, 0, 0)  # for counter
Yellow = (255, 255, 0)  # for counter
Frame_Blue = (72, 160, 255)  # for the frame
Background_White = (255, 255, 255)

from Display import Display
from Board import Board
from Player import Player

class Game:
    def __init__(self, dimensions):
        self.board = Board(dimensions)
        self.displayer = Display(dimensions)
        self.board.Create_Board()
        self.player = Player()
        self.MoveList = []
        self.GameEnd = False

    def Make_Move(self, turn, HumPlayer="yes"):
        try:
            temp = int(HumPlayer)
            isHuman = False
        except:
            isHuman = True

        if isHuman: # could neaten this up by putting it into the try except statement
            move = self.player.Get_Move()
            print("Move returned by GET_MOVE is:", move) # for TESTING

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
                NextPosition = self.board.GetNextColumnCell()
                CurrentRow = NextPosition[self.Column_Place][0]
                self.displayer.PlaceCounter(NextPosition, value-1, self.player.Get_Turn())
                self.board.UpdateColumnPlace(self.Column_Place)


                if self.Column_Place == - 1: # works here!
                    self.GoBackMove()
                    self.board.Display_Board()
                    ValueSkipped = True

                elif not self.board.CheckInBounds(CurrentRow - 1, self.Column_Place): # works here!
                    print(value, "is not a valid column to place in right now, skipping this!")
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
            #print("ENDED DUE TO DL-->UR")  # for debugging
            return True
        else:
            self.GameEnd = False
            return False

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
            #print("ENDED DUE TO UL-->DR")  # for debugging
            return True
        else:
            self.GameEnd = False
            return False

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
            #print("ENDED DUE TO HORIZONTAL")  # for debugging
            return True
        else:
            self.GameEnd = False
            return False

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
            #print("ENDED DUE TO VERTICAL")  # for debugging
            return True
        else:
            self.GameEnd = False
            return False

    def DisplayWinner(self, turn):
        if (self.enemy == 1) and (turn == 2):
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

        amountofrows = (self.board.GetDimensions())[0] # had to add this because I forgot to update rowcount
        for rows in self.board.GetBoard():
            # print("found", rows[PosToRemove], "at position", rowcount, PosToRemove) # for debugging
            if rows[PosToRemove] == 0:
                # print("Removed the value at", (rowcount-1), PosToRemove, "Value was", self.board[rowcount-1, PosToRemove]) # for debugging
                self.board.Update_Board((rowcount - 1, PosToRemove), 0)
                self.player.Update_Turn()
                return True
            rowcount += 1
            if rowcount == amountofrows:
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
            integerchosen = False
            while not integerchosen:
                try:
                    depth = int(input("Enter a depth of moves you want the AI to go to(higher number is harder, but will also take longer)"))
                    integerchosen = True
                except:
                    print("try again, enter an integer")

            self.AI_Depth = depth
        if choice == 2:
            print("human enemy chosen")
        self.enemy = choice

        print("")

    def AI_Make_Move(self, turn):
        #there is an issue here

        #print("ai testing moves!") # for debugging
        move = self.player.NEWAI_Get_Move(self.board.dimensions, self.board.GetTotalScoreBoard(), self, self.board, self.AI_Depth)
        #print("AI move:", move) # for debugging
        NextPosition = self.board.GetNextColumnCell()
        print("NextPosition is", NextPosition) # for testing
        GoneBack = False
        if move == -1:
            self.displayer.PlaceCounter(NextPosition, self.MoveList[-1] - 1, 3)
            self.GoBackMove()
            GoneBack = self.GoBackMove()

        if GoneBack:
            return GoneBack


        else:
            self.board.UpdateColumnPlace(move)
            print("Column place is", self.board.GetColumnPlace()) # for testing
            self.board.New_Place_Piece(turn)
            print("Placed counter at", NextPosition, move) # for testing
            self.displayer.PlaceCounter(NextPosition, move, turn)
            mymove = self.board.GetColumnPlace() + 1
            self.Update_Move_List(mymove)
        self.MoveMade = move + 1

    def MainGame(self):
        PlayerWon = False
        LoadState = input("Would you like to load from a previous state? (y/n): ")
        self.board.Display_Board()
        #print("Board displayed") # for debugging

        self.board.GetTotalScoreBoard()

        GameLoaded = False
        boardfull = False
        #print(self.board.GetTotalScoreBoard())
        if LoadState == "y":
            while not GameLoaded:
                StateToLoad = input("Enter a list of the previous state to load: ")
                GameLoaded = self.LoadGame(StateToLoad)
                self.board.Display_Board()

        self.ChooseOpponent()

        while not self.GameEnd:
            self.board.GetCellsForEachThing() # for debugging
            NextPosition = self.board.GetNextColumnCell()
            playerturn = self.player.Get_Turn()
            if playerturn == 2 and self.enemy == 1:
                #print("AI making move")
                HasGoneBack = self.AI_Make_Move(playerturn)
            else:
                print("It is your turn player", playerturn, "Press R to go back moves")
                #HasGoneBack = self.Make_Move(playerturn)
                HasGoneBack = self.Display_Make_Move(playerturn, NextPosition)
            if HasGoneBack:
                print("Gone back a move")
            else:
                PlayerWon = self.CheckWin()
                self.player.Update_Turn()
            self.board.Display_Board()
            print("Move made was:", self.MoveMade)
            boardfull = self.board.CheckBoardFull()
            #self.CheckWin()# AM HERE IN TESTING
            #error due to checkwin
            if boardfull:
                self.GameEnd = True
            print("\n")


        if PlayerWon:
            self.player.Update_Turn()
            self.DisplayWinner(playerturn)
            self.DisplayMoves()
            # add code here for the game ending
            self.displayer.GameOver(playerturn)

        elif boardfull:
            print("No one wins")
            self.displayer.GameOver(5) # tells players the game has ended

