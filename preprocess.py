#imports 
import time
import numpy
import pickle
import os
import tqdm
import unicodedata
import re
import numpy as np
import pandas as pd
import sys
import nltk

from nltk.stem import WordNetLemmatizer, PorterStemmer  
from config import config_params

#read the data
#mapping from uuid to row, doc pair
rowdict = {}
#a dictionary that maps docid to its contents
rowsnip = {}
docid = 0

for i in os.listdir('TelevisionNews'):
  try:
    df =  pd.read_csv(os.path.join('TelevisionNews', i))
  except:
    print(i+" was not processed")
    continue

  for index, row in df.iterrows():
    docid += 1
    rowdict[docid] = (index, os.path.join('TelevisionNews', i))
    rowsnip[docid] = row["Snippet"]

#preprocessing
def unicode_to_ascii(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s)
      if unicodedata.category(c) != 'Mn')


lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
def preprocess_sentence(w):
  w = unicode_to_ascii(w.lower().strip())

  # creating a space between a word and the punctuation following it
  w = re.sub(r"([?.!,¿])", r" \1 ", w)
  w = re.sub(r'[" "]+', " ", w)
  w=w.replace('.','')
  w=w.replace(',','')
  w=w.replace('!','')

  # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
  w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)

  w = w.strip()

  tokenized_list = nltk.word_tokenize(w)
  preprocessed_sent=''
  for i in tokenized_list:
    
    #root form reductions based on condition
    i=i.strip()
    if config_params['preprocess_type']=='stemming':
      i=ps.stem(i)
    elif config_params['preprocess_type']=='lemmatization':
      i=lemmatizer.lemmatize(i)
    preprocessed_sent+=i
    preprocessed_sent+=' '
  
  return preprocessed_sent

for doc in rowsnip:
  print(rowsnip[doc])
  print()
  print()
  rowsnip[doc] = preprocess_sentence(rowsnip[doc])
  print(rowsnip[doc])

  print()


#write the preprocessed document pickle files.
with open("data/rowdict.pkl", "wb") as f:
  pickle.dump(rowdict, f)

with open("data/rowsnip.pkl", "wb") as f:
  pickle.dump(rowsnip, f)

