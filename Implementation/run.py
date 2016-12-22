import os
import re
from semanticanalyzer.clustering import Clustering
from ranking.featuresplusfuzzy import FeatureExtraction

if __name__ == '__main__':
    filepath = '/mnt/Semester/Major Final/Implementation/Corpus/Dummy_Corpus/Sample Text 12.txt'
    source = "/".join(filepath.split('/')[:-1]) + '/'
    file = filepath.split('/')[-1]
    dest = '/mnt/Semester/Major Final/Implementation/Output/' + source.split('/')[-2] + '/' + file.split('.')[0] + '/'
    if not os.path.exists(dest):
        os.makedirs(dest)

    with open(source + file) as f:
        data = re.split('\n|\.|\?|\!',f.read())

    for idx,sent in enumerate(data):
        data[idx] = " ".join(sent.split())
    data = list(filter(('').__ne__, data))

    clusteringObject = Clustering(filepath)
    clusteringObject.cluster()
    clusterLabels = clusteringObject.getLabels()

    featureObject = FeatureExtraction(data,source,file,dest)
    featureObject.run()
    rankedSentences = featureObject.getSortedRankedTuples()

    clusterTaken = []

    summary = ''
    for (idx,sentScore) in rankedSentences:
        if clusterLabels[idx] not in clusterTaken:
            summary += data[idx] + '.\n'
            if clusterLabels[idx] != -1:
                clusterTaken.append(clusterLabels[idx])

    with open(dest + 'Summarized ' + file, 'w') as doc:
        doc.write(summary)






