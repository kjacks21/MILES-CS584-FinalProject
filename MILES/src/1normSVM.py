#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 18:36:15 2016

@author: kyle
"""

import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.svm import LinearSVC

# classification step

# target contains the labels in order
target = pd.read_table('/media/kyle/My Passport/sample_files_183/labels_183.txt', header=None)
del target[0]
label_cv = target[1]

# convert label to binary
label_bin = []
for i in label_cv:
    if i == "t2d":
        label_bin.append(1)
    else:
        label_bin.append(0)
label_bin = pd.DataFrame(label_bin)



# if sim_mat is being read in
#sim_mat = np.load("sim_mat_183.npy")

clf = LinearSVC(penalty="l1", dual=False)

scores_accuracy = cross_val_score(clf, X=sim_mat, y=label_bin, cv=5, n_jobs=3, scoring="accuracy")

scores_f1 = cross_val_score(clf, sim_mat, label_bin, cv=5, n_jobs=3, scoring="f1")

scores_rocauc = cross_val_score(clf, sim_mat, label_bin, cv=5, n_jobs=3, scoring="roc_auc")

np.save("sim_mat_183.npy", sim_mat)

