from collections import Counter
from multiprocessing import Pool
import math
import numpy as np
import pandas as pd
import pickle
import re
import time

# Creating a list of Stopwords
with open('../../Resource_Files/Hindi_Stop_Words.txt', 'r') as fileDesc:
    stopwords = set(fileDesc.read().split('\n'))

try:
    with open('../../Resource_Files/ImportantVariablesGeneratingCorpus.pkl','rb') as doc:
        impVar = pickle.load(doc)
except FileNotFoundError:
    impVar = {'serialNum' : -1, 'fileIndex' : -1}


# Symbols and Punctuations to be removed
punctuations = ['।','॥','!','"','\'','`','``',':','\'\'','?',',',';','“','”']
symbols = ['.','~','/','@','#','$','%','^','&','<','>','+','*','\\','|','=','_','₹','(',')','[',']','{','}']
# Symbols which have different meaning depending on condition
specialSymbols = ['-']


def findUniqueWordsAndFrequencies(text):
    ''' Function to find unique words and its frequencies '''
    return dict(Counter(text.split()))


def buildTfMatrixPoolFunction(docDetails):
    ''' Initializing Processes to speed up calculations '''
    wordFreqVector = findUniqueWordsAndFrequencies(docDetails[1])
    # Creating temprorary DataFrame for a single file
    docTf = pd.DataFrame({}, columns=[docDetails[0]])
    for word, freq in wordFreqVector.items():
        # Adding words of Document to the DataFrame
        docTf.loc[word] = [freq]
    return docTf


class TfIdf:
    ''' Class to generate the TF-IDF Matrix '''
    def __init__(self,corpus):
        ''' Initializing the TfIdf Object'''
        self.corpus = corpus
        self.noOfFiles = impVar['fileIndex'] + 1
        # Initializing a Blank dataFrame for Tf Values
        self.tfMatrix = pd.DataFrame({})
        self.idfVector = pd.DataFrame({})
        self.tfIdfMatrix = pd.DataFrame({})

    def __cleanCorpus(self):
        ''' Function to clean the corpus from all the symbols, punctuations and stopwords '''
        for filename in self.corpus:
            # Removing Symbols - Replacing them by a space
            for symbol in symbols:
                self.corpus[filename] = self.corpus[filename].replace(symbol,' ')

            # Removing Punctuations - Replacing them by a space
            for punctuation in punctuations:
                self.corpus[filename] = self.corpus[filename].replace(punctuation,' ')

            # Removing More than 1 Hyphenated Words
            self.corpus[filename] = " ".join(re.sub(r'(--(-*)| -(-*)?)', r' ',self.corpus[filename]).split())

            # Removing stopwords and extra spaces due to replacement of symbols and punctuations
            self.corpus[filename] = " ".join([word for word in self.corpus[filename].split() if word not in stopwords])


    def __buildTfMatrix(self):
        ''' Function to build the tf Matrix '''
        argList = [(filename,text) for filename,text in self.corpus.items()]
        pool = Pool(processes = 12)
        self.__docTfs = pool.map(buildTfMatrixPoolFunction,argList)

        for docTf in self.__docTfs:
            # Merging the Document DataFrame with Main DataFrame
            self.tfMatrix = pd.concat([self.tfMatrix, docTf]).groupby(level=0).sum()

    def __buildIdfVector(self):
        ''' Function to build idf Vector '''
        self.idfVector = self.tfMatrix.astype(bool).sum(axis=1)

    def __buildTfIdfMatrix(self):
        ''' Funtion to build tf-idf Matrix '''
        self.tfIdfMatrix = self.tfMatrix.apply(np.log).add(1).mul(math.log(1/self.idfVector.divide(self.noOfFiles)[0],10),axis=0)

        # Removing any ambiguity left in form of np.inf or np.NaN or -inf
        self.tfIdfMatrix = self.tfIdfMatrix.replace(np.inf,np.NaN)
        self.tfIdfMatrix = self.tfIdfMatrix.replace('-inf',np.NaN)
        self.tfIdfMatrix = self.tfIdfMatrix.fillna(0)

    def __cleanTfMatrix(self):
        ''' Post Cleaning of TfMatrix after being built '''
        startHyphen = self.tfMatrix.loc[self.tfMatrix.index.str.match('^-')]
        endHyphen = self.tfMatrix.loc[self.tfMatrix.index.str.match('^.*-$')]

        for row in startHyphen.itertuples():
            self.tfMatrix.loc[row[0][1:]] = startHyphen.loc[row[0]] + self.tfMatrix.loc[row[0][1:]] if (row[0][1:] in self.tfMatrix.index) else startHyphen.loc[row[0]].copy()
            self.tfMatrix = self.tfIdfMatrix[self.tfMatrix.index.str.match('^%s$' % row[0]) == False]

        for row in endHyphen.itertuples():
            self.tfMatrix.loc[row[0][:-1]] = endHyphen.loc[row[0]] + self.tfMatrix.loc[row[0][:-1]] if (row[0][:-1] in self.tfMatrix.index) else endHyphen.loc[row[0]].copy()
            self.tfMatrix = self.tfIdfMatrix[self.tfMatrix.index.str.match('^%s$' % row[0]) == False]

    def __joinPreviousMatrix(self):
        ''' Function to join previously built tf-idf matrixes '''
        try:
            previousTfMatrix = pd.read_csv("../../Resource_Files/tfmatrix.csv",sep="\t",index_col=0)
            previousIdfVector = pd.read_csv("../../Resource_Files/idfvector.csv",sep="\t",index_col=0)
        except FileNotFoundError:
            pass
        else:
            self.tfMatrix = pd.concat([previousTfMatrix,self.tfMatrix]).groupby(level=0).sum()
            self.idfVector = pd.concat([previousIdfVector,self.idfVector]).groupby(level=0).sum().sum(axis=1)
        finally:
            # Filling all NaN values with 0 and making them int
            self.tfMatrix = self.tfMatrix.fillna(0).astype(int)
            self.idfVector = self.idfVector.fillna(0).astype(int)

    def __save(self):
        ''' Function to Save Matrices and Vectors in .csv '''
        self.tfMatrix.to_csv("../../Resource_Files/tfmatrix.csv",sep="\t")
        self.idfVector.to_csv("../../Resource_Files/idfvector.csv",sep="\t")
        self.tfIdfMatrix.to_csv("../../Resource_Files/tfidfmatrix.csv", sep="\t")

    def run(self):
        ''' Clean the corpus and start the calculation '''
        self.__cleanCorpus()
        self.__buildTfMatrix()
        self.__cleanTfMatrix()
        self.__buildIdfVector()
        self.__joinPreviousMatrix()
        self.__buildTfIdfMatrix()
        self.__save()


if __name__ == "__main__":
    start_time = time.time()
    # Fetching all the document and their ids
    docIds = pd.read_csv("../../Resource_Files/docIds.csv",sep="\t",index_col=0)

    corpus = {}
    # Looping over all the files in the folder to generate a corpus
    for doc in docIds.itertuples():
        if(doc[0] == 2 or doc[0] == 3):
            with open(doc[2],'r') as fileDesc:
                corpus[doc[1]] = fileDesc.read()

    tfIdfObject = TfIdf(corpus)
    tfIdfObject.run()

    print("Time Taken - " + str(time.time() - start_time))