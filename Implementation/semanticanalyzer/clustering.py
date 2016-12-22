from gensim.models import Doc2Vec
from sklearn.cluster import KMeans,DBSCAN
from sklearn.manifold import TSNE
import pandas as pd
import math
import matplotlib.pyplot as plt
import os
import re

docIds = pd.read_csv("/mnt/Semester/Major Final/Implementation/Resource_Files/docIds.csv", sep="\t",index_col=0)
model = Doc2Vec.load("/mnt/Semester/Major Final/Implementation/Resource_Files/SentenceVector.model")

class Clustering:
    ''' Class to cluster sentences on the basis of the given vectors '''
    def __init__(self,filepath):
        ''' Initializing the parameters for the clustering '''
        self.__filepath = filepath
        self.__fileSentenceVectors = []
        self.__fileDocId = None
        self.__labels = []
        self.__noOfSentences = 0
        self.__data = None

    def __getDestinationPath(self):
        ''' Function to get the destination path of the file '''
        self.__destination = "/mnt/Semester/Major Final/Implementation/Output/"+"/".join(self.__filepath.split('.')[0].split('/')[-2:])+"/"
        if not os.path.exists(self.__destination):
            os.makedirs(self.__destination)

    def __getFileData(self):
        ''' Function to get File Data and Number of Sentences'''
        with open(self.__filepath, 'r') as doc:
            self.__data = doc.read()
        self.__noOfSentences = self.__data.count('.') + self.__data.count('?') + self.__data.count('!') + 1

    def __findDocId(self):
        ''' Function to get Document Id of the Document'''
        self.__fileDocId = docIds.loc[docIds["Doc-Path"].str.match(self.__filepath)].values[0][0]

    def __findFileSenteceVectors(self):
        ''' Function to extract the Vectors of the Sentences of the file '''
        key = 0
        while key < self.__noOfSentences:
            try:
                # Checking if a sentence with this tag is in the model
                sentenceVector = model.docvecs["%s-%s" % (self.__fileDocId, key)]
            except KeyError:
                # Print the error
                print(str(self.__fileDocId) + '-' + str(key) + ' doesnt exist')
                self.__noOfSentences +=1
            else:
                # If yes then add it to the fileSentence Vector
                self.__fileSentenceVectors.append(sentenceVector)
            finally:
                # Always Run it
                key += 1

        # dis = []
        # for i in range(len(self.__fileSentenceVectors)):
        #     j = i+1
        #     while j < len(self.__fileSentenceVectors):
        #         dis.append(math.sqrt(sum(map(lambda a : a*a,self.__fileSentenceVectors[i] - self.__fileSentenceVectors[j]))))
        #         j += 1
        #
        # print(max(dis),min(dis),sum(dis)/len(dis))

    def cluster(self):
        ''' Function to cluster the sentences'''
        # Finding the parameters
        self.__getDestinationPath()
        self.__getFileData()
        self.__findDocId()
        self.__findFileSenteceVectors()

        # Running DBSCAN Algo
        dbscan = DBSCAN(eps=0.28,min_samples=2)
        dbscan.fit(self.__fileSentenceVectors)
        self.__labels = dbscan.labels_

        X_tsne = TSNE(perplexity=10).fit_transform(self.__fileSentenceVectors)
        plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=self.__labels, s = 70)
        plt.savefig(self.__destination + 'TNSE.png', bbox_inches='tight')

        self.__writeFile()

    def getLabels(self):
        ''' Function to return the labels '''
        return self.__labels

    def __writeFile(self):
        ''' Save the File '''
        self.__data = re.split("\n|\.|\?|\!", self.__data)
        for idx, sent in enumerate(self.__data):
            self.__data[idx] = " ".join(sent.split())
        data = list(filter(('').__ne__,self.__data))

        # Generating the Clustered Dataset
        labelledSent = {label: [idx for idx, label1 in enumerate(self.__labels) if label1 == label] for label in self.__labels}

        # Writing the to the file
        with open(self.__destination + 'cluster.txt', 'w') as doc:
            for key, values in labelledSent.items():
                for value in values:
                    doc.write(str(key) + ' : ' + str(value) + ' : ' + self.__data[value] + '\n')
                doc.write('\n')

if __name__ == '__main__':
    filename = '/mnt/Semester/Major Final/Implementation/Corpus/Dummy_Corpus/Sample Text 21.txt'
    # Start the clustering
    clusteringObject = Clustering(filename)
    clusteringObject.cluster()
