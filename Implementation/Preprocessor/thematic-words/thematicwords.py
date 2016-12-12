import pandas as pd
import numpy as np

class ThematicWords:
    ''' Class to generate the Thematic Words for every document '''
    def __init__(self,tfIdfMatrix,threshold):
        ''' Initializing the attributes '''
        self.__tfIdfMatrix = tfIdfMatrix
        self.__threshold = threshold
        self.__thematicWords = None

    def generate(self):
        ''' Function to generate the Thematic words '''
        rows = self.__tfIdfMatrix.index
        self.__thematicWords = self.__tfIdfMatrix.apply(lambda x : x > self.__threshold, raw = True).apply(lambda x : list(rows[x.values]),axis = 0)
        self.__thematicWords.to_csv('../../Resource_Files/thematicwords.csv',sep='\t')
        self.__thematicWords.to_pickle('../../Resource_Files/thematicwords.pkl')


if __name__ == "__main__":
    # Creating a DataFrame using the tfIdfMatrix kept in Resource Folder
    tfIdfMatrix = pd.read_pickle("../../Resource_Files/tfidfmatrix.pkl")

    # Deciding the threshold
    theshold = 0.004

    thematicWordsObject = ThematicWords(tfIdfMatrix,theshold)
    thematicWordsObject.generate()



