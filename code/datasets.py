import os
import csv
import numpy as np
import json

from tqdm import tqdm

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

seed = 3535999445

def race(path):    
    X, Y = [], []
    for i in range(3): #set
        X += [[]]
        Y += [[]]
        for j in range(9):
            X[i] += [[]]

    for k in range(3):
        if k == 2:
            y = 0
        with open(os.path.join(path, ["race_train.json", "race_dev.json", "race_test.json"][k]), "r") as f:
            data = json.load(f)
            for i in range(len(data)):
                s = data[i][0]
                for j in range(len(data[i][1])):
                    qid = ''.join(data[i][-1].split("/")[1:]) + "-" + str(j)
                    q = data[i][1][j]["question"]
                    X[k][0] += [s[0]]
                    X[k][6] += [s[1]]
                    X[k][7] += [s[2]]
                    X[k][8] += [s[3]]
                    X[k][1] += [q]
                    for l in range(4):
                        c = data[i][1][j]["choice"][l]
                        X[k][l+2] += [c]
                        if k != 2 and c == data[i][1][j]["answer"]:
                            y = l
                    Y[k] += [y]
                    
    trX1, trX2, trX3, trX4, trX5, trX6, trX7, trX8, trX9 = X[0][0], X[0][1], X[0][2], X[0][3], X[0][4], X[0][5], X[0][6], X[0][7], X[0][8]
    vaX1, vaX2, vaX3, vaX4, vaX5, vaX6, vaX7, vaX8, vaX9 = X[1][0], X[1][1], X[1][2], X[1][3], X[1][4], X[1][5], X[1][6], X[1][7], X[1][8]
    teX1, teX2, teX3, teX4, teX5, teX6, teX7, teX8, teX9 = X[2][0], X[2][1], X[2][2], X[2][3], X[2][4], X[2][5], X[2][6], X[2][7], X[2][8]
    trY = np.asarray(Y[0], dtype=np.int32)
    vaY = np.asarray(Y[1], dtype=np.int32)
    teY = np.asarray(Y[2], dtype=np.int32)
    return (trX1, trX2, trX3, trX4, trX5, trX6, trX7, trX8, trX9, trY), (vaX1, vaX2, vaX3, vaX4, vaX5, vaX6, vaX7, vaX8, vaX9, vaY), (teX1, teX2, teX3, teX4, teX5, teX6, teX7, teX8, teX9)
        

