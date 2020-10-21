import pickle
from collections import defaultdict
from config import config_params
import indexes as index

with open("data/data.pkl", "rb") as f:
  data_dict = pickle.load(f)

if config_params["index"] == "tfidf":
  index = index.TFIDFIndex(data_dict['rowterms'])

for docid in index.query("brazil's government is defending its plan to build dozens of huge hydro-electric dams")[:10]:
  print(data_dict['rowsnip'][docid[0]])
  print(*data_dict['rowdict'][docid[0]], docid[1])
  print()
