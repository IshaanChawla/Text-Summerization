import numpy as  np
import os
import pandas as pd
import pickle
import re
import time

try:
    with open('../Resource_Files/ImportantVariablesGeneratingCorpus.pkl','rb') as doc:
        impVar = pickle.load(doc)
except FileNotFoundError:
    impVar = {'serialNum' : -1, 'fileIndex' : -1}

class SingleFileCorpus:
    ''' Class to get to intigrate the corpus '''
    def __init__(self):
        ''' Function to initialize the parameters '''
        self.__docIds = pd.DataFrame({}, columns=['Doc-Id', 'Doc-Path'])
        self.__fileSentences = pd.DataFrame({}, columns=['Doc-Id', 'Sentence-Id', 'Sentence'])
        self.__serialNum = impVar['serialNum'] + 1
        self.__fileIndex = impVar['fileIndex'] + 1

    def __save(self):
        ''' Function to save the file in .csv formats '''
        try:
            previosDocIds = pd.read_csv("../Resource_Files/docIds.csv", sep="\t",index_col=0)
            previousFileSentences = pd.read_csv("../Resource_Files/fileSentences.csv", sep="\t",index_col=0)
        except FileNotFoundError:
            pass
        else:
            self.__docIds = pd.concat([previosDocIds, self.__docIds])
            self.__fileSentences = pd.concat([previousFileSentences, self.__fileSentences])
        finally:
            self.__docIds.to_csv("../Resource_Files/docIds.csv", sep="\t")
            self.__fileSentences.to_csv("../Resource_Files/fileSentences.csv", sep="\t")
            with open('../Resource_Files/ImportantVariablesGeneratingCorpus.pkl', 'wb') as doc:
                pickle.dump({'serialNum' : self.__serialNum,'fileIndex' : self.__fileIndex}, doc, protocol=pickle.HIGHEST_PROTOCOL)


    def __singleFileRun(self,sourceFolder,file):
        # Fetching the content of the file and breaking it into sentences.
        with open(sourceFolder + file, 'r') as doc:
            fileData = re.split("\n|\.|\?|\!", doc.read())
        fileData = list(filter(None, fileData))

        self.__docIds.loc[self.__fileIndex] = [self.__fileIndex, sourceFolder + file]
        # Adding sentences of the file to the dataframe
        for sentIndex, sentence in enumerate(fileData):
            self.__fileSentences.loc[self.__serialNum] = [self.__fileIndex, sentIndex, sentence]
            self.__serialNum += 1


    def __cleanFileSentences(self):
        ''' Function to clean File Sentences Corpus '''
        # Removing extra spaces left in the sentences
        self.__fileSentences['Sentence'] = self.__fileSentences['Sentence'].str.split(' ').apply(
            lambda sentList: " ".join([word for word in sentList if len(word) > 0]))

        # Removing Blank Lines
        self.__fileSentences["Sentence"].replace('', np.NaN, inplace=True)
        self.__fileSentences.dropna(subset=["Sentence"], inplace=True)

        # Saving in integers format rather than float
        self.__docIds['Doc-Id'] = self.__docIds['Doc-Id'].astype(int)
        self.__fileSentences['Doc-Id'] = self.__fileSentences['Doc-Id'].astype(int)
        self.__fileSentences['Sentence-Id'] = self.__fileSentences['Sentence-Id'].astype(int)

class SingleFileCorpusUsingMultipleSources(SingleFileCorpus):
    ''' Creating/Updating Corpus using Multiple Files '''
    def __init__(self, sourceFolders):
        ''' Function to initialize the parameters '''
        SingleFileCorpus.__init__(self)
        self.sourceFolders = sourceFolders

    def run(self):
        ''' Function to help generate the Single File Corpus '''
        # Looping over the folders to retreive the files
        for sourceFolder in self.sourceFolders:
            print(sourceFolder)
            # Listing all the files in folder
            files = os.listdir(sourceFolder)
            # Looping over the files
            for file in files:
                self._SingleFileCorpus__singleFileRun(sourceFolder, file)
                print(self._SingleFileCorpus__fileIndex)
                self._SingleFileCorpus__fileIndex += 1

        # Cleaning the Single File Corpus
        self._SingleFileCorpus__cleanFileSentences()

        # Saving the File
        self._SingleFileCorpus__save()


class SingleFileCorpusUsingSingleSource(SingleFileCorpus):
    ''' Creating/Updating Corpus using Single Source'''
    def __init__(self,filepath):
        ''' Initializing the parameters '''
        SingleFileCorpus.__init__(self)
        splitFilePath = filepath.split('/')
        self.__sourceFolder = "/".join(splitFilePath[:-1])+'/'
        self.__file = splitFilePath[-1]

    def run(self):
        ''' Function to generate the Single File Corpus '''
        self._SingleFileCorpus__singleFileRun(self.__sourceFolder, self.__file)

        # Cleaning the Single File Corpus
        self._SingleFileCorpus__cleanFileSentences()

        # Saving the File
        self._SingleFileCorpus__save()


if __name__ == '__main__':
    start_time = time.time()

    sourceFolders = ['./Dummy_Corpus/']

    # singleFileCorpusObject = SingleFileCorpusUsingMultipleSources([os.path.abspath(sourceFolder)+'/' for sourceFolder in sourceFolders])
    # singleFileCorpusObject.run()

    singleFileCorpusObject = SingleFileCorpusUsingSingleSource('/mnt/Semester/Major Final/Implementation/Corpus/Dummy_Corpus/Sample Text 8.txt')
    singleFileCorpusObject.run()

    print("time taken - " + str(time.time() - start_time))