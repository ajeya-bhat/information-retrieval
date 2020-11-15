import os
import sys
import re
import random
import pickle

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from preprocess import preprocess_sentence
from config import config_params
from utils.timer import timer_decorator
import metrics

def compare_scores(snippets):
    corpus = ''.join(snippets)
    # print(corpus)
    corpus_list = corpus.split('.')
    # print(corpus_list)
    # (tp, fp, fn, tn)
    scores_dict = dict()
    F1avg = 0
    zero_F1 = 0
    for i in range(0,50):
        query = random.choice(corpus_list)
        if(len(query.split()) < 5 or len(query.split()) > 12):
            continue
        print("iteration number:", i)
        print(query)

        # preprocess the query
        query = " ".join(preprocess_sentence(query)) if config_params["es_preprocess"] else query
        scores = metrics.metrics(query)

        precision = scores[0] / (scores[0] + scores[1] + 1e-9)
        recall = scores[0] / (scores[0] + scores[2] + 1e-9)
        F1 = 2*precision*recall/(precision + recall + 1e-9)
        if(F1 >= 0.4):
            scores_dict[query] = F1
        if(F1 == 0.0):
            zero_F1 += 1
        F1avg += F1
        print('scores:', scores)
        print('F1-score:', F1, 'precision:', precision, 'recall:', recall)
        print()
    print(F1avg/50)
    print(zero_F1)
    return scores_dict

def compare(snippets):
    try:
        print('in try block')
        f = open('data/scores.pkl', 'rb')
        scores_dict = pickle.load(f)
        f.close()
        scores_dict.update(compare_scores(snippets))
    except:
        print('in except')
        scores_dict = compare_scores(snippets)
        # print(scores_dict)
    finally:
        print('in finally')
        print(scores_dict)
        f = open('data/scores.pkl', 'wb')
        pickle.dump(scores_dict, f)
        f.close()

if __name__ == "__main__":
    f = open('data/data.pkl', 'rb')
    snippets = list(pickle.load(f)['rowsnip'].values())
    f.close()
    compare(snippets)
