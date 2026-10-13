
class Position:

    def __init__(self, Choice, rows, Gameinstance, BoardInstance, state=None):
        self.Column = Choice
        self.Row = rows
        self.Location = [self.Row, self.Column]
        self.BoardInstance = BoardInstance
        self.GameInstance = Gameinstance
        self.State = state


    def isTerminal(self, turn):
        '''
        This will take an input of the turn, and will then make the move that was fed in. It will then test that move to
        see if it is a winning move(also known as a terminal node). If it is, then True is returned, otherwise False is
         returned
        '''
        self.GameInstance.Make_Move(turn, self.Column)
        isTerminal = self.GameInstance.CheckWin() # will check for a win
        if isTerminal: # returns true if it is a terminal state(aka end of game, or a player won!)
            return True
        else:
            return False

    def GetLocation(self):
        '''
        This will return the location that the counter was placed in.
        '''
        NextCells = self.BoardInstance.GetNextColumnCell()
        NewLocation = NextCells[self.Location[1]]
        CurrentHeight = (self.Row+1) - NewLocation[0]
        NewerLocation = [CurrentHeight,  self.Location[1]]
        self.Location = NewerLocation

        return self.Location


    def Get_Children(self, turn):
        Children = []
        for value in self.BoardInstance.GetEmptyColumns(): # this gives each column that the next one can be played down!
            try:
                int(value)
                Children.append(value)
            except:
                print("Column is full")
        self.Children = Children.copy()
        return self.Children

    def HeuristicValue(self):
        '''
        This will return the score of a cell at a certain place. This is generally used if that cell is terminal, or if
        it reaches the depth it has been specified to go to.
        '''
        Score = self.BoardInstance.GetCellScore(self.Location)
        return Score
