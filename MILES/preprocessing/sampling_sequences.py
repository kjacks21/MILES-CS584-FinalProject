#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 18:37:24 2016

@author: kyle
"""
######
# This file is used to generate the necessary files with sampling and after sampling
######

import os
import random
import pandas as pd

##############################################################################
# get samples from each file

def file_len(fname):
    """Get file length"""
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
for seq_file in os.listdir("/media/kyle/My Passport/sequences"):
    file = "/media/kyle/My Passport/sequences/"+ seq_file
    num_reads = file_len(file)
    n = int(num_reads / 1000)  # change denominator to alter sample size ratio
    random_indices = random.sample(range(num_reads), n)
    
    # write new files from random samples
    # new_file contains patient file sampling
    new_file = open("/media/kyle/My Passport/sampled_sequences/sampled_"+seq_file, "w")
    # original file with contigs
    f = open(file)
    lines = f.readlines()
    for index in random_indices:
        new_file.write(str(lines[index]))
        
    f.close()
    new_file.close()
    
##############################################################################    
# create IDsequences.txt using sample files
# format is patient_ID <tab> sequence
# intention is to get sequences.txt and instance_table.txt from this
id_file = open("/media/kyle/My Passport/sample_files_183/IDsequences_183.txt", "w")
for seq_file in os.listdir("/media/kyle/My Passport/sampled_sequences_183"):
    file = "/media/kyle/My Passport/sampled_sequences_183/"+seq_file
    # drop the ".txt" portion
    patient_id = str(seq_file[8:-14])
    f = open(file)
    for line in f:
        id_file.write(patient_id+"\t"+str(line))
    f.close()
id_file.close()

 
#############################################################################
# generate sequences.txt and instances-table.txt from IDsequences.txt
IDseq = pd.read_table('/media/kyle/My Passport/sample_files_183/IDsequences_183.txt', header=None).as_matrix()
# old instance-table
#old_table = pd.read_table('instance-table.txt', header=None).as_matrix() # this doesn't need to be run every time
seq_file = open("/media/kyle/My Passport/sample_files_183/sequences_183.txt", "w")
instance_table = open("/media/kyle/My Passport/sample_files_183/instance-table_183.txt", "w")

# generate sequences.txt
for index, line in enumerate(IDseq):
    seq_file.write(line[1]+"\n")  
seq_file.close()

# generate instance-table.txt
ID = IDseq[0][0]
instance_table.write(str(ID)+"\t0\t")
for i, line in enumerate(IDseq):
    index = i
    if i == 0:
        pass
    else:
        if line[0] == IDseq[i-1][0]:
            pass
        else:
            instance_table.write(str(i-1)+"\n"+str(line[0])+"\t"+str(i)+"\t")
instance_table.write(str(index))
instance_table.close()   

#############################################################################
from shutil import copyfile

# get subset of patient files
random_indices = list(random.sample(range(367), 183))
for i, patient_file in enumerate(os.listdir("/media/kyle/My Passport/sampled_sequences")):
    if i in random_indices:
        copyfile("/media/kyle/My Passport/sampled_sequences/"+patient_file, "/media/kyle/My Passport/sampled_sequences_183/"+patient_file)
        print("moving "+patient_file)



