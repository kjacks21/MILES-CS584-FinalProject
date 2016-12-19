#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 17:24:21 2016

@author: kyle
"""

import pandas as pd
import os

""" 
Get labels for subset of patients

"""

instance_table = pd.read_table('/media/kyle/My Passport/sample_files_183/instance-table_183.txt', header=None).as_matrix() # /data/scratch/kjacks21/ncbiDataC/instance-table.txt
labels = pd.read_table('/home/kyle/labels.txt', header=None).as_matrix()

# get IDs and labels for patients in the sample
#ID_list contains only ids from sampled patients
ID_list = []
labels_list = []
for seq_file in os.listdir("/media/kyle/My Passport/sampled_sequences_183"):
    # drop the ".txt" portion
    patient_id = str(seq_file[8:-14])
    ID_list.append(patient_id)

for line in labels:
    if line[0] in ID_list:
        labels_list.append(list(line))

# write labels_matrix to .txt
with open('/media/kyle/My Passport/sample_files_183/labels_183.txt','w') as f:
    for i in labels_list:
        f.write(i[0]+"\t"+i[1]+"\n")

    