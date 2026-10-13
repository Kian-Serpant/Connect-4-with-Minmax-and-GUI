# IMPORT LIBRARIES
import random



from Position import Position


class Player:
    def __init__(self):
        self.playerturn = 1

    def Update_Turn(self):
        '''
        This will change which player's turn it is. The turn is used to decide which colour counter to place, and also
        for printing which player wins at the end.
        '''
        if self.playerturn == 1:
            self.playerturn = 2

        elif self.playerturn == 2:
            self.playerturn = 1

    def UpdateColumnPlace(self, column):
        '''
        This will update self.Column_Place to the column that is input
        '''
        self.Column_Place = column

    def Get_Move(self):  # outputs the move that the player wants for other classes to use
        '''
        This will take a move from the player. This code is no longer used in the final version, but can be used if you
        don't want the display, and you instead just want it to input things in terminal.
        '''
        Correct_Input = False
        while not Correct_Input:
            try:
                mycolumn = int(input("Press number of the column you want to place it in, or '0' to go back a move, -1 to display the moves played so far: "))
                self.UpdateColumnPlace(mycolumn - 1)
                Correct_Input = True
            except:
                print("Enter an integer, try again!")

        return self.Column_Place

    def Get_Turn(self):
        '''
        This will return which player's turn it is in order for other classes to use.
        '''
        return self.playerturn

    def AIBogoSort(self, dimensions):
        '''
        This is the original algorithm that I had used in order to make AI moves. It was mainly a test to check if I
        could have non-human moves input automatically. It is no longer used, but I have kept it in case someone wants
        to play against an AI that is random.
        '''
        columns = dimensions[1]
        AIChoice = random.randint(1, columns)
        print("AI picked to place it in", AIChoice)
        self.Column_Place = AIChoice - 1
        return self.Column_Place

    def NEWgenerate_combinations(self, elements, depth, current_combination, result):
        '''
        :param elements: this is the children that it is using.
        :param depth: the depth it needs to go to from this move.
        :param current_combination: this is the moves that have been played so far in this running of creating the
         combinations.
        :param result: this one of the combinations of moves that can be played to the depth specified at the start.

        This will basically run through every single combination up to the depth specified, and put them all into a
        list.
        The list will be of the size: Columns to the power of the depth multiplied by the depth.(for 7 columns and
        a depth of 4, the list will have a total of 7^4 different combinations, each one with 4 moves, so (7^4)*4
        moves in that array, or 9604.)
        This is a recursive algorithm that will reduce the depth by one when it calls itself.
        '''
        if depth == 0:  # Base case: add the current combination to the results, if it has reached lowest depth
            result.append(current_combination)
            return result

        for element in elements:  # the elements is the list of children. this will go through for each column, and a list of values it could be/
            # Recursive call with depth reduced by 1 and element added to combination
            self.NEWgenerate_combinations(elements, depth - 1, current_combination + [element], result)

        return result

    def NEWUseMinMax(self, children, depth, GameInstance, BoardInstance, dimensions, ScoredCells):
        '''
        :param children: These are all the columns, and whether they have space in.
        :param depth: This is the depth that the algorithm should go to
        :param GameInstance: The temporary instance of the game being used, and one that each combination will be fed
        into in order to score them
        :param BoardInstance: The temporary instance of the board being used, and one that each combination will be fed
        into in order to score them
        :param dimensions: this is the dimensions of the board that is being played on
        :param ScoredCells: this is the board, but with each cell having a score, instead of one for playing on.

        This will return a list of the scores, with each score corresponding to the column. For example, the first value
        in this list will be the score for column 1. If a column is full before it can test the depth, the score for
        that column will be set to 0, for usage later on.
        '''
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
                    temp = 5
            for value in range(0, totalMoves):
                GameInstance.Make_Move(CurrentTurn, -1)

        return ScoreDict

    def NEWAI_Get_Move(self, dimensions, ScoreBoard, Gameinstance, BoardInstance, depth=0):
        '''
        :param dimensions: this is the dimensions of the board that is being played on
        :param ScoreBoard: this is the board, but with each cell having a score, instead of one for playing on.
        :param Gameinstance: The temporary instance of the game being used, and one that each combination will be fed
        into in order to score them
        :param Boardinstance: The temporary instance of the board being used, and one that each combination will be fed
        into in order to score them
        :param depth: This is the depth that the algorithm should go to. it is set to 0 if nothing is input when calling
        this function.

        This will get the children of the current state(each column), and will then use NEWUseMinMax in order to get the
        scores of each column. It will then run through the scores. If the score of a column is 0(if it is full), then
        the score will be set to -(10^30), and this ensures that the AI will not play in that column.
        After it has done this, it will find which column has the best score, and will return that column, and set
        self.Column_Place to that column.
        '''
        print("AI is deciding on a move")
        children = BoardInstance.GetEmptyColumns()
        ColumnScores = self.NEWUseMinMax(children, depth, Gameinstance, BoardInstance, dimensions, ScoreBoard)

        readableScores = []
        counter = 0
        for value in ColumnScores:
            counter += 1
            if ColumnScores[value] == 0:
                readableScores.append(-1*10**20)
            else:
                readableScores.append(float(ColumnScores[value]))

        TopScore = max(readableScores)
        BestColumn = readableScores.index(TopScore)
        print("Ranked columns as:", readableScores)
        self.Column_Place = BestColumn
        return self.Column_Place
