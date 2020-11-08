#imports
import time
import numpy
import pickle
import os

from tqdm import tqdm
import unicodedata
import re
import numpy as np
import pandas as pd
import sys
import nltk

from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from config import config_params

#preprocessing
def unicode_to_ascii(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s)
      if unicodedata.category(c) != 'Mn')


#initialize the stemmer and lemmatizer
lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
stopword_set = set(stopwords.words('english'))


def preprocess_sentence(w):

  w = unicode_to_ascii(w.lower().strip())

  # creating a space between a word and the punctuation following it
  w = re.sub(r"([?.!,¿])", r" \1 ", w)
  w = re.sub(r'[" "]+', " ", w)
  w=w.replace('.','')
  w=w.replace(',','')
  w=w.replace('!','')
  
  # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
  w = re.sub(r"[^a-zA-Z?.!,¿*]+", " ", w)
  preprocessed_sent  = []
  w = w.strip()
  if "*" not in w:
    tokenized_list = nltk.word_tokenize(w)
    for i in tokenized_list:
      if config_params['preprocess_type']==1:
          i=ps.stem(i)
      elif config_params['preprocess_type']==2:
        i=lemmatizer.lemmatize(i)
      if config_params["stopword_removal"]==1 and i in  stopword_set:
        continue
      preprocessed_sent.append(i)
  else:
    tokenized_list = w.split()
    for i in tokenized_list:
      i=i.strip()
      if '*' in i:
        preprocessed_sent.append(i)
        continue
      elif config_params['preprocess_type']==1:
        i=ps.stem(i)
      elif config_params['preprocess_type']==2:
        i=lemmatizer.lemmatize(i)
      if config_params["stopword_removal"]==1 and i in  stopword_set:
        continue
      preprocessed_sent.append(i)
  
  
    #root form reductions based on condition
  return preprocessed_sent

if __name__ == "__main__":
  #read the data
  #mapping from uuid to row, doc pair
  rowdict = {}
  #a dictionary that maps docid to its snippet
  rowsnip = {}
  #a dictionary that maps a row to its term list 
  rowterms = {}
  word_corpus = set()

  docid = 0

  for i in os.listdir('TelevisionNews'):
    try:
      df =  pd.read_csv(os.path.join('TelevisionNews', i))
    except:
      print(i+" was not processed")
      continue

    for index, row in df.iterrows():
      docid += 1
      rowdict[docid] = (index, os.path.join('TelevisionNews', i), str(row['Station']).lower(), str(row["Show"]).lower())
      rowsnip[docid] = row["Snippet"]
      word_corpus.update(row["Snippet"].split())


  for doc in tqdm(rowsnip):
    rowterms[doc] = preprocess_sentence(rowsnip[doc])

  #write the preprocessed document pickle files.
  with open("data/data.pkl", "wb") as f:
    pickle.dump({"rowsnip" : rowsnip, "rowterms":rowterms, "rowdict" : rowdict, "word_corpus" : word_corpus}, f)

