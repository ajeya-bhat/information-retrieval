from collections import defaultdict, Counter
from math import log10, sqrt
from preprocess import preprocess_sentence

class Index:
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
      return log10(1+tf)*idf

  def query(self, query_string):
    #returns a sorted list of docids, with decreasing cosine similarity

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
    return sorted(ranked_docs, key = lambda x : x[1], reverse = True)
