import time
import pygame
import numpy as np
import sys


class Display:
    def __init__(self, Dimensions):
        self.WindowWidth = 875
        self.WindowHeight = 875
        self.Colours = [(0,0,0), (35, 87, 255), (255, 0, 0), (255, 255, 0)] # Black, Blue, Red, Yellow
        self.Rows = Dimensions[0]
        self.Columns = Dimensions[1]
        self.SquareSize = (self.WindowWidth // max(self.Rows, self.Columns))
        self.CircRadius = (self.SquareSize / 2 - (self.SquareSize/25))
        self.AmountBelow = self.WindowHeight - (self.SquareSize*self.Rows) - 5
        self.DrawStartBoard()

    def Create_Display(self):
        self.Interface = pygame.display.set_mode((self.WindowWidth, self.WindowHeight))
        self.PlaceLocation = self.AmountBelow - self.SquareSize

    def DrawStartBoard(self): # this works for any amount of rows and columns now
        Blue = self.Colours[1]
        Black = self.Colours[0]
        for column in range(self.Columns):
            for row in range(self.Rows):
                RectParams = (column * self.SquareSize, row * self.SquareSize + self.AmountBelow, self.SquareSize, self.SquareSize) # offset from left, offset from top, rectangle width, rectangle height
                pygame.draw.rect(self.Interface, Blue, RectParams)

                CircPos = (int((column+0.5) * self.SquareSize), int((row+0.5) * self.SquareSize + self.AmountBelow))
                pygame.draw.circle(self.Interface, Black, CircPos, self.CircRadius)
                pygame.display.update()

    def PlaceCounter(self, Positions, MoveMade, Turn):
        Location = Positions[MoveMade]
        Row = self.Rows - Location[0]
        Column = Location[1]
        Red = self.Colours[2]
        Yellow = self.Colours[3]

        CircPos = (int((Column + 0.5) * self.SquareSize), int((Row + 0.5) * self.SquareSize + self.AmountBelow))
        if Turn == 1: # for it being a human
            pygame.draw.circle(self.Interface, Red, CircPos, self.CircRadius)
        if Turn == 2: # for it being AI
            pygame.draw.circle(self.Interface, Yellow, CircPos, self.CircRadius)
        pygame.display.update()

    def GetPlacement(self, Turn, enemy, Positions):
        Yellow = self.Colours[3]
        Red = self.Colours[2]
        Black = self.Colours[0]

        CounterPlaced = False
        if enemy == 1: # this makes a counter follow the mouse but at the top, enemy being 1 represents a human
            while not CounterPlaced:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(self.Interface, Black, (0, self.PlaceLocation, self.WindowWidth, self.SquareSize))
                        posx = event.pos[0]
                        if Turn == 1:
                            pygame.draw.circle(self.Interface, Red, (posx, self.PlaceLocation+self.CircRadius), self.CircRadius)
                        else:
                            pygame.draw.circle(self.Interface, Yellow, (posx, self.PlaceLocation+self.CircRadius), self.CircRadius)
                    pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        MousePosition = event.pos[0]
                        ColumnToPlace = int(np.floor(MousePosition / self.SquareSize))
                        LocationValid = True # temporary, update this to actually check if valid using classes from before
                        if LocationValid:
                            self.PlaceCounter(Positions, ColumnToPlace, Turn, self.Rows)
                        CounterPlaced = True
                        posx = event.pos[0]
                        if Turn == 1:
                            pygame.draw.circle(self.Interface, Yellow, (posx, self.PlaceLocation+self.CircRadius), self.CircRadius)
                        else:
                            pygame.draw.circle(self.Interface, Red, (posx, self.PlaceLocation+self.CircRadius), self.CircRadius)
                        pygame.display.update()

        if enemy == 2:
            # USING AI MOVE, IT PLACES THE COUNTER IN POSITION AI SPECIFIES.
            pass

        # The code in the if True is temporary - it should be updated in the actual program
        if True:
            currentLocation = 0
            NewPosition = []
            for value in Positions:
                if currentLocation == ColumnToPlace:
                    NewValue = [value[0] + 1, value[1]]
                    NewPosition.append(NewValue)
                else:
                    NewPosition.append(value)
                currentLocation += 1

            return NewPosition



#Locations = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]]
Locations = []
for value in range(DefaultRowCount):
    LocationToAdd = [1, value]
    Locations.append(LocationToAdd)

#MoveMade = 4
#Turn = 1
#PlaceCounter(Locations, MoveMade, Turn, DefaultRowCount)
time.sleep(1)
for Value in range(1, 71):
    Turn = (Value % 2) + 1
    #PlaceCounter([[1, 1], [1, 2], [1, 3], [Value, 4], [1, 5], [1, 6], [1, 7]], MoveMade, Turn, DefaultRowCount)
    Locations = GetPlacement(Turn, SquareSize, 1, Locations, DefaultRowCount, MoveCounterLocation)

time.sleep(1)
GetPlacement()