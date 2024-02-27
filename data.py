#!/bin/env python
import os
import wfdb
from pathlib import Path
import re 
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from patient import Patient

def parse_data():
    # Ensure the working directory is set to where the files are located
    # removers = ["#", " ", ]
    folder_path = Path('./physionet.org/files/neurocritical-pediatric/1.0.0/waves')

    header = [('Artery', int), ('hAbp', float), ('hIcp', float), ('Hct', float), ('ABP', float), ('CBFV', float)]

    # Now, read the record without specifying the path
    accessed = False

    # hAbp_list = []
    # hIcp_list = []

    # patient_Map = defaultdict(Patient)
    train_data = []
    validation_data = []
    test_data = []

    train_y = []
    valid_y = []
    test_y = []

    for filename in folder_path.iterdir():

        if not accessed:
            os.chdir('./physionet.org/files/neurocritical-pediatric/1.0.0/waves')
            accessed = True
        
        entity = filename.stem.split("_")
        # id = int(entity[0][7:])
        artery_side = 1 if entity[2] == 'RMCA' else 2
        hAbp = -1
        hIcp = -1
        Hct = -1
        
        with open(filename.stem + ".hea", "r") as f:
            lines = f.readlines()
        for line in lines:
            if "#" in line: 
                feature_pattern = re.compile(r'\b(?:hAbp|hIcp|Hct)\b')
                value_pattern = re.compile(r'\b\d+(\.\d+)?\b')
                feature = feature_pattern.search(line)[0]
                value = value_pattern.search(line)[0]
                if feature == "hAbp":
                    hAbp = float(value)
                elif feature == 'hIcp':
                    hIcp = float(value)
                elif feature == 'Hct':
                    Hct = float(value) / 100
        
        record = wfdb.rdrecord(filename.stem, sampfrom=0)
        data = np.empty(record.sig_len, dtype = header)
        temp_y = []
        for i, signal in enumerate(record.p_signal.T):
            if i == 0:
                data['ABP'] = signal
            elif i == 1:
                temp_y = signal
            else:
                data['CBFV'] = signal
        
        data['Artery'] = np.full(record.sig_len, artery_side)
        data['hAbp'] = np.full(record.sig_len, hAbp)
        data['hIcp'] = np.full(record.sig_len, hIcp)
        data['Hct'] = np.full(record.sig_len, Hct)

        temp_train = data[0:int(record.sig_len * 0.7)]
        temp_valid = data[int(record.sig_len * 0.7): int(record.sig_len*0.9)]
        temp_test = data[int(record.sig_len*0.9):]
        
        for i, t in enumerate(temp_train):
            train_data.append(t)
            train_y.append(temp_y[i])
        for i, t in enumerate(temp_valid):
            validation_data.append(t)
            valid_y.append(temp_y[i])
        for i, t in enumerate(temp_test):
            test_data.append(t)
            test_y.append(temp_y[i])
    #     if id in patient_Map:
    #         patient_Map[id].avg_abp = (patient_Map[id].avg_abp + np.mean(data['ABP']) ) / 2
    #         patient_Map[id].avg_icp = (patient_Map[id].avg_icp + np.mean(data['ICP'])) / 2

    #         if patient_Map[id].hct != None:
    #             patient_Map[id].hct = (patient_Map[id].hct + Hct) / 2 if Hct != -1 else patient_Map[id].hct
    #         else:
    #             patient_Map[id].hct = Hct if Hct != -1 else patient_Map[id].hct

    #         patient_Map[id].hAbp = (patient_Map[id].hAbp + hAbp) / 2
    #         patient_Map[id].hIcp = (patient_Map[id].hIcp + hIcp) / 2
    #     else:
    #         patient_Map[id] = Patient(np.mean(data['ABP']), np.mean(data['ICP']), Hct if Hct != -1 else None, hAbp, hIcp)

    # for key,value in patient_Map.items():
    #     print(key)
    #     print(value)
    return np.vstack(train_data), np.vstack(validation_data), np.vstack(test_data), np.array(train_y), np.array(valid_y), np.array(test_y)
