from collections import Counter
import pandas as pd
import os
import math

# Creating a list of Stopwords
with open('../../Resource_Files/Hindi_Stop_Words.txt', 'r') as fileDesc:
    stopwords = set(fileDesc.read().split('\n'))

# Symbols and Punctuations to be removed
punctuations = ['।','॥','!','"','\'','`','``',':','\'\'','?',',',';']
symbols = ['.','~','/','@','#','$','%','^','&','<','>','+','*','\\','|','=','_','₹','(',')','[',']','{','}']
# Symbols which have different meaning depending on condition
specialSymbols = ['-']

class TfIdf:
    ''' Class to generate the TF-IDF Matrix '''
    def __init__(self,corpus):
        ''' Initializing the TfIdf Object'''
        self.corpus = corpus
        self.noOfFiles = len(corpus)
        # Initializing a Blank dataFrame for Tf Values
        self.tfMatrix = pd.DataFrame({})
        self.idfVector = pd.DataFrame({})
        self.tfIdfMatrix = pd.DataFrame({})
        self.lengthVector = pd.DataFrame({})

    def __getLengthOfEachText(self):
        ''' Function to find the length of all texts and save it in a list '''
        self.lengthVector = pd.DataFrame.from_dict({filename:[len(text)] for filename,text in self.corpus.items()})

    def __cleanCorpus(self):
        ''' Function to clean the corpus from all the symbols, punctuations and stopwords '''
        for filename in self.corpus:
            # Removing Symbols - Replacing them by a space
            for symbol in symbols:
                self.corpus[filename] = self.corpus[filename].replace(symbol,' ')
            # Removing Punctuations - Replacing them by a space
            for punctuation in punctuations:
                self.corpus[filename] = self.corpus[filename].replace(punctuation,' ')
            # Removing stopwords and extra spaces due to replacement of symbols and punctuations
            self.corpus[filename] = " ".join([word for word in self.corpus[filename].split() if word not in stopwords])

    def __findUniqueWordsAndFrequencies(self,text):
        ''' Function to find unique words and its frequencies '''
        return dict(Counter(text.split()))

    def __buildTfMatrix(self):
        ''' Function to build the tf Matrix '''
        # Looping over every Document and its Text
        for filename,text in self.corpus.items():
            wordFreqVector = self.__findUniqueWordsAndFrequencies(text)
            # Creating temprorary DataFrame for a single file
            docTf = pd.DataFrame({},columns=[filename])
            for word,freq in wordFreqVector.items():
                # Adding words of Document to the DataFrame
                docTf.loc[word] = [freq]
            # Merging the Document DataFrame with Main DataFrame
            self.tfMatrix = pd.concat([self.tfMatrix,docTf]).groupby(level = 0).sum()
        # Filling all NaN values with 0 and making them int
        self.tfMatrix = self.tfMatrix.fillna(0).astype(int)

    def __buildIdfVector(self):
        ''' Function to build idf Vector '''
        self.idfVector = self.tfMatrix.astype(bool).sum(axis=1)

    def __buildTfIdfMatrix(self):
        ''' Funtion to build tf-idf Matrix '''
        self.tfIdfMatrix = self.tfMatrix.divide(self.lengthVector.ix[0]).mul(math.log(1/self.idfVector.divide(self.noOfFiles)[0],10),axis=0)

    def __save(self):
        ''' Function to Save Matrices and Vectors in .csv and pickle '''
        # Saving in .csv Format
        self.lengthVector.to_csv("../../Resource_Files/lengthVector.csv",sep="\t")
        self.tfMatrix.to_csv("../../Resource_Files/tfmatrix.csv",sep="\t")
        self.idfVector.to_csv("../../Resource_Files/idfvector.csv",sep="\t")
        self.tfIdfMatrix.to_csv("../../Resource_Files/tfidfmatrix.csv", sep="\t")

        # Saving in pickle Format
        self.lengthVector.to_pickle("../../Resource_Files/lengthVector.pkl")
        self.tfMatrix.to_pickle("../../Resource_Files/tfmatrix.pkl")
        self.idfVector.to_pickle("../../Resource_Files/idfvector.pkl")
        self.tfIdfMatrix.to_pickle("../../Resource_Files/tfidfmatrix.pkl")

    def run(self):
        ''' Clean the corpus and start the calculation '''
        self.__getLengthOfEachText()
        self.__cleanCorpus()
        self.__buildTfMatrix()
        self.__buildIdfVector()
        self.__buildTfIdfMatrix()
        self.__save()


if __name__ == "__main__":
    # Folder where all documents are kept
    sourceFolders = ["../../Corpus/NDTV_Corpus/"]
    # Listing all the Files in the source folder
    files = sorted([sourceFolder + file for sourceFolder in sourceFolders for file in os.listdir(sourceFolder)])

    corpus = {}
    # Looping over all the files in the folder to generate a corpus
    for filename in files:
        with open(filename,'r') as fileDesc:
            corpus[filename] = fileDesc.read()

    tfIdfObject = TfIdf(corpus)
    tfIdfObject.run()