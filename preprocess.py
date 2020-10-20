import time
import numpy
import pickle
import os

import unicodedata
import re
import numpy as np
import pandas as pd


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


def preprocess_sentence(w):
  #TODO: use if statements and argparse
  w = unicode_to_ascii(w.lower().strip())

  # creating a space between a word and the punctuation following it
  # eg: "he is a boy." => "he is a boy ."
  # Reference:- https://stackoverflow.com/questions/3645931/python-padding-punctuation-with-white-spaces-keeping-punctuation
  w = re.sub(r"([?.!,¿])", r" \1 ", w)
  w = re.sub(r'[" "]+', " ", w)

  # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
  w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)

  w = w.strip()

  # adding a start and an end token to the sentence
  # so that the model know when to start and stop predicting.
  return w

for doc in rowsnip:
  rowsnip[doc] = preprocess_sentence(rowsnip[doc])


#write the preprocessed document pickle files.
with open("data/rowdict.pkl", "wb") as f:
  pickle.dump(rowdict, f)

with open("data/rowsnip.pkl", "wb") as f:
  pickle.dump(rowsnip, f)

