import gensim
import torch.nn as nn
import numpy as np
from collections import Counter
from torch.optim.lr_scheduler import *
from typing import List, Dict
from pathlib import Path
import os



def  getWord2Id() -> Dict:
    """
    word2id: word -> id
    is a dictionary which give each word in training set and valid set a id, range from 0 to n_words
    """
    path = ["./Dataset/test.txt", "./Dataset/train.txt"]
    word2id = Counter()
    for each in path:
        with open(each, encoding="utf-8", errors="ignore") as f:
            for line in f.readlines():
                sentence = line.strip().split()
                for word in sentence[1:]:
                    if word not in word2id.keys():
                        word2id[word] = len(word2id)
    return word2id


def getWord2Vec(word2id):
    """
    word2vec: word -> vector
    is a dictionary which give each word in training set and valid set a vector, range, the length of vector is 50
    """
    path = "./Dataset/wiki_word2vec_50.bin"
    preModel = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    word2vecs = np.array(np.zeros([len(word2id) + 1, preModel.vector_size]))
    for key in word2id:
        try:
            word2vecs[word2id[key]] = preModel[key]
        except Exception:
            pass
    return word2vecs


def getCorpus(path, word2id, maxLength=50):
    contents, labels = np.array([0] * maxLength), np.array([])
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f.readlines():
            sentence = line.strip().split()
            content = np.asarray([word2id.get(w, 0) for w in sentence[1:]])[:maxLength]
            padding = max(maxLength - len(content), 0)
            content = np.pad(content, ((0, padding)), "constant", constant_values=0)
            labels = np.append(labels, int(sentence[0]))
            contents = np.vstack([contents, content])
    contents = np.delete(contents, 0, axis=0)
    return contents, labels