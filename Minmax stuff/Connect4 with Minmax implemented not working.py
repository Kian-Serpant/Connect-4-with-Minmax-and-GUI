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
            print("Move invalid")
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

    def GetEmptyColumns(self):
        '''
        this will iterate throught the board and check which columns are empty to feed into the minmax algorithm
        '''
        amountofcolumns = self.dimensions[1]
        amountofrows = len(self.board)
        emptycolumns = []
        for value in range(0, amountofcolumns):
            self.Update_row_place(amountofrows)
            self.UpdateColumnPlace(value)

            if self.Check_Column_Not_Full():
                emptycolumns.append(value + 1)
        return emptycolumns

    def GetCellsForEachThing(self):
        '''
        This will return a 2D list consisting of which cells have each players things in. It will return all 3 of them
        The order of the output is the Empty cells, player 1s cells, then player 2s cells
        '''

        P1Cells = []
        P2Cells = []
        EmptyCells = []
        myboard = self.GetBoard()
        rowlocation = 0

        for row in myboard:
            rowlocation += 1
            columnlocation = 0
            for column in row:
                columnlocation += 1
                if column == 0:
                    EmptyCells.append([rowlocation, columnlocation])
                elif column == 1:
                    P1Cells.append([rowlocation, columnlocation])
                elif column == 2:
                    P2Cells.append([rowlocation, columnlocation])

        totalcells = [EmptyCells, P1Cells, P2Cells]
        return totalcells

    def GetNextColumnCell(self):
        '''
        This will use the board, and will check where the next position for each column is - it will return it as a list
        with the element index corresponding to the column. If that Column has no places, then it will return [-1, -1]
        in it's place.
        '''

        PlaceRow = 0
        AmountOfCol = (self.GetDimensions())[1]
        EmptyList = []
        for number in range(0, AmountOfCol):
            EmptyList.append([0,0])

        myboard = self.GetBoard()

        for row in myboard:
            PlaceRow += 1
            PlaceColumn = 0
            for ColumnVal in row:
                PlaceColumn += 1
                if ColumnVal == 0:
                    if EmptyList[PlaceColumn-1] == [0,0]:
                        EmptyList[PlaceColumn - 1] = [PlaceRow, PlaceColumn]

        ValLocation = -1
        for Element in EmptyList:
            ValLocation += 1
            if Element == [0,0]:
                EmptyList[ValLocation] = [-1, -1]

        return EmptyList

    def ScoreForAtEnd(self): # this should go through the board and score each thing for if AT END OF ROW
        CurrentBoard = self.GetBoard()
        Dimensions = self.GetDimensions()
        Rows = Dimensions[0]
        Columns = Dimensions[1]
        ScoreBoard = np.zeros([Rows, Columns])

        CurrentRow = -1

        for Row in CurrentBoard: # this will check for each row, and see if it works
            CurrentRow += 1
            CurrentCol = -1
            for Square in Row:
                SquareScore = 0
                amountinrow = 0
                CurrentCol += 1

                for AddCol in range(0,4): # checks for if it can go to the right
                    CheckCol = CurrentCol + AddCol
                    InBounds = self.CheckInBounds(CurrentRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for MinCol in range(0,4): # checks if can go to left
                    CheckCol = CurrentCol - MinCol
                    InBounds = self.CheckInBounds(CurrentRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for AddRow in range(0,4): # checks if can go up
                    CheckRow = CurrentRow + AddRow
                    InBounds = self.CheckInBounds(CheckRow, CurrentCol)
                    if InBounds:
                        amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for MinRow in range(0,4): # checks if can go down
                    CheckRow = CurrentRow - MinRow
                    InBounds = self.CheckInBounds(CheckRow, CurrentCol)
                    if InBounds:
                        amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for Add_DLUR in range(0,4): # checks diagonal from square, up to right
                    CheckRow = CurrentRow + Add_DLUR
                    CheckCol = CurrentCol + Add_DLUR
                    InBounds = self.CheckInBounds(CheckRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for Min_DLUR in range(0,4): # checks from square down to left
                    CheckRow = CurrentRow - Min_DLUR
                    CheckCol = CurrentCol - Min_DLUR
                    InBounds = self.CheckInBounds(CheckRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for Add_ULDR in range(0,4): # checks from square up to left
                    CheckRow = CurrentRow + Add_ULDR
                    CheckCol = CurrentCol - Add_ULDR
                    InBounds = self.CheckInBounds(CheckRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for Min_ULDR in range(0,4): # checks from square down to right
                    CheckRow = CurrentRow - Min_ULDR
                    CheckCol = CurrentCol + Min_ULDR
                    InBounds = self.CheckInBounds(CheckRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1


                ScoreBoard[CurrentRow, CurrentCol] = SquareScore


        return ScoreBoard

    def ScoreForInMiddle(self):  # this should go through the board and score each thing for if AT SECOND POS OF ROW!
        CurrentBoard = self.GetBoard()
        Dimensions = self.GetDimensions()
        Rows = Dimensions[0]
        Columns = Dimensions[1]
        ScoreBoard = np.zeros([Rows, Columns])

        CurrentRow = -1

        for Row in CurrentBoard:  # this will check for SECOND THING in each row, and see if it works
            CurrentRow += 1
            CurrentCol = -1
            for Square in Row:
                SquareScore = 0
                amountinrow = 0
                CurrentCol += 1

                for AddCol in range(0, 3):  # checks for if it can go to the right 2, and left 1
                    CheckCol = CurrentCol + AddCol
                    InBounds = self.CheckInBounds(CurrentRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                CheckCol = CurrentCol - 1
                InBounds = self.CheckInBounds(CurrentRow, CheckCol)
                if InBounds:
                    amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for MinCol in range(0, 3):  # checks if can go to left 2 and right 1
                    CheckCol = CurrentCol - MinCol
                    InBounds = self.CheckInBounds(CurrentRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                CheckCol = CurrentCol + 1
                InBounds = self.CheckInBounds(CurrentRow, CheckCol)
                if InBounds:
                    amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for AddRow in range(0, 3):  # checks if can go up 2 and down 1
                    CheckRow = CurrentRow + AddRow
                    InBounds = self.CheckInBounds(CheckRow, CurrentCol)
                    if InBounds:
                        amountinrow += 1
                CheckRow = CurrentRow - 1
                InBounds = self.CheckInBounds(CheckRow, CurrentCol)
                if InBounds:
                    amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for MinRow in range(0, 3):  # checks if can go down 2 and up 1
                    CheckRow = CurrentRow - MinRow
                    InBounds = self.CheckInBounds(CheckRow, CurrentCol)
                    if InBounds:
                        amountinrow += 1
                CheckRow = CurrentRow + 1
                InBounds = self.CheckInBounds(CheckRow, CurrentCol)
                if InBounds:
                    amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1
                amountinrow = 0

                for Add_DLUR in range(0, 3):  # checks diagonal from square, up to right 2, down left 1
                    CheckRow = CurrentRow + Add_DLUR
                    CheckCol = CurrentCol + Add_DLUR
                    InBounds = self.CheckInBounds(CheckRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                CheckRow = CurrentRow - 1
                CheckCol = CurrentCol - 1
                InBounds = self.CheckInBounds(CheckRow, CheckCol)
                if InBounds:
                    amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for Min_DLUR in range(0, 3):  # checks from square down to left 2, up right 1
                    CheckRow = CurrentRow - Min_DLUR
                    CheckCol = CurrentCol - Min_DLUR
                    InBounds = self.CheckInBounds(CheckRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                CheckRow = CurrentRow + 1
                CheckCol = CurrentCol + 1
                InBounds = self.CheckInBounds(CheckRow, CheckCol)
                if InBounds:
                    amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for Add_ULDR in range(0, 3):  # checks from square up to left 2, down right 1
                    CheckRow = CurrentRow + Add_ULDR
                    CheckCol = CurrentCol - Add_ULDR
                    InBounds = self.CheckInBounds(CheckRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                CheckRow = CurrentRow - 1
                CheckCol = CurrentCol + 1
                InBounds = self.CheckInBounds(CheckRow, CheckCol)
                if InBounds:
                    amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                amountinrow = 0

                for Min_ULDR in range(0, 3):  # checks from square down to right 2, up left 1
                    CheckRow = CurrentRow - Min_ULDR
                    CheckCol = CurrentCol + Min_ULDR
                    InBounds = self.CheckInBounds(CheckRow, CheckCol)
                    if InBounds:
                        amountinrow += 1
                CheckRow = CurrentRow + 1
                CheckCol = CurrentCol - 1
                InBounds = self.CheckInBounds(CheckRow, CheckCol)
                if InBounds:
                    amountinrow += 1
                if amountinrow == 4:
                    SquareScore += 1

                ScoreBoard[CurrentRow, CurrentCol] = SquareScore

        return ScoreBoard

    def GetTotalScoreBoard(self): # all working!
        '''
        This will go through the board, and using the functions to score middle and end, will add those together to give
        a total score for that position(aka how many different "4s" that square is a part of), and will return a board
        of the scores for each square. This directly corresponds to the board that you play on!
        '''

        Ends = self.ScoreForAtEnd()
        Mids = self.ScoreForInMiddle()
        Dimensions = self.GetDimensions()
        Rows = Dimensions[0]
        Columns = Dimensions[1]
        TotalScoreBoard = np.zeros([Rows, Columns])


        for Row in range(0, Rows):
            for Column in range(0, Columns):
                EndScore = Ends[Row-1, Column-1]
                MidScore = Mids[Row-1 , Column-1]
                TotalScore = EndScore + MidScore
                TotalScoreBoard[Row-1, Column-1] = TotalScore

        print("\nhere is scored board(each tile assigned a value!)")

        print(TotalScoreBoard)
        return TotalScoreBoard

    def GetCellScore(self, location):
        ScoreBoard = self.GetTotalScoreBoard()
        Score = ScoreBoard[location]
        return Score




# ignore SubGame class for now - might be used later!
class SubGame:
    '''
    created this for going down trees

     maybe change it from being a class later
    '''
    def __init__(self, GameToLoad, dimensions):
        self.InGame = Game(dimensions)
        self.InGame.LoadGame(GameToLoad)

    def TestTerminal(self, move):
        print("hello")


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

        print("move gotten:", self.Column_Place)
        return self.Column_Place

    def Get_Turn(self): # outputs the playerturn, for other classes to use
        return self.playerturn

    def AIBogoSort(self, dimensions):
        columns = dimensions[1]
        AIChoice = random.randint(1, columns)
        print("AI picked to place it in", AIChoice)
        self.Column_Place = AIChoice - 1
        return self.Column_Place

    # can probably delete AIMinMax in final version - pretty sure it's useless
    def AIMinMax(self, CellLocations, dimensions, board, nextcell, depth):
        '''

        :param CellLocations: uses Game --> self.board.GetCellsForEachThing
        :param dimensions: uses game --> self.board.GetDimensions
        :param board: uses game --> self.board.GetBoard
        :param nextcell: uses game --> self.board.GetNextColumnCell
        :param depth: maybe get player to input a thing for this to do!
        '''
        PlayerCell = 1
        AICell = 2

        EmptyCells = CellLocations[0] # these are all places where the things can be placed!
        EnemyCells = CellLocations[1]
        MyCells = CellLocations[2]
        NextCells = nextcell
        TotalColumns = dimensions[1]
        TotalRows = dimensions[0]
        ActualBoard = board
        DepthToGoTo = depth

        x = Game.CheckWin() # to check for a win - will be true if returned correctly!


        # now on step 9 online - I need to figure/ask Dr Jackson how I would pull from a different class
        if Game.CheckWin(self):
            print("test")

    def MinMaxAlgorithm(self, inposition, depth, alpha, beta, IsMaximizingPlayer, dimensions, ScoreBoard):
        '''
        This is using the wikipedia page on minimax - specifically using the pseudocode, and the "minimax algorithm with
        alternate moves" section
        ADDITIONALLY, AM NOW USING ALPHA-BETA PRUNING WIKI PAGE

        NEED TO SETUP POSITION TO HAVE TEH RIGHT ARGUMENTS!

        NEED TO LEARN WHAT max() DOES IN PYTHON!!!

        MaximizingPlayer is the player that we want to win, or are doing the minmax for MAYBE!?
        '''

        print("Dimensions:", dimensions)
        position = Position(inposition, (dimensions[0] - 1))

        ScoredCells = ScoreBoard
        Score = ScoredCells[position.GetLocation()]

        TerminalNode = position.isTerminal(self.Get_Turn())
        if depth == 0 or TerminalNode:
            return Score

        if IsMaximizingPlayer:
            Score = -(np.inf)
            for child in position.GetChildren(self.Get_Turn()):
                Score = max(Score, self.MinMaxAlgorithm(child, depth - 1, alpha, beta, False, dimensions, ScoreBoard))
                # max will return the highest value of the input values
                if Score > beta:
                    break # beta cut off
                alpha = max(alpha, Score)
            return Score

        else:
            Score = np.inf
            for child in position.GetChildren():
                Score = min(Score, self.MinMaxAlgorithm(child, depth - 1, alpha, beta, True, dimensions, ScoreBoard))
                if Score < alpha:
                    break # alpha cut off
                beta = min(beta, Score)
            return Score

    def getMinMaxScores(self, dimensions, depth, ScoreBoard):
        alpha = np.inf
        beta = -alpha
        ColumnScores = [] # this basically creates a list for each column - or the score for each

        for column in range(0, dimensions[1]+1):
            Score = self.MinMaxAlgorithm(column, depth, alpha, beta, True, dimensions, ScoreBoard)
            ColumnScores.append(Score)

        print(ColumnScores)
        return ColumnScores

    def AI_Get_Move(self, dimensions, ScoreBoard):
        ColumnScores = self.getMinMaxScores(dimensions, 20, ScoreBoard) # initial depth is 20 - eventually change to be user input!
        TopScore = max(ColumnScores)
        BestColumn = ColumnScores.index(TopScore)
        print("Best Column is:", BestColumn)
        self.Column_Place = BestColumn - 1
        return self.Column_Place


class Game:
    def __init__(self, dimensions):
        self.board = Board(dimensions)
        self.board.Create_Board()
        self.player = Player()
        self.MoveList = []
        self.GameEnd = False

    def testInitWork(self):
        print(self.board.GetBoard())

    def Make_Move(self, turn, HumPlayer=False):
        if not HumPlayer:
            move = self.player.Get_Move() # errors here?! BUT WHYYYY - only errors when I use move later ;-;
        else:
            move = HumPlayer
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
            Themove = self.board.GetColumnPlace() + 1
            self.Update_Move_List(Themove)

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
            print("ENDED DUE TO DL-->UR")  # for debugging
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
            print("ENDED DUE TO UL-->DR")  # for debugging
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
            print("ENDED DUE TO HORIZONTAL")  # for debugging
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
            print("ENDED DUE TO VERTICAL")  # for debugging
            return True
        else:
            self.GameEnd = False
            return False

    def DisplayWinner(self):
        if self.enemy == 1:
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

    def Bogo_AI_Make_Move(self, turn):
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

    def AI_Make_Move(self, turn):
        move = self.player.AI_Get_Move(self.board.dimensions, self.board.GetTotalScoreBoard())
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

        self.board.GetTotalScoreBoard()

        GameLoaded = False
        boardfull = False
        if LoadState == "y":  #
            while not GameLoaded:
                StateToLoad = input("Enter a list of the previous state to load: ")
                GameLoaded = self.LoadGame(StateToLoad)
                self.board.Display_Board()


        self.ChooseOpponent()


        while not self.GameEnd:
            self.board.GetCellsForEachThing() # for debugging
            self.board.GetNextColumnCell()
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
            self.GameEnd = self.board.CheckBoardFull()

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

class Position(Game):
    # created this separate class because it made following the wikipedia pseudocode a lot easier!
    # maybe make into a subclass, and change it to being a minmax algorithm or smth?

    def __init__(self, Choice, row):
        self.Column = Choice
        self.Row = row
        self.Location = [self.Row, self.Column]


    def isTerminal(self, turn):
        self.testInitWork() # BREAKS HERE FOUND IT YAY! - missing positional argument self D:
        self.Make_Move(turn, self.Column) # errors here due to not having been fed Game!
        isTerminal = self.CheckWin()
        self.Make_Move(turn, -1) # this goes back a move (so that the game doesn't end)

        if isTerminal: # returns true if it is a terminal state(aka end of game, or a player won!)
            return True
        else:
            return False

    def GetLocation(self):
        print(self.Location)
        return self.Location

    def Get_Children(self, turn):
        self.Children = Board.GetEmptyColumns() # this gives each column that the next one can be played down!

    def HeuristicValue(self):
        Score = Board.GetCellScore(self.Location)
        return Score


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

def PlayGame():
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


# WHEN BOARD IS FULL, IT NEEDS TO END THE GAME!!!!
PlayGame()
# I also need to implement the minmax into it
# connect 4 game is working! - i think? - need to now interface it using pygame
# make it work with the keyboard button presses?

# IN FINAL VERSION - SPLIT THIS UP INTO DIFFERENT FILES. EACH FILE HAS ONE CLASS IN

# Krish wants me to add previous games(aka NOT FROM CODE THING) - tf is this gonna work?!


class pygam_interface:
    def __init__(self, dimensions, frame_colour, p1_colour, p2_colour, Background_colour):
        self.dimensions = dimensions
        self.FrameColour = frame_colour
        self.p1Colour = p1_colour
        self.p2Colour = p2_colour
        self.BackgroundColour = Background_colour





