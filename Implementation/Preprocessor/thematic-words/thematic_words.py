import pandas as pd
import numpy as np

class ThematicWords:
    ''' Class to generate the Thematic Words for every document '''
    def __init__(self,tfIdfMatrix,threshold = 7.0):
        ''' Initializing the attributes '''
        self.__tfIdfMatrix = tfIdfMatrix
        self.__threshold = threshold
        self.__thematicWords = pd.DataFrame({})

    def generateAll(self):
        ''' Function to generate the Thematic words '''
        # rows = self.__tfIdfMatrix.index
        # self.__thematicWords = self.__tfIdfMatrix.apply(lambda x : x > self.__threshold, raw = True).apply(lambda x : list(rows[x.values]),axis = 0)
        # # Saving the file .csv Format
        # self.__thematicWords.to_csv('../../Resource_Files/thematicwords.csv',sep="\t")

        self.__thematicWords['Words'] = []
        maxElements = self.__tfIdfMatrix.max()

        for col in self.__tfIdfMatrix.columns:
            self.__thematicWords.loc[col] = [[ind for ind in self.__tfIdfMatrix[self.__tfIdfMatrix[col] > 0.75 * maxElements[col]].index]]
        self.__thematicWords.to_csv('../../Resource_Files/thematicwords.csv', sep="\t")

if __name__ == "__main__":
    # Creating a DataFrame using the tfIdfMatrix kept in Resource Folder
    tfIdfMatrix = pd.read_csv("../../Resource_Files/tfidfmatrix.csv",sep="\t",index_col=0)

    # Deciding the threshold
    theshold = 7.0

    thematicWordsObject = ThematicWords(tfIdfMatrix,theshold)
    thematicWordsObject.generateAll()

