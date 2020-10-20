import pickle

#TODO: read the preprocessed index files and build inverted index and write it to file

with open("data/rowdict.pkl", "rb") as f:
  rowdict = pickle.load(f)

print(len(rowdict))
