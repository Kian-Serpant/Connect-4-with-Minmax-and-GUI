# IMPORT LIBRARIES
import pygame
import numpy as np
import random # for bogo sort :D

# Constants
Red = (255, 0, 0)  # for counter
Yellow = (255, 255, 0)  # for counter
Frame_Blue = (72, 160, 255)  # for the frame
Background_White = (255, 255, 255)

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
            #print("move valid")
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
            else:
                emptycolumns.append("x") # for if column is empty for iteration
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


        return TotalScoreBoard

    def GetCellScore(self, location):
        ScoreBoard = self.GetTotalScoreBoard()
        Score = ScoreBoard[location]
        return Score


class Position:
    # created this separate class because it made following the wikipedia pseudocode a lot easier!
    # maybe make into a subclass, and change it to being a minmax algorithm or smth?

    def __init__(self, Choice, rows, Gameinstance, BoardInstance, state=None):
        self.Column = Choice
        self.Row = rows
        self.Location = [self.Row, self.Column]
        self.BoardInstance = BoardInstance
        self.GameInstance = Gameinstance
        self.State = state


    def isTerminal(self, turn):
        #print("checking if terminal") # for debugging
        self.GameInstance.Make_Move(turn, self.Column)
        isTerminal = self.GameInstance.CheckWin() # will check for a win
        #self.BoardInstance.Display_Board()
        #if isTerminal:# added if statement -  check if running when next doing stuff!
            #print("VALUE WAS TERMINAL!!!!") # for debugging
        #print("End of checking if terminal \n") # for debugging

        if isTerminal: # returns true if it is a terminal state(aka end of game, or a player won!)
            return True
        else:
            return False

    def GetLocation(self):
        NextCells = self.BoardInstance.GetNextColumnCell()
        #print("Next cells:", NextCells) # for debugging
        #print("CURRENT LOCATION IS:", self.Location) # for debugging
        NewLocation = NextCells[self.Location[1]] # the first argument is the position up from bottom
        CurrentHeight = (self.Row+1) - NewLocation[0]
        NewerLocation = [CurrentHeight,  self.Location[1]]
        #print("Newer location:", NewerLocation) # for debugging
        self.Location = NewerLocation

        return self.Location
        #return self.Location

    def Get_Children(self, turn):
        Children = []
        for value in self.BoardInstance.GetEmptyColumns(): # this gives each column that the next one can be played down!
            try:
                int(value)
                Children.append(value)
            except:
                print("Column is full")
        self.Children = Children.copy()
        #print("children:", self.Children) # for debugging
        return self.Children

    def HeuristicValue(self):
        Score = self.BoardInstance.GetCellScore(self.Location)
        return Score




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
                mycolumn = int(input("Press number of the column you want to place it in, or '0' to go back a move, -1 to display the moves played so far: "))
                self.Column_Place = mycolumn - 1
                Correct_Input = True
            except:
                print("Enter an integer, try again!")

        #print("move gotten:", self.Column_Place)
        return self.Column_Place

    def Get_Turn(self): # outputs the playerturn, for other classes to use
        return self.playerturn

    def AIBogoSort(self, dimensions):
        columns = dimensions[1]
        AIChoice = random.randint(1, columns)
        print("AI picked to place it in", AIChoice)
        self.Column_Place = AIChoice - 1
        return self.Column_Place

    def NEWgenerate_combinations(self, elements, depth, current_combination, result):  # sets current combinations and result to be empty lists if first time running through
        if depth == 0:  # Base case: add the current combination to the results, if it has reached lowest depth
            result.append(current_combination)
            return result

        for element in elements:  # the elements is the list of children. this will go through for each column, and a list of values it could be/
            # Recursive call with depth reduced by 1 and element added to combination
            self.NEWgenerate_combinations(elements, depth - 1, current_combination + [element], result)

        return result

    def NEWUseMinMax(self, children, depth, GameInstance, BoardInstance, dimensions, ScoredCells):
        allcombos = self.NEWgenerate_combinations(children, depth, [], [])

        ScoreDict = {}
        columnnum = 0
        for key in children: # initialises a dictionary of the scores!
            columnnum += 1
            ScoreDict[columnnum] = 0
        for combination in allcombos:
            Depth2 = depth
            totalMoves = 0
            for move in combination:
                try:
                    int(move)
                    CurrentTurn = GameInstance.player.Get_Turn()
                    Depth2 -= 1
                    position = Position(move-1, (dimensions[0] - 1), GameInstance, BoardInstance)
                    Location = position.GetLocation()
                    loc1 = Location[0]
                    loc2 = Location[1]
                    #print("Loc1:", loc1, "Loc2", loc2, "\n") # for debugging
                    try:
                        ThisScore = ScoredCells[loc1][loc2]
                        GameInstance.player.Update_Turn()
                        TerminalNode = position.isTerminal(CurrentTurn)
                        if TerminalNode:
                            if (CurrentTurn == 2):  # currently testing this thing to give reward
                                ThisScore += 101 * (Depth2 + 1)
                            if (CurrentTurn == 1) and TerminalNode:
                                ThisScore -= 200 * (Depth2 + 1)
                        totalMoves += 1
                        ScoreDict[combination[0]] += ThisScore
                    except:
                        ThisScore = 0
                except:
                    x = "NotDoingThis"
            for value in range(0, totalMoves):
                GameInstance.Make_Move(CurrentTurn, -1)

        return ScoreDict

    def NEWAI_Get_Move(self, dimensions, ScoreBoard, Gameinstance, BoardInstance, depth=0):
        print("AI is deciding on a move")
        #print("In AI_Get_Move") # for debugging
        children = BoardInstance.GetEmptyColumns()
        #depth = int(input("Enter the depth you want the algorithm to go to(placeholder):"))
        ColumnScores = self.NEWUseMinMax(children, depth, Gameinstance, BoardInstance, dimensions, ScoreBoard)

        readableScores = []
        counter = 0
        for value in ColumnScores:
            counter += 1
            #print("Column", counter, "score:", ColumnScores[value]) # for debugging
            if ColumnScores[value] == 0:
                readableScores.append(-1*10**30)
            else:
                readableScores.append(float(ColumnScores[value]))
        #print("Column Scores:", readableScores)  # for debugging

        TopScore = max(readableScores)
        #print("TOP SCORE:", TopScore) # for debugging
        BestColumn = readableScores.index(TopScore)
        print("Scores were:", readableScores) # for debugging
        #print("AI Chose column:", BestColumn + 1)
        self.Column_Place = BestColumn
        return self.Column_Place


class Game:
    def __init__(self, dimensions):
        self.board = Board(dimensions)
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


        integerchosen = False
        while not integerchosen:
            try:
                depth = int(input("Enter a depth of moves you want the AI to go to(higher number is harder, but will also take longer)"))
                integerchosen = True
            except:
                print("try again, enter an integer")

        self.AI_Depth = depth
        print("")

    def AI_Make_Move(self, turn):
        #print("ai testing moves!") # for debugging
        move = self.player.NEWAI_Get_Move(self.board.dimensions, self.board.GetTotalScoreBoard(), self, self.board, self.AI_Depth) # gets stuck here
        #print("AI move:", move) # for debugging
        GoneBack = False
        if move == -1:
            GoneBack = self.GoBackMove()

        if GoneBack:
            return GoneBack
        else:
            self.board.UpdateColumnPlace(move)
            #print("Column place1:", self.board.GetColumnPlace()) # for debugging
            MoveValid = self.board.Check_Move_Valid()
            while not MoveValid:
                self.Column_Place = self.player.AIBogoSort(self.board.dimensions)
                self.board.UpdateColumnPlace(self.Column_Place)
                if self.Column_Place == -1:
                    GoneBack = self.GoBackMove()
                    return GoneBack

                MoveValid = self.board.Check_Move_Valid()
            self.board.New_Place_Piece(turn) # at some point it is going back a move where it shouldn't
            mymove = self.board.GetColumnPlace() + 1
            self.Update_Move_List(mymove)
        self.MoveMade = move + 1

    def MainGame(self):
        LoadState = input("Would you like to load from a previous state? (y/n): ")
        self.board.Display_Board()
        #print("Board displayed") # for debugging

        self.board.GetTotalScoreBoard()

        GameLoaded = False
        boardfull = False
        #print(self.board.GetTotalScoreBoard())
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
            if playerturn == 2 and self.enemy == 1:
                #print("AI making move")
                HasGoneBack = self.AI_Make_Move(playerturn)
            else:
                print("It is your turn player", playerturn)
                HasGoneBack = self.Make_Move(playerturn)
            if HasGoneBack:
                print("Gone back a move")
            else:
                self.CheckWin()
                self.player.Update_Turn()
            self.board.Display_Board()
            print("Move made was:", self.MoveMade)
            boardfull = self.board.CheckBoardFull()
            self.CheckWin()
            if boardfull:
                self.GameEnd = True
            print("\n")

        if boardfull:
            print("No one wins")
        elif self.GameEnd:
            self.player.Update_Turn()
            self.DisplayWinner(playerturn)
            self.DisplayMoves()


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


PlayGame()


class pygam_interface:
    def __init__(self, dimensions, frame_colour, p1_colour, p2_colour, Background_colour):
        self.dimensions = dimensions
        self.FrameColour = frame_colour
        self.p1Colour = p1_colour
        self.p2Colour = p2_colour
        self.BackgroundColour = Background_colour





