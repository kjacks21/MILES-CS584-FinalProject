#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:57:16 2016

@author: kyle
"""

import pandas as pd
import numpy as np
import subprocess as sp
import time


    
seqs = open('/home/kjacks21/MILES/sequences_183.txt', 'r')  # /data/scratch/kjacks21/ncbiDataC/sequences.txt
patients = pd.read_table('/home/kjacks21/MILES/instance-table_183.txt', header=None).as_matrix() # /data/scratch/kjacks21/ncbiDataC/instance-table.txt

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

start = time.time()
for i in np.arange(num_bags):
    bag = open("/data/scratch/kjacks21/sampled_sequences_183/sampled_" + p_index[i] + "_sequences.txt", 'r')   # /data/scratch/kjacks21/
    for j, seq in enumerate(seqs):
        print("bag " + str(i) + ", instance " + str(j))
        # set min_dist to 0 since the sequence is in the same bag
        if (j >= patients[i, 1] and j <= patients[i, 2]):
            min_dist = 0
            print("min dist = 0")
        else:
            # write seq file (test1.txt) in fasta format
            with open("/home/kjacks21/MILES/test1.txt", 'w') as f:
                f.write(">\n"+str(seq))
            
            min_dist = 200
            for b_seq in bag:
                prev_min_dist = min_dist
                
                # write b_seq fasta file (test2.txt) for mash
                with open("/home/kjacks21/MILES/test2.txt", 'w') as f:
                    f.write(">\n"+str(b_seq))
                
                # calculate mash dist between
                proc = sp.Popen(["/home/kjacks21/MILES/mash-Linux64-v1.1.1/mash","dist","-k","12","-r","test1.txt","test2.txt"], stdout=sp.PIPE)
                output = str((proc.stdout.readline()), 'UTF8')
                mash_dist = float((output.split('\t'))[2])
                
                min_dist = min(prev_min_dist, mash_dist) # call mash distance here
                if prev_min_dist != min_dist:
                    print("new min dist = " + str(min_dist))
        sim_mat[i, j] = min_dist
        bag.seek(0)
    #np.savetxt("/data/scratch/kjacks21/" + p_index[i] + "_matrow.txt", sim_mat)
    bag.close() 
    seqs.seek(0)
    
    # if cluster time limit is met, break and say where the last bag was
    if (time.time() - start)/60 > 717:
        with open("/home/kjacks21/MILES/last_bag_183.txt", 'w') as f:
            f.write("Last bag was sampled_"+str(p_index[i])+"_sequences.txt")
        break
        
seqs.close()
end = time.time()
total_elapsed = end - start
print(total_elapsed)

np.save("/home/kjacks21/MILES/sim_mat_183.npy", sim_mat)


########################################


# testing
#with open("test2.txt", 'w') as f:
#    f.write(">\n"+str(b_seq))

#with open("test1.txt", 'w') as f:
#    f.write(">\n"+str(seq))

#proc = sp.Popen(["/home/kyle/Documents/cs584/mash/mash-Linux64-v1.1.1/mash","dist","-r","test1.txt","test2.txt"], stdout=sp.PIPE)
#output = str((proc.stdout.readline()), 'UTF8')
#mash_dist = float((output.split('\t'))[2])


############################################











