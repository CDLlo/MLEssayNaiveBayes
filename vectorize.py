# -*- coding: utf-8 -*-
from __future__ import print_function
import spacy
import os
import io
import time
import re
import sys
import numpy as np
import pandas as pd

x = re.compile('dep')
y = re.compile('\.txt|dep')


directory = '/media/clloyd/HardDrive/nli-shared-task-2017/data/essays/dev/depend'
counter = 1

featureList = ['acomp','advcl','advmod','agent','amod','appos','attr','aux','auxpass','cc','ccomp','complm','conj','csubj','csubjpass','dep','det','dobj','expl','hmod','hyph','infmod','intj','iobj','mark','meta','neg','nmod','npadvmod','nsubj','nsubjpass','number','oprd','parataxis','partmod','pcomp','pobj','poss','possessive','preconj','predet','prep','prt','punct','quantmod','rcmod','root','xcomp']
vectorList = []
Tfile = open('/media/clloyd/HardDrive/nli-shared-task-2017/data/labels/dev/labels.dev.csv','r')
#Taglist = np.array(Tfile.read().split('\n')
Taglist = pd.read_csv(Tfile)
Taglist = Taglist[['test_taker_id','L1']]
b = os.listdir(directory)
b.sort()
A = pd.DataFrame(b, columns = ['names'])
A['indexNumber'] = [int(re.sub('\D','',i)) for i in A['names']]
A.sort_values(['indexNumber'], ascending = [True], inplace = True)
A.drop('indexNumber', 1, inplace = True)
Taglist['filename'] = A
targetfilename = 'devVectorsBayes.csv'
Ofile = open(targetfilename,'w')
Ofile.write('tag,acomp,advcl,advmod,agent,amod,appos,attr,aux,auxpass,cc,ccomp,complm,conj,csubj,csubjpass,dep,det,dobj,expl,hmod,hyph,infmod,intj,iobj,mark,meta,neg,nmod,npadvmod,nsubj,nsubjpass,number,oprd,parataxis,partmod,pcomp,pobj,poss,possessive,preconj,predet,prep,prt,punct,quantmod,rcmod,root,xcomp\n')
for elem in Taglist.itertuples():
    tempsource = directory +'/'+ elem[3]
    temptarget = 'trainVectors.csv'
    Ifile = open(tempsource,'r')
    vecDict = {}
    table = Ifile.read().split('\n')
    for line in table:
        if line:
            templist = re.split('(?<!\+),(?=[A-Za-z])|(?<=\D),(?=\d)',line)
            try:
                vecDict[templist[2]] = vecDict.get(templist[2],0) + int(templist[3])
            except:
                print(line)
                print(templist)
    Ofile.write(elem[2])
    for dep in featureList:
        Ofile.write(',' + str(vecDict.get(dep,0)))

    Ofile.write('\n')
    Ifile.close()
    sys.stdout.write('\r'+str(counter))
    sys.stdout.flush()
    counter += 1
Ofile.close()
