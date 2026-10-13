# IMPORT LIBRARIES
import numpy as np




class Board:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.Rows = dimensions[0] - 1

    def Create_Board(self):
        '''
        this will create a board of all zeros, based on the dimensions. It is a numpy array, as that runs quicker than
        a standard python list. A zero represents an empty cell.
        '''
        self.board = np.zeros(self.dimensions)

    def Display_Board(self):
        '''
        This will print the board. It prints self.board backwards in order to mimic the look of connect 4, but still
        keeping the ease of the columns and rows aligning with that in the board.
        '''
        x = self.board
        print(x[::-1])

    def New_Place_Piece(self, playerturn):
        '''
        This will place a piece in a given column. It will go through that column until it reaches an empty cell, where
        it will then place the counter.
        '''
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
        '''
        This will update self.Row_place to the place that is input
        '''
        self.Row_place = newPlace

    def Get_Row_Place(self):
        '''
        This will return the row place for usage in the program
        '''
        return self.Row_place

    def Update_Board(self, position, value):
        '''
        This will take in parameters of position and value. It will update the board at that position, so it indicates
        the counter that should be there
        '''
        self.board[position] = value

    def Check_Column_Not_Full(self):
        '''
        This will check if the value at the top of the column is 0. If it is anything but zero(no space to place it)
        it will return False, indicating the column is full. If it's a zero, then it will return True, indicating there
        is space in that column
        '''
        if self.board[(self.Rows, self.Column_Place)] != 0:
            return False
        else:
            return True

    def Check_Move_Valid(self):
        '''
        This will use the function to check if a column is full in combination with the function to check if the move is
        actually one that is in bounds(aka they aren't trying to play column 8 on a board with only 7 columns). It will
        return True if the move is valid, otherwise it will let the player know why the move is invalid, and will return
        False, which then triggers a promp that will get the player to try again.
        '''
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
            return True

    def GetColumnPlace(self):
        '''
        This will return the column place for usage in the program.
        '''

        return self.Column_Place

    def UpdateColumnPlace(self, column):
        '''
        This will take an input of column, and will update self.Column_Place to that value
        '''
        self.Column_Place = column

    def CheckBoardFull(self):
        '''
        This will go through the entire board, checking if each position is full. If every position is full, then it
        will return True, and let the user know in terminal that the board is full. If the board has any zeros, or empty
        places, then it will return False, indicating the board still has space.
        '''
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
        '''
        This will take in both a row and a column, and will return thing that is in that square for usage in the program
        '''
        return self.board[RowToCheck, ColumnToCheck]

    def CheckInBounds(self, Row, Column):
        '''
        This will take in both a row and a column, and will check if they are inside the playing area, or rather if
        they can actually be played as columns. It returns False if the cells are out of bounds, and True if in bounds
        '''
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
        '''
        This will return the board for usage in the program.
        '''
        return self.board

    def GetDimensions(self):
        '''
        This will return the dimensions of the board for usage in the program.
        '''
        return self.dimensions

    def GetEmptyColumns(self):
        '''
        this will iterate through the board and check which columns are empty to feed into the minmax algorithm
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

    def GetNextColumnCell(self): #  can use this for code to display my board
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

    def ScoreForAtEnd(self):
        '''
        This will go through and check how many different ways there are of winning with this square at the end of the
        line. It will then return that amount. (e.g. bottom right corner can win 3 different ways from being at the end
        of a winning combination, whereas the center square can win in 10 different ways from being at the end)
        '''
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
        '''
        This will go through and check how many different ways there are of winning with this square in the middle of a
        winning line. It will then return that amount. (e.g. bottom right corner can only win from being at the end, and
        so has no score added for being in the middle, whereas the second one in the leftmost column can win in one way
        from being in the centre, and the third one up can win in two ways from being in the center.)
        '''
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

    def GetTotalScoreBoard(self):
        '''
        This will go through the board, and using the functions to score middle and end, will add those together to give
        a total score for that position(aka how many different "4s" that square is a part of), and will return a board
        of the scores for each square. This directly corresponds to the board that you play on. There is a diagram of
        this in the documentation.
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
        '''
        This will take in a location, and will get the score of that cell for usage on scoring moves. It will then
        return that score.
        '''
        ScoreBoard = self.GetTotalScoreBoard()
        Score = ScoreBoard[location]
        return Score