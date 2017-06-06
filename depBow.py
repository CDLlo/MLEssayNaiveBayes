from __future__ import print_function
import os
import io
import time
import re
import sys
import numpy as np
import pandas as pd
import math

Data = pd.read_csv('devVectorsBayes.csv')
Testset = pd.read_csv('vectorsBayes.csv')
totalInstances = Data.shape[0]
Tags = Data.tag.unique()
vecList = []
for elem in Tags:
    IndivTag = Data.loc[Data['tag'] == elem]
    IndivCounts = IndivTag.sum(numeric_only=1)
    #for t in IndivTag.keys():
        #print(IndivCounts[t])
    total = IndivCounts.sum()
    FinalTagVec = pd.Series([elem,IndivTag.shape[0],total,math.log(float(IndivTag.shape[0])/totalInstances)])
    FinalTagVec = FinalTagVec.rename({0: 'tag',1: 'count',2:'total',3:'freq'})
    FinalTagVec = FinalTagVec.append(IndivCounts)
    vecList.append(FinalTagVec)
BayesCounts = pd.concat(vecList, axis=1, keys=[s[0] for s in vecList])

right = 0
wrong = 0
counter = 0
for index, row in Testset.iterrows():
    #print('tag: ' + row['tag'])
    classVec = []
    for tag in Tags:
        BayesCounts[tag]
        sumVec = []
        for elem in Data.columns:
            if elem != 'tag':
                try:
                    sumVec.append(math.log(float(BayesCounts[tag][elem])/float(BayesCounts[tag]['total'])))
                except:
                    sumVec.append(0)
        pred = float(sum(sumVec)*BayesCounts[tag]['freq'])
        prediction = pd.Series([pred])
        prediction = prediction.rename({0:tag})
        #print(prediction)
        classVec.append(prediction)
        #print(classVec)
    #print(classVec)
    sys.stdout.write('\r'+str(counter))
    sys.stdout.flush()
    counter += 1
    predVec = pd.concat(classVec, axis=1,keys=[s.name for s in classVec])
    if predVec.transpose().sum(numeric_only=1).idxmax(axis=1) == tag:
        right += 1
    else:
        wrong += 1
print(right)
print(wrong)


#how to get rows by name
#BayesCounts.loc['expl']
