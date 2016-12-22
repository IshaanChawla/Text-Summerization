from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import numpy as np
import pandas as pd
import re
import time

class DocIterator(object):
    ''' Iterator to generate 1 doc at a time for Doc2Vec model '''
    def __init__(self, docSentList):
        ''' Inititalizing the Iterator parameters'''
        self.docSentList = docSentList

    def __iter__(self):
        ''' Iterator function to generate the next sentence'''
        for docSent in self.docSentList:
            yield LabeledSentence(words=docSent[3].split(),tags=["%s-%s" % (docSent[1],docSent[2])])


if __name__ == '__main__':
    start_time = time.time()
    # Fetching all the sentences from the corpus
    fileSentences = pd.read_csv("../Resource_Files/fileSentences.csv",sep="\t",index_col=0)
    sentenceList = [i for i in fileSentences.itertuples()]
    # Creating an generator for yielding the sentences
    it = DocIterator(sentenceList)
    # Creating Model and Build Vocab
    try:
        model = Doc2Vec.load("/mnt/Semester/Major Final/Implementation/Resource_Files/SentenceVector.model")
    except FileNotFoundError:
        model = Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025)
        model.build_vocab(it)

    # Iterating over the data to train the model
    for epoch in range(10):
        model.train(it)
        model.alpha = -0.002
        model.min_alpha = -0.002

    # Saving the model in resource files
    model.save("../Resource_Files/SentenceVector.model")
    print("Time Taken - " + str(time.time() - start_time))
