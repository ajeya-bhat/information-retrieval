import pandas as pd
import requests
from elasticsearch import helpers, Elasticsearch
import csv
import json
import sys
from pprint import pprint
import os

# make sure ES is up and running
# res = requests.get('http://localhost:9200')
# print(res.content)

# TODO - check doc id
def build_index(es, index, path):
    """ builds ES index """
    for _csv in sorted(os.listdir(path)):
        file = os.path.join(path, _csv)
        with open(file) as f:
            if(_csv != "CNN.200910.csv"):
                print(_csv)
                df = pd.read_csv(file)
                reader = csv.DictReader(f)
                helpers.bulk(es, reader, index=index, doc_type='_doc')

def delete_index(es, index):
    """ deletes ES index """
    try:
        if "." not in index:
            es.indices.delete(index=index)
            print("Successfully deleted", index)
    except Exception as error:
        print("indices.delete.error", error)

def cat_indices(es):
    """ lists ES indices """
    indices = es.indices.get_alias().keys()
    print(sorted(indices))

def search(es, index_name, search):
    res = es.search(index=index_name, body=search)
    print(json.dumps(res, indent = 3))

if __name__ == '__main__':
    # connect to our cluster
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es is not None:
            print(help(build_index))
            path = "../TelevisionNews"
            index = "test"

            build_index(es, index, path)
            cat_indices(es)

            # TODO - need to add types of queries
            # search_object = {'query': {'match_all': {}}}
            search_object = {"query": {"multi_match": {
                "query" : "brazil's government is defending its plan to build dozens of huge hydro-electric dams",
                "fields" : ["Snippet"]
            }}}
            search(es, index, json.dumps(search_object))
            # delete_index(es, index)
