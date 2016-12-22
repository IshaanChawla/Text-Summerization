import os
import pickle
import re

class CleanCorpus:
    ''' Class to get rid of unwanted things in the document '''
    def cleanFile(self,filepath):
        # Opening the file
        with open(filepath, 'r') as doc:
            data = doc.read()
        # Changing the पूर्णविराम(।) to fullstop(.)
        data = data.replace('।', '.')

        # Replacing all the hypens which include Ads and multi hyphens
        data = re.sub(r'(---+)(.|\n)*?(---+)', r' ', data)
        data = re.sub(r'(---+)', r' ', data)

        # Replacing all -- with - and -?|?- with - ?|? -
        data = re.sub(r'(--)', r' - ', data)
        data = re.sub(r'( -|- )', r' - ', data)

        # Writing the changes to the file
        with open(filepath, 'w') as doc:
            doc.write(data)


class CleanMultipleFiles(CleanCorpus):
    ''' Class to clean multiple files'''
    def __init__(self,sourceFolders):
        ''' Initializing the parameters '''
        self.__sourceFolders = sourceFolders

    def run(self):
        # Looping over the folders
        for sourceFolder in self.__sourceFolders:
            #Listing all the files
            files = os.listdir(sourceFolder)
            # Iterating over all the files
            for file in files:
                self.cleanFile(sourceFolder+file)


class CleanSingleFile(CleanCorpus):
    def __init__(self,sourceFile):
        ''' Initializing the parameters '''
        self.__sourceFile = sourceFile

    def run(self):
        self.cleanFile(self.__sourceFile)

if __name__ == '__main__':
    # sourceFolders = ['./Dummy_Corpus/','./IIT-B_Corpus/','./NDTV_Corpus/','./Agriculture_Corpus/']

    cleanObj = CleanSingleFile('/mnt/Semester/Major Final/Implementation/Corpus/Agriculture_Corpus/hi.tok')
    cleanObj.run()
