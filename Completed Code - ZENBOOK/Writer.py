class Writer:
    def __init__(self, FilePath):
        self.FileName = str(FilePath)

    def OpenFile(self, mode):
        '''
        This opens the file for either writing or reading, depending on which mode is fed in. It allows for the mode to
        be input for in case functionality for reading from text files is added.
        '''
        self.myfile = open(self.FileName, mode)

    def closeFile(self):
        '''
        This will close the text file
        '''
        self.myfile.close()

    def WriteFile(self, MovesMade, HowEnd):
        '''
        This will write the lines to the file
        '''
        self.OpenFile("a")
        myMoves = str(MovesMade) + str(HowEnd) + "\n"
        self.myfile.write(myMoves)
        self.closeFile()
