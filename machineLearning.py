# -*- coding: utf-8 -*-

import os
import json
import numpy as np
from sklearn import svm
import scipy.spatial

path = './data/'
# set to 0 if not wanted
outlierDetection = 1
# how many data points should be deleted?
outlierRate = 0.1
# how many principal components should be displayed?
amountComponents = 20

def createModel():
    print("started creating Model...")
    global clfSVM, X, Y

    # get data
    (X, Y) = get_training_data(path)

    # preprocessing of the data
    if outlierDetection == 1:
        # outlier detection
        distances = gammaidx(X, 5)
        # delete outliers from data and label
        indices = np.argsort(distances)[:int(outlierRate*len(distances))]
        X = np.delete(X, indices, 0)
        Y = np.delete(Y, indices, 0)

    # SVM classifier
    clfSVM = svm.SVC(kernel='linear', C=1)

    # fit SVM model
    clfSVM.fit(X,Y)
    print("done creating Model! \n")

    # with open("./test.json") as data_file:
        # print(data_file);
        # print(json.load(data_file));
        # print(clfSVM.predict(object_to_column(json.load(data_file))))

    return

# predict one data point and measure the time it takes
def predictEmoji(clientData):
    # convert json object to data structure for ML
    dataColumn = object_to_column(clientData)
    # predict emoji
    predictedEmoji = clfSVM.predict(dataColumn)
    # find the k nearest cluster
    nearestEmoji = find_nearest_cluster(dataColumn, 4)
    # returns string with emoji name, e.g. "joy"
    return [predictedEmoji, nearestEmoji]


# convert nested json structure to single column
def object_to_column(dataObject):
    dataColumn = []
    del dataObject["emojis"]["dominantEmoji"]
    flatObject = flatten_json(dataObject)
    for key, value in flatObject.items():
        dataColumn.append(float(value))
    return dataColumn

# convert json data in for ML suitable form
def get_training_data(path):
    dataMatrix = []
    dataColumn = []
    labels = []
    # for all persons
    for filename in os.listdir(path):
        with open(path+filename) as data_file:
            person = json.load(data_file)
            # for all emojis
            for emoji in person:
                # for all measurements
                for measurement in person[emoji]:
                    # for all objects
                    for dataObject in measurement:
                        del dataObject["emojis"]["dominantEmoji"]
                        flatObject = flatten_json(dataObject)
                        # for all individual values
                        for key, value in flatObject.items():
                            dataColumn.append(float(value))
                        if dataMatrix == []:
                            dataMatrix = dataColumn
                            labels.append(emoji)
                        else:
                            dataMatrix = np.vstack((dataMatrix, dataColumn))
                            labels.append(emoji)
                        dataColumn = []
    return (dataMatrix, labels)

# function to get a flat structure
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[str(name[:-1])] = str(x)

    flatten(y)
    return out

# Outlier detection
def gammaidx(X, k):
    #check input variable k; matrix is assumed to be in suitable shape
    if k < 1 or k > len(X):
        raise ValueError('Number of k nearest neighbors (k) not within the range (1, %d).\n' %len(X))
    #initialize y
    y = np.zeros(X.shape[0])
    #calculates vector-form distance vector
    dist = scipy.spatial.distance.pdist(X, 'euclidean')
    #converts the vector-form distance vector to a square-form distance matrix
    dist = scipy.spatial.distance.squareform(dist)
    #set diagonal distance to infinite as it is the distance of the point to itself
    np.fill_diagonal(dist, float('inf'), wrap=False)
    #sort the indices of all points by distance descending
    #cut the matrix to k entrys for each data point
    idx = np.argsort(dist)[:,:k]
    #creates row vector with range(X.shape[0]) indices
    #for being able to easily access the values from the dist matrix
    rowIdx = np.arange(X.shape[0]).reshape(X.shape[0],1)
    #calculates mean over coloums
    y = np.mean(dist[rowIdx,idx], axis=1)
    return y

# predict the k'th clostest cluster
def find_nearest_cluster(dataColumn, k):
    # find all data points for all clusters and calculate the mean respectively
    # for each cluster we need #features mean values
    X_mean = np.zeros((np.unique(Y).shape[0], X.shape[1]))
    # go through all cluster = emoji name
    for emojiName in np.unique(Y):
        Y_indices = []
        # go through all data points and check if they belong to cluster #counter
        for i, j in enumerate(Y):
            # if value in Y equals #counter
            if j == emojiName:
                # append index to Y_indices
                Y_indices.append(i)
        # when searching through all data points calculate mean of cluster
        clusterNumber = list(np.unique(Y)).index(emojiName)
        print("clusternum", clusterNumber)
        print("Y_indices", Y_indices)
        print("size X", X.shape)
        print("size X_mean", X_mean.shape)
        print("size Y_indices", np.asarray(Y_indices).shape)
        X_mean[clusterNumber,:] = np.mean(X[Y_indices,:], axis=0)
    # find out and return k nearest cluster
    dist = scipy.spatial.distance.cdist(dataColumn, X)
    distances = gammaidx(X_mean, k)
    print("distances", distances)
    print("dist", dist)
    # get list of nearest neighbours
    nearestEmoji = []
    indices = np.argsort(distances)
    for idx in indices:
        nearestEmoji.append(Y[idx])
    return nearestEmoji
