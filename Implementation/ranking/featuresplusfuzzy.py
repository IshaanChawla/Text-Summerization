import os
import re
import numpy as np
import sys
import re
from .fuzzy import inference
from .singlefile import fun
import pandas as pd


class FeatureExtraction:
    def __init__(self, data,source,file,dest):
        self.__data = data
        self.__source = source
        self.__file = file
        self.__dest = dest
        self.__titlematrix = None
        self.__numerical = None
        self.__proper = None
        self.__length = None
        self.__max = 0
        self.__senetenceposition = None
        self.__thematicwords = None
        self.__featurematrix = np.ndarray(shape=(4, len(data)))

    def maxsentence(self, data):
        for s in data:
            le = len(s)
            if le > self.__max:
                self.__max = le
                # print (self.__max)


    def numericaldata(self, data):
        n = []
        for s in data:
            q = len(re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*[%]?\d", s))
            if s != '\n':
                k = s.split()
            t = len(k)
            n.append(q / (t + 1))
        self.__numerical = n

    def sentencelength(self, data):
        length = []
        for i in data:
            k = i.split()
            le = len(k)
            length.append(le)
        l = 0
        for i in length:
            length[l] = i / (self.__max)
            l += 1
        self.__length = length

    def titlewords(self, data):
        t = data[0].split()
        l = 0
        count = []
        for i in data:
            cnt = 0
            k = data[l].split()
            for val in t:
                if val in k:
                    cnt = cnt + 1
            l += 1
            count.append(cnt)
        l = 0
        for s in data:
            k = s.split()
            lent = len(k)
            if lent != 0:
                count[l] = count[l] / lent
            l += 1
        self.__titlematrix = count

    def propernoun(self, dest, file):
        sen = []
        with open(dest + 'tagged ' + file, 'r') as infile:
            data1 = infile.readlines()
        cou = 0
        senc = 0
        for i in data1:
            if i.split()[0] == '</s>':
                senc = cou / senc
                sen.append(senc)
                cou = 0
                senc = 0
            else:
                k = i.split()
                senc = senc + 1
                # print(senc)
                for j in range(len(k)):
                    if k[j] == 'NNP':
                        cou += 1
        self.__proper = sen

    # print(len(self.__proper))

    def sentencepositon(self, data):
        # l=0
        senp = []
        # print(k)
        for j in data:
            para = j.split('.')
            # print (para)
            n = len(para)
            # print(n)
            for i in range(n):
                # print(i)
                senp.append(max(1 / (i + 1), 1 / (n - i + 2)))
        # print(senp)
        self.__senetenceposition = senp

    # print(len(self.__senetenceposition))

    def thematicwords(self, filepath, data):
        # Loading the Pandas DataFrame
        docIds = pd.read_csv("/mnt/Semester/Major Final/Implementation/Resource_Files/docIds.csv", sep='\t', index_col=0)
        allThematicWords = pd.Series.from_csv("/mnt/Semester/Major Final/Implementation/Resource_Files/thematicwords.csv", sep='\t', index_col=0)

        # Getting the Document Id of the Document
        fileDocId = docIds.loc[docIds['Doc-Path'] == filepath].iloc[0]['Doc-Id']

        # Getting the Themaic Words of the Document
        thematicwrds = allThematicWords[allThematicWords.index == fileDocId].iloc[0][1:-1].replace("'", "").split(',')

        thematic = []
        for i in data:
            k = i.split()
            count = 0
            l = 0
            for j in k:
                for l in thematicwrds:
                    if j == l:
                        count = count + 1
            thematic.append(count / (len(thematicwrds)))
        self.__thematicwords = thematic

    def featurematrix(self):
        self.__featurematrix[0] = self.__numerical
        self.__featurematrix[1] = self.__length
        self.__featurematrix[2] = self.__titlematrix
        self.__featurematrix[3] = self.__thematicwords

    def getfeaturematrix(self):
        return self.__featurematrix

    def tagging(self,source,file,dest):
        fun(source,file,dest)

    def ranking(self,dest,file):
        k = self.getfeaturematrix()
        self.__rankedSentences = inference(k)
        self.__sortedRankedTuples = sorted([(idx,num) for idx,num in enumerate(self.__rankedSentences)],key = lambda tup: tup[1],reverse = True)

        with open(dest+'Ranked '+file,'w') as doc:
            for tup in self.__sortedRankedTuples:
                doc.write(str(tup[0]) + ' - ' + str(tup[1]) + '\n')

    def getRankedSentences(self):
        return self.__rankedSentences

    def getSortedRankedTuples(self):
        return self.__sortedRankedTuples

    def run(self):
        self.tagging(self.__source,self.__file,self.__dest)
        self.maxsentence(self.__data)
        self.numericaldata(self.__data)
        self.sentencelength(self.__data)
        self.titlewords(self.__data)
        self.propernoun(self.__dest,self.__file)
        self.sentencepositon(self.__data)
        self.thematicwords(self.__source + self.__file, self.__data)
        self.featurematrix()
        self.ranking(self.__dest, self.__file)




if __name__ == '__main__':

    filepath = '/mnt/Semester/Major Final/Implementation/Corpus/Dummy_Corpus/Sample Text 9.txt'
    source = "/".join(filepath.split('/')[:-1])+'/'
    file = filepath.split('/')[-1]
    dest = '/mnt/Semester/Major Final/Implementation/Output/' + source.split('/')[-2] + '/' + file.split('.')[0] + '/'
    if not os.path.exists(dest):
        os.makedirs(dest)

    with open(source + file) as doc:
        data = re.split('\n\!\?\.',doc.read())

    Object = FeatureExtraction(data,source,file,dest)
    Object.run()
