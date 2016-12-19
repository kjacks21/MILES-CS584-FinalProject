#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:57:16 2016

@author: kyle
"""

import pandas as pd
import numpy as np
from subprocess import call
from sklearn.svm import LinearSVC
    
seqs = open('/home/kyle/Desktop/sequences.txt', 'r')  # /data/scratch/kjacks21/ncbiDataC/sequences.txt
patients = pd.read_table('instance-table.txt', header=None).as_matrix() # /data/scratch/kjacks21/ncbiDataC/instance-table.txt

def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        l = min(len(s1), len(s2))
        s1 = s1[0:l]
        s2 = s2[0:l]
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

num_seqs = patients[-1,-1]
num_bags = patients.shape[0]

p_index = patients[:, 0]

for i in np.arange(num_bags):
    bag = open("/media/kyle/My Passport/sampled_sequences/sampled_" + p_index[i] + "_sequences.txt", 'r')   # /data/scratch/kjacks21/
    matrow = np.zeros(num_seqs, dtype=int)
    print(matrow)
    for j, seq in enumerate(seqs):
        print("bag " + str(i) + ", instance " + str(j))
        if (j >= patients[i, 1] and j <= patients[i, 2]):
            min_dist = 0
            print("min dist = 0")
        else:
            min_dist = 200
            for b_seq in bag:
                prev_min_dist = min_dist
                min_dist = min(prev_min_dist, hamming_distance(seq, b_seq)) # call mash distance here
                if(prev_min_dist != min_dist):
                    print("new min dist = " + str(min_dist))
        matrow[j] = min_dist
        bag.seek(0)
    np.savetxt("/data/scratch/kjacks21/" + p_index[i] + "_matrow.txt", matrow)
    bag.close() 
    seqs.seek(0)
    break
seqs.close()















