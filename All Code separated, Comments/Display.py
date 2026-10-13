# IMPORT LIBRARIES
import pygame
import numpy as np
import sys
import time


class Display:
    def __init__(self, Dimensions):
        self.WindowWidth = 700
        self.WindowHeight = 700
        self.Colours = [(0, 0, 0), (35, 87, 255), (255, 0, 0), (255, 255, 0)]  # Black, Blue, Red, Yellow
        self.Rows = Dimensions[0]
        self.Columns = Dimensions[1]
        self.MakeSquareSize()
        self.CircRadius = (self.SquareSize / 2 - (self.SquareSize / 25))
        self.AmountBelow = self.WindowHeight - (self.SquareSize * self.Rows) - 5
        self.Create_Display()

    def MakeSquareSize(self):
        '''
        this creates the size of the square, by taking the predefined height and width, and then dividing it by
        whichever of the rows or columns there are more of in order to fit the maximum amount within that size whilst
        still looking good
        '''
        if self.Rows >= self.Columns:
            self.SquareSize = (self.WindowHeight // max(self.Rows+1, self.Columns+1))
        else:
            self.SquareSize = (self.WindowHeight // max(self.Rows, self.Columns))

    def Create_Display(self):
        '''
        Create_Display will make the interface for the game, so it can be used later. It will also make the width of
        the window to match that of the amount of columns, to remove blank space at the sides.
        '''
        self.NewWindowWidth = self.SquareSize * self.Columns
        self.Interface = pygame.display.set_mode((self.NewWindowWidth, self.WindowHeight))
        self.PlaceLocation = self.AmountBelow - self.SquareSize
        self.DrawStartBoard()

    def DrawStartBoard(self):
        '''
        This will create the initial board before any moves have been made. It does this by making a square of blue in
        the space where it is, and then placing a black circle in the center in order to get the "empty square" look
        '''
        Blue = self.Colours[1]
        Black = self.Colours[0]
        for column in range(self.Columns):
            for row in range(self.Rows):
                RectParams = (column * self.SquareSize, row * self.SquareSize + self.AmountBelow, self.SquareSize,
                              self.SquareSize)  # offset from left, offset from top, rectangle width, rectangle height
                pygame.draw.rect(self.Interface, Blue, RectParams)

                CircPos = (int((column + 0.5) * self.SquareSize), int((row + 0.5) * self.SquareSize + self.AmountBelow))
                pygame.draw.circle(self.Interface, Black, CircPos, self.CircRadius)
        pygame.display.update()

    def GameOver(self, Winner):
        '''
        This will take in the winner when called, and then will display which player has won as an overlay on the
        board. It will then wait until the user has clicked to exit the game, or to end the program.
        '''

        # code block here to display the winner
        pygame.init()
        myfont = pygame.font.SysFont("calibri", int(self.NewWindowWidth/11.6), True)
        if Winner == 5:
            myText = ("The board is full, click to exit")
        else:
            myText = ("Player " + str(Winner) + " Wins!, click to exit")
        label = myfont.render(myText, 1, self.Colours[0])
        pygame.draw.rect(self.Interface, (100, 255, 25), (0, self.WindowHeight//2, self.WindowWidth, 75))
        self.Interface.blit(label, (0, self.WindowHeight//2))
        pygame.display.update()

        time.sleep(1)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return False


    def PlaceCounter(self, Positions, MoveMade, Turn, SameColumn = False):
        '''
        This will take in a list of the positions, the column to place it in, whose turn it is and also whether or not
        it is the same column(for when going back moves). It will then take a location from the positions, and will then
        place a counter in that location on the pygame display interface. If it can't place it, it will let the user
        know and will return False
        '''
        try:
            Location = Positions[MoveMade]
        except:
            print("Invalid location")
            return False
        if Turn == 3:
            if Location[0] == -1:
                Row = 0
            else:
                Row = self.Rows - Location[0] + 1
            if SameColumn:
                Row += 1
        else:
            Row = self.Rows - Location[0]

        Column = MoveMade
        Red = self.Colours[2]
        Yellow = self.Colours[3]
        Black = self.Colours[0]

        if (Row == -1) or (Column == -1):
            return False
        else:
            CircPos = (int((Column + 0.5) * self.SquareSize), int((Row + 0.5) * self.SquareSize + self.AmountBelow))
            if Turn == 1:  # for it being P1
                pygame.draw.circle(self.Interface, Red, CircPos, self.CircRadius)
            if Turn == 2:  # for it being P2
                pygame.draw.circle(self.Interface, Yellow, CircPos, self.CircRadius)
            if Turn == 3: # for removing counter from board if move is gone back
                pygame.draw.circle(self.Interface, Black, CircPos, self.CircRadius)

            pygame.display.update()

            return True


    def GetPlacement(self, Turn, Positions, Enemy):
        '''
        This will wait for the user to click a column. Once the user has clicked on a column, it will attempt to place a
        counter in that column, and will return it. It doesn't care if the column is full, as that check is done later.
        If the user presses r, it will undo the previously made move (2 moves if playing against an AI, as otherwise it
        becomes the AI turn, and the player can't do anything)
        '''

        Yellow = self.Colours[3]
        Red = self.Colours[2]
        Black = self.Colours[0]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return 0


                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.Interface, Black, (0, self.PlaceLocation, self.WindowWidth, self.SquareSize))
                    posx = event.pos[0]
                    if Turn == 1:
                        pygame.draw.circle(self.Interface, Red, (posx, self.PlaceLocation + self.CircRadius), self.CircRadius)
                    else:
                        pygame.draw.circle(self.Interface, Yellow, (posx, self.PlaceLocation + self.CircRadius), self.CircRadius)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    MousePosition = event.pos[0]
                    ColumnToPlace = int(np.floor(MousePosition / self.SquareSize))
                    LocationValid = self.PlaceCounter(Positions, ColumnToPlace, Turn)

                    if LocationValid:
                        if Enemy == 2:
                            posx = event.pos[0]
                            if Turn == 1:
                                pygame.draw.circle(self.Interface, Yellow, (
                                    posx, self.PlaceLocation + self.CircRadius), self.CircRadius)
                            else:
                                pygame.draw.circle(self.Interface, Red, (
                                    posx, self.PlaceLocation + self.CircRadius), self.CircRadius)
                            pygame.display.update()
                        return ColumnToPlace + 1


