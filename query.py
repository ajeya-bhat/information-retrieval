import pickle
from collections import defaultdict
from config import config_params
import indexes as index
import json


def preprocess_query(query):
  query = query.strip()
  channel = None
  show = None

  if '`' in query:
    #extract the field
    bt1 = query.index('`')
    bt2 = query.index('`', query.index('`')+1)

    channel = query[bt1+1:bt2]

    if '/' in channel:
      channel, show = channel.split('/')

    #strip the channel condition from the query
    query = query[bt2+1:]
  return query, channel, show

def postprocess_query(docs, channel, show):
  result = []
  #postprocess the docs and maintain only the ones with the given show/channel
  for doc in docs:
    if (not channel or data_dict['rowdict'][doc][2] == channel) and (not show or data_dict['rowdict'][doc][3] == show):
      result.append(doc)
  return result

#load the processed pickle file
with open("data/data.pkl", "rb") as f:
  data_dict = pickle.load(f)

if config_params["index"] == 1:
  index = index.TFIDFIndex(data_dict['rowterms'])
elif config_params["index"] == 2:
  index=index.BooleanQuery(data_dict['rowterms'])

#query = "brazif g*ment is defending its plan to build dozens of huge hydro-electric dams"
query="scientif*c communit*"
query, channel, show = preprocess_query(query)
docs = index.query(query)
docs = postprocess_query(docs, channel, show)

json_res={}
if config_params['index']==1:
  json_res['index']="vector space model(tf idf)"
elif config_params['index']==2:
  json_res['index']="boolean query"

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
  json_res['number_of_hits']='100+'
else:
  json_res['number_of_hits']=len(docs)
if(len(docs)>100):
  docs=docs[:100]
json_res['hits']=[]
for docid in docs:
  resdict={}
  resdict['id']=data_dict['rowdict'][docid][0]
  resdict['document_name']=data_dict['rowdict'][docid][1]
  resdict['station']=data_dict['rowdict'][docid][2]
  resdict['show']=data_dict['rowdict'][docid][3]
  resdict['snippet']=data_dict['rowsnip'][docid]
  json_res['hits'].append(resdict)

print(json.dumps(json_res,indent=1))
