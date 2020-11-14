import os
import sys
import re
import random
import pickle

# hello there

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.timer import timer_decorator
import metrics

f = open('data/data.pkl', 'rb')
snippets = pickle.load(f)['rowsnip']
f.close()
# for key in snippets:
#     if(key > 10):
#         break
#     print(key, snippets[key])

# snippets = list(rowsnip.values())[0:10]
# print(snippets)
