import pickle
from collections import defaultdict
from config import config_params
import indexes as index


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

if config_params["index"] == "tfidf":
  index = index.TFIDFIndex(data_dict['rowterms'])
elif config_params["index"] == "boolean":
  index=index.BooleanQuery(data_dict['rowterms'])



query = " `bbcnews/bbc news` brazil's government is defending its plan to build dozens of huge hydro-electric dams"
query, channel, show = preprocess_query(query)
docs = index.query(query)
docs = postprocess_query(docs, channel, show)

for docid in docs[:10]:
  print(data_dict['rowsnip'][docid])
  print(*data_dict['rowdict'][docid])
  print()
