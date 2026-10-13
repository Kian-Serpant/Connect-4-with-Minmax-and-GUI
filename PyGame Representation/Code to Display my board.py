import time
import pygame
import numpy as np
import sys

WindowWidth = 875
WindowHeight = 875
WindowSize = (WindowWidth, WindowHeight)

DefaultColumnCount = 140 # can pull this from my board class later
DefaultRowCount = 120 # can pull this from my board class later
MaxLengthOrWidth = max(DefaultColumnCount, DefaultRowCount) # should be changed to amount of rows and columns later

SquareSize = WindowWidth // MaxLengthOrWidth
CircRadius = (SquareSize / 2 - (SquareSize/25))

MyBoard = np.zeros((DefaultRowCount, DefaultColumnCount)) # can pull this from my board class later
Interface = pygame.display.set_mode(WindowSize) # makes the pygame interface size given

BlueOfBoard = (35, 87, 255)
Background = (0, 0, 0)

AmountVerticalTaken = SquareSize*DefaultRowCount
AmountBelow = WindowHeight - AmountVerticalTaken- 5

def DrawStartBoard(): # this works for any amount of rows and columns now
    for column in range(DefaultColumnCount):
        for row in range(DefaultRowCount):
            RectParams = (column * SquareSize, row * SquareSize + AmountBelow, SquareSize, SquareSize) # offset from left, offset from top, rectangle width, rectangle height
            pygame.draw.rect(Interface, BlueOfBoard, RectParams)

            CircPos = (int((column+0.5) * SquareSize), int((row+0.5) * SquareSize + AmountBelow))
            pygame.draw.circle(Interface, Background, CircPos, CircRadius)
            pygame.display.update()

def PlaceCounter(Positions, MoveMade, Turn, Rows):
    Location = Positions[MoveMade]
    Row = Rows - Location[0]
    Column = Location[1]
    Yellow = (255, 255, 0)
    Red = (255, 0, 0)

    CircPos = (int((Column + 0.5) * SquareSize), int((Row + 0.5) * SquareSize + AmountBelow))
    if Turn == 1: # for it being a human
        pygame.draw.circle(Interface, Red, CircPos, CircRadius)
    if Turn == 2: # for it being AI
        pygame.draw.circle(Interface, Yellow, CircPos, CircRadius)
    pygame.display.update()


def GetPlacement(Turn, SquareSize, enemy, Positions, TotRows, CounterHeight):
    Yellow = (255, 255, 0)
    Red = (255, 0, 0)
    Black = (0, 0, 0)
    CounterPlaced = False
    if enemy == 1: # this makes a counter follow the mouse but at the top, enemy being 1 represents a human
        while not CounterPlaced:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(Interface, Black, (0, CounterHeight, WindowWidth, SquareSize))
                    posx = event.pos[0]
                    if Turn == 1:
                        pygame.draw.circle(Interface, Red, (posx, CounterHeight+CircRadius), CircRadius)
                    else:
                        pygame.draw.circle(Interface, Yellow, (posx, CounterHeight+CircRadius), CircRadius)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    MousePosition = event.pos[0]
                    ColumnToPlace = int(np.floor(MousePosition / SquareSize))
                    LocationValid = True # temporary, update this to actually check if valid using classes from before
                    if LocationValid:
                        PlaceCounter(Positions, ColumnToPlace, Turn, TotRows)
                    CounterPlaced = True
                    posx = event.pos[0]
                    if Turn == 1:
                        pygame.draw.circle(Interface, Yellow, (posx, CounterHeight+CircRadius), CircRadius)
                    else:
                        pygame.draw.circle(Interface, Red, (posx, CounterHeight+CircRadius), CircRadius)
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


MoveCounterLocation = AmountBelow - SquareSize

DrawStartBoard()
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