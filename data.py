#!/bin/env python
import os
import wfdb
from pathlib import Path
import re 
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from patient import Patient
from sklearn.preprocessing import MinMaxScaler


def process_data(folder_path, header):
    data_list = []
    label_list = []

    patient_static = defaultdict(Patient)
    for filename in folder_path.glob('*.hea'):
        entity = filename.stem.split("_")
        id = entity[0][7:]

        hAbp, hIcp, Hct = None, None, None # Default values
        patient = patient_static.get(id)
        if patient:
            hAbp = patient.hAbp
            hIcp = patient.hIcp
            Hct = patient.Hct
        
        with open(filename.with_suffix('.hea'), 'r') as f:
            for line in f:
                if "#" in line:
                    feature, value = re.search(r'\b(?:hAbp|hIcp|Hct)\b', line)[0], re.search(r'\b\d+(\.\d+)?\b', line)[0]
                    if feature == "hAbp":
                        hAbp = (hAbp + float(value))/ 2 if hAbp else float(value)
                    elif feature == 'hIcp':
                        hIcp = (hIcp + float(value))/2 if hIcp else float(value)
                    elif feature == 'Hct':
                        Hct = (Hct + float(value) / 100)/2 if Hct else float(value) / 100

        patient_static[id] = Patient(Hct, hAbp, hIcp)

    for filename in folder_path.glob('*.dat'):  # Ensure we process only .dat files
        entity = filename.stem.split("_")
        id = entity[0][7:]
        artery_side = 1.0 if entity[2] == 'RMCA' else 2.0
        curr_patient = patient_static[id]
        hAbp, hIcp, Hct = curr_patient.hAbp if curr_patient.hAbp else -1, curr_patient.hIcp if curr_patient.hIcp else -1, curr_patient.Hct if curr_patient.Hct else -1  # Default values

        
        # Read the data record
        record = wfdb.rdrecord(str(filename.with_suffix('')), sampfrom=0)
        data = np.empty(record.sig_len, dtype=header)
        temp_labels = []

        for i, signal in enumerate(record.p_signal.T):
            if i == 0:
                data['ABP'] = signal
            elif i == 1:
                temp_labels = signal
            else:
                data['CBFV'] = signal

        data['Artery'] = np.full(record.sig_len, artery_side)
        data['hAbp'] = np.full(record.sig_len, hAbp)
        data['hIcp'] = np.full(record.sig_len, hIcp)
        data['Hct'] = np.full(record.sig_len, Hct)

        data_list.append(data)
        label_list.extend(temp_labels)

    aggregated_data = np.concatenate(data_list)
    aggregated_labels = np.array(label_list)
    # res = np.array(normalize_data(aggregated_data), dtype=header)
    return np.vstack(normalize_data(aggregated_data)), aggregated_labels


def split_data(data, labels, train_ratio=0.8, valid_ratio=0.00001):
    total_len = len(data)
    train_len = int(total_len * train_ratio)
    valid_len = int(total_len * (train_ratio + valid_ratio))

    train_data, train_labels = data[:train_len], labels[:train_len]
    valid_data, valid_labels = data[train_len:valid_len], labels[train_len:valid_len]
    test_data, test_labels = data[valid_len:], labels[valid_len:]

    return np.vstack(train_data), np.vstack(train_labels), np.vstack(valid_data), np.vstack(valid_labels), np.vstack(test_data), test_labels

def normalize_data(data):
    data_array = data.view((data.dtype[0], len(data.dtype.names)))

    min_vals = np.min(data_array, axis=0)
    max_vals = np.max(data_array, axis=0)
    normalized_data = (data_array - min_vals) / (max_vals - min_vals)
    return normalized_data