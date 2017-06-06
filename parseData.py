# -*- coding: utf-8 -*-
from __future__ import print_function
import spacy
import os
import io
import time
import re
import sys







caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    sentences = [s.decode('utf-8') for s in sentences]
    return sentences




def FileToSents(file):
    return split_into_sentences(file.read().replace('\n',''))



directory = '/media/clloyd/HardDrive/nli-shared-task-2017/data/essays/dev/original'
target = '/media/clloyd/HardDrive/nli-shared-task-2017/data/essays/dev/depend'
nlp = spacy.load('en_core_web_md')
counter = 1

for filename in os.listdir(directory):
    tempsource = directory +'/'+ filename
    temptarget = target + '/dep' + filename
    Ifile = open(tempsource,'r')
    Ofile = open(temptarget,'w')
    depDict = {}
    Sent_List = FileToSents(Ifile)
    for sent in Sent_List:
        doc = nlp(sent)
        for token in doc:
            depDict[(token.head.orth_,token.head.pos_,token.head.dep_)] = depDict.get((token.head.orth_,token.head.pos_,token.head.dep_),0) + 1
    for elem in depDict.keys():
        Ofile.write(str(elem[0]) + ',' + str(elem[1]) + ','+ str(elem[2]) + ',' + str(depDict[elem]) +'\n')
    Ifile.close()
    Ofile.close()
    sys.stdout.write('\r'+str(counter))
    sys.stdout.flush()
    counter += 1

#doc = nlp(u'I like green eggs and ham. John is a pill.')
#for token in doc:
#    print(token.head.orth_)
#for np in doc.noun_chunks:
#    print(np.text, np.root.text, np.root.dep_, np.root.head.text)
