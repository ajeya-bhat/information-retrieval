import query
from Elasticsearch.ES import search_snippet
import json
import sys

def metrics(query_string):
  """
  A helper function to obtain performance metrics for the search engine for a particular query.
  Uses the results from elasticsearch as the true labels
  """
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
  return (tp, fp, fn, tn)

if __name__ == "__main__":
  assert len(sys.argv) == 2, "Please enter the query to run the search against"
  print(metrics(sys.argv[1]))
  # print(metrics("sea animals are dying in the ocean"))
  print(metrics("climate change talks"))
