#imports
import query
import json

from Elasticsearch.ES import search_snippet

"""
A helper function to obtain performance metrics for the search engine for a particular query.
Uses the results from elasticsearch as the true labels
Inputs:
  query_string : The query input of the user
Outputs:
  confusion_matrix : A tuple of true positive, true negative, false positive and false negative of the results returned by our search engine
"""
def metrics(query_string):
  
  results = query.main(query_string)
  es_results = search_snippet(query_string)
  es_doc_ids = {x['_source']['id'] for x in[i for i in es_results['hits']['hits']]}
  doc_ids = {x['_source']['id'] for x in [i for i in results['hits']]}
  # print(json.dumps(results, indent = 3))
  # print(json.dumps(es_results, indent = 3))

  # print(es_doc_ids)
  # print(doc_ids)
  tp = len(doc_ids.intersection(es_doc_ids))
  fp = len(doc_ids) - tp
  fn = len(es_doc_ids) - tp
  tn = query.ind.ndocs - tp - fp - fn
  confusion_matrix = (tp, fp, fn, tn)
  return confusion_matrix

if __name__ == "__main__":
  # print(metrics("brazil's government was defending its plan to build dozens of huge hydro-electric dams"))
  # print(metrics("sea animals are dying in the ocean"))
  print(metrics("climate change talks"))
