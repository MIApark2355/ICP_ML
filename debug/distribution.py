import wfdb
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re
import os
from collections import defaultdict

def process_data(folder_path, header, features):
    patient_files = defaultdict(list)
    for filename in folder_path.glob('*.dat'):
        patient_id = re.match(r'(Patient\d+)', filename.stem)
        if patient_id:
            patient_files[patient_id.group()].append(filename)
    
    for patient_id, files in patient_files.items():
        print(f"Processing data for {patient_id}")
        patient_data_list = []
        
        for file in files:
            record = wfdb.rdrecord(str(file.with_suffix('')), sampfrom=0)
            if record.p_signal is not None:
                expected_fields = len(header)
                actual_fields = record.p_signal.shape[1]
                if actual_fields < expected_fields:
                    # Pad the signal with default values (e.g., np.nan) to match the expected shape
                    padding = np.full((record.sig_len, expected_fields - actual_fields), np.nan)
                    signal = np.hstack((record.p_signal, padding))
                else:
                    signal = record.p_signal
                print(f"Adjusted shape of signal: {signal.shape}")
                data = np.core.records.fromarrays(signal.T, dtype=header)
                patient_data_list.append(data)
        
        if patient_data_list:
            aggregated_data = np.concatenate(patient_data_list)
            plot_distribution(aggregated_data, features, patient_id)
        else:
            print(f"No data available for {patient_id}")

def plot_distribution(data, features, patient_id):
    distribution_folder = "distribution"
    os.makedirs(distribution_folder, exist_ok=True) 
    for feature in features:
        plt.figure()
        plt.hist(data[feature], bins=50)
        plt.title(f'{patient_id} - Distribution of {feature}')
        plt.xlabel(feature)
        plt.ylabel('Frequency')
        file_path = os.path.join(distribution_folder, f"{patient_id}_{feature}_distribution.png")
        plt.savefig(file_path)
        plt.close()
        
header = [('hAbp', float), ('hIcp', float), ('Hct', float), ('ABP', float), ('CBFV', float)]
features = ['hAbp', 'hIcp', 'Hct', 'ABP', 'CBFV']

folder_path = Path('../data/waves')
process_data(folder_path, header, features)
