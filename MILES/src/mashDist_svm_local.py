#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:57:16 2016

@author: kyle
"""

import pandas as pd
import numpy as np
import subprocess as sp
import datetime as dt
import sourmash_lib

    
seqs = open('/media/kyle/My Passport/sample_files_183/sequences_183.txt', 'r')  # /data/scratch/kjacks21/ncbiDataC/sequences.txt
patients = pd.read_table('/media/kyle/My Passport/sample_files_183/instance-table_183.txt', header=None).as_matrix() # /data/scratch/kjacks21/ncbiDataC/instance-table.txt

#def hamming_distance(s1, s2):
#    if len(s1) != len(s2):
#        l = min(len(s1), len(s2))
#        s1 = s1[0:l]
#        s2 = s2[0:l]
#    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

num_seqs = patients[-1,-1] + 1
num_bags = patients.shape[0]

p_index = patients[:, 0]
sim_mat = np.zeros((num_bags, num_seqs))

# setting sourmash estimators

start = dt.datetime.now()
for i in np.arange(num_bags):
    bag = open("/media/kyle/My Passport/sampled_sequences_183/sampled_" + p_index[i] + "_sequences.txt", 'r')   # /data/scratch/kjacks21/
    print("Working on bag " + str(i) + "...")
    for j, seq in enumerate(seqs):
        if ((j % 1000) == 0):
            now = dt.datetime.now()
            print("Currently on bag " + str(i) + ", instance " + str(j) + " at time " + str(now - start))
        # set max_sim to 1 since the sequence is in the same bag
        if (j >= patients[i, 1] and j <= patients[i, 2]):
            max_sim = 1
            #print("max_sim = 1")
        else:
            # write seq file (test1.txt) in fasta format
            #with open("test1.txt", 'w') as f:
            #    f.write(">\n"+str(seq))
            E1 = sourmash_lib.Estimators(n=50,ksize=10)
            E1.add(seq.strip())
            
            max_sim = 0
            for b_seq in bag:
                prev_max_sim = max_sim
                
                # write b_seq fasta file (test2.txt) for mash
                #with open("test2.txt", 'w') as f:
                #    f.write(">\n"+str(b_seq))
                
                # calculate mash dist between
                #proc = sp.Popen(["/home/kyle/Documents/cs584/mash/mash-Linux64-v1.1.1/mash","dist","-k","15","-r","-p","3","test1.txt","test2.txt"], stdout=sp.PIPE)
                #output = str((proc.stdout.readline()), 'UTF8')
                #mash_dist = float((output.split('\t'))[2])
                E2 = sourmash_lib.Estimators(n=50,ksize=10)
                E2.add(b_seq.strip())
                
                max_sim = max(prev_max_sim, E1.jaccard(E2)) # call mash distance here
                #if prev_max_sim != max_sim:
                    #print("new max_sim = " + str(max_sim))
        #print("max_sim = " + str(max_sim))
        sim_mat[i, j] = max_sim
        bag.seek(0)
    #np.savetxt("/data/scratch/kjacks21/" + p_index[i] + "_matrow.txt", sim_mat)
    bag.close() 
    seqs.seek(0)
seqs.close()
end = time.time()
total_elapsed = end - start
print(total_elapsed)


np.save("/media/kyle/My Passport/sample_files_183/sim_mat_183.npy", sim_mat)

# reading saved .npy matrix file
sim_mat_183 = np.load("/media/kyle/My Passport/sample_files_183/sim_mat.npy")


########################################

#ignore


# testing
with open("test2.txt", 'w') as f:
    f.write(">\n"+str(b_seq))

with open("test1.txt", 'w') as f:
    f.write(">\n"+str(seq))

proc = sp.Popen(["/home/kyle/Documents/cs584/mash/mash-Linux64-v1.1.1/mash","dist","-r","test1.txt","test2.txt"], stdout=sp.PIPE)
output = str((proc.stdout.readline()), 'UTF8')
mash_dist = float((output.split('\t'))[2])





