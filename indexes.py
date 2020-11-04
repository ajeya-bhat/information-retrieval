from collections import defaultdict, Counter
from math import log10, sqrt
from preprocess import preprocess_sentence
from config import config_params
from functools import reduce
from nltk.corpus import words
from nltk.metrics import edit_distance
import pickle
from bstree import BSTNode

with open("data/data.pkl", "rb") as f:
  data_dict = pickle.load(f)

class Index:
  def process_spell_errors(self, query):
    if config_params["spell_check"]:
      split_query = query.split()
      result = []
      words_list = set(words.words()).union(data_dict['word_corpus'])

      for word in split_query:
        if word not in words_list and '*' not in word:
          print(word, "is not in dict")
          #process
          words_distance = zip(words_list, map(lambda x : edit_distance(word, x), words_list))
          best_word = reduce(lambda x,y : x if x[1]<=y[1] else y, words_distance)[0]
          word = best_word
          print("replaced with", word)
        result.append(word)
      query = result
    return " ".join(query)

  def query(self, q):
    pass

  def __init__(self, corpus_dictionary):
    pass

class TFIDFIndex(Index):
  index = defaultdict(lambda : defaultdict(int)) #index[term][docid] = tf(doc, term)
  idf = defaultdict(set)    #idf[term] = idf(term)
  ndocs = 0

  def __init__(self, corpus_dictionary, scheme = ""):

    self.ndocs = len(corpus_dictionary)
    self.scheme = scheme

    #build the inverted index
    for doc in corpus_dictionary:
      for term in corpus_dictionary[doc]:
        self.index[term][doc] += 1
        self.idf[term].add(doc)

    for term in self.idf:
      self.idf[term] = log10(self.ndocs/len(self.idf[term]) + 1e-10)

  def tfidf_score(self, tf, idf):
    if config_params['tf_scheme'] == 1:
      tf_idf=tf*idf
    if config_params['tf_scheme'] == 2:
      tf_idf=1+log10(tf+1e-10)
    if config_params['tf_scheme'] == 3:
      tf_idf=log10(1+tf)*idf
    return tf_idf

  def query(self, query_string):
    #returns a sorted list of docids, with decreasing cosine similarity
    query_string = self.process_spell_errors(query_string)

    query_terms = preprocess_sentence(query_string)
    query_frequencies = Counter(query_terms) #query_term : frequency(query_term) in the query

    dotproducts = defaultdict(int) #sum of dotproduct elements of tfidf of the query and the document
    magnitude = defaultdict(int) #stores the magnitude of the document tfidf vector
    query_magnitude = 0

    #calculate the cosine similarity for the docs
    for term in query_frequencies.keys():

      if term not in self.index:
        continue

      query_tfidf = self.tfidf_score(query_frequencies[term], self.idf[term])
      query_magnitude += query_tfidf**2
      for doc in self.index[term]:
        doc_tfidf = self.tfidf_score(self.index[term][doc], self.idf[term])
        dotproducts[doc] += query_tfidf * doc_tfidf
        magnitude[doc] += doc_tfidf**2

    query_magnitude = sqrt(query_magnitude)
    cosine_similarity = {}
    for doc in magnitude:
        cosine_similarity[doc] = dotproducts[doc] / (query_magnitude * sqrt(magnitude[doc]) + 1e-10)

    ranked_docs = list(cosine_similarity.items())

    ranked_docs = sorted(ranked_docs, key = lambda x : x[1], reverse = True)
    return [i[0] for i in ranked_docs]

class BooleanQuery(Index):
  index = defaultdict(set) #index[term][docid] = tf(doc, term)
  ndocs = 0
  term_set=set()
  term_list=[]

  def __init__(self, corpus_dictionary):

    self.ndocs = len(corpus_dictionary)
    for doc in corpus_dictionary:
      for term in corpus_dictionary[doc]:
        self.term_set.add(term)
        self.index[term].add(doc)
    self.term_list=sorted(list(self.term_set))[2:]
    self.tree=BSTNode(self.term_list)#bst of terms
    
  def query(self, query_string):
    query_string = self.process_spell_errors(query_string)
    query_terms = preprocess_sentence(query_string)
    print(query_terms,2)
    for term in query_terms:
      if '*' in term:
        pass
    query_terms.sort(key=lambda x: len(self.index[x]))
    return list(reduce(lambda x,y:x.intersection(y),map(lambda x:self.index[x], query_terms)))

