import pickle
from collections import defaultdict
from config import config_params
import indexes as index
import json
from utils.timer import timer_decorator
import os
import datetime
import pandas as pd

with open(os.path.join('data', 'data.pkl'), "rb") as f:
    data_dict = pickle.load(f)

def preprocess_query(query):
  query = query.strip()
  channel = None
  show = None
  filters = {}

  if '<' in query:
    #extract doc
    bt1 = query.index('<')
    bt2 = query.index('>')
    filters['document'] = query[bt1+1:bt2]
    query = query[bt2+1:]
  else:
    filters['document'] = None

  if '`' in query:
    #extract the field
    bt1 = query.index('`')
    bt2 = query.index('`', query.index('`')+1)

    filters['channel'] = query[bt1+1:bt2]

    if '/' in filters['channel']:
      filters['channel'], filters['show'] = filters['channel'].split('/')

    #strip the channel condition from the query
    query = query[bt2+1:]
  return query, filters

def postprocess_query(docs,scores, filters):
  result = []
  score=[]
  if len(filters)==0:
    return docs, scores
  #postprocess the docs and maintain only the ones with the given show/channel
  for i in range(len(docs)):
    if ('channel' not in filters or len(filters['channel'])==0 or data_dict['rowdict'][docs[i]][2] == filters['channel']) and \
      ('show' not in filters or len(filters['show'])==0 or data_dict['rowdict'][docs[i]][3] == filters['show']) :
      result.append(docs[i])
      if(config_params['index']==1):
        score.append(scores[i])
  return result,scores


def prepare_query(query):
  global index
  #load the processed pickle file
  with open(os.path.join("data", "data.pkl"), "rb") as f:
    data_dict = pickle.load(f)

  new_rowterm_dict={}
  query, filters = preprocess_query(query)
  if filters['document'] is not None:    
    for j in data_dict['rowterms']:
      if data_dict['rowdict'][j][1].split(os.path.sep)[1][:-4] == filters['document']:
        new_rowterm_dict[j]=data_dict['rowterms'][j]
  else:
    new_rowterm_dict=data_dict['rowterms']
  if config_params["index"] == 1:
    index = index.TFIDFIndex(new_rowterm_dict)
  elif config_params["index"] == 2:
    index=index.BooleanQuery(new_rowterm_dict)
  elif config_params['index'] == 3:
    index =index.PositionalIndex(new_rowterm_dict)

  return perform_query(new_rowterm_dict,query, filters)

@timer_decorator
def perform_query(new_rowterm_dict,query, filters):

  docs = index.query(query)
  if config_params['index']==1:
    scores=[i[1] for i in docs]
    docs=[i[0] for i in docs]
  else:
    scores=[]
  docs, scores = postprocess_query(docs, scores, filters)
  return new_rowterm_dict, docs, scores

def main():
  d_dict, docs, scores = prepare_query(query)

  json_res={}
  if config_params['index']==1:
    json_res['index']="vector space model(tf idf)"
  elif config_params['index']==2:
    json_res['index']="boolean query"
  elif config_params['index']==3:
    json_res['index']="positional index"
  

  if config_params['stopword_removal']==1:
    json_res['stopword_removal']=True
  else:
    json_res['stopword_removal']=False
  if config_params['preprocess_type']==1:
    json_res['preprocessing']="stemming"
  elif config_params['preprocess_type']==2:
    json_res['preprocessing']="lemmatization"
  elif config_params['preprocess_type']==3:
    json_res['preprocessing']="none"

  if config_params['spell_check']==1:
    json_res['spell_check']=True
  else:
    json_res['spell_check']=False

  if config_params['tf_scheme']==1:
    json_res['tf_scheme']="Normal TF"
  elif config_params['tf_scheme']==2:
    json_res['tf_scheme']="1+log(tf)"
  elif config_params['tf_scheme']==3:
    json_res['tf_scheme']="log(1+tf)"


  if len(docs)>100:
    json_res['number_of_hits']='20+'
  else:
    json_res['number_of_hits']=len(docs)

  if(len(docs)>20):
    docs=docs[:20]
    if config_params['index']==1:
      scores=scores[:20]

  json_res['hits']=[]
  for j in range(len(docs)):
    resdict={}
    resdict['id']=data_dict['rowdict'][docs[j]][0]
    resdict['document_name']=data_dict['rowdict'][docs[j]][1]
    resdict['station']=data_dict['rowdict'][docs[j]][2]
    resdict['show']=data_dict['rowdict'][docs[j]][3]
    resdict['snippet']=data_dict['rowsnip'][docs[j]]
    if config_params['index']==1:
      resdict['score']=scores[j]
      
    json_res['hits'].append(resdict)
  print(json.dumps(json_res,indent=1))
  return json_res


if __name__ == "__main__":
  query = "`bbcnews` brazil's government was defending its plan to build dozens of huge hydro-electric dams"
  #query = "`BBCNEWS.201701:` brazil's government is defending its plan to build dozens of huge"
  #query = input()
  #query="scientific community"

  doclist = main()
  if config_params["index"] == 1:
    if "prev_queries.csv" in os.listdir("data"):
      df = pd.read_csv(os.path.join("data", "prev_queries.csv"), index_col=False)
    else:
      df = pd.DataFrame(columns = ["Query", "Time", "station", "show", "document", "rowid", "row_snippet"])
    df = df.append({
      "Query":query,
      "Time":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
      "station": doclist['hits'][0]["station"],
      "show":doclist['hits'][0]['show'],
      "document": doclist['hits'][0]["document_name"],
      "rowid" : doclist['hits'][0]['snippet'],
      "row_snippet" : doclist['hits'][0]['id']
    }, ignore_index = True)
    print(df)
    df.to_csv(os.path.join("data", "prev_queries.csv"), index = None)

