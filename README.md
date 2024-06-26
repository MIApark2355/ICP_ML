# ICP_ML

1. Description
Our project is to improve a non-invasive predictive model alternative to invasive intracranial pressure (ICP) monitoring. 

2. Dataset
Both datasets are stored in Google Cloud Storage(GCP), and subsets are saved locally

(a)Neurocritical care waveform recordings in pediatric patients
(b)MIMIC-III Waveform Database Matched Dataset

The dataset for filtered MIMIC-III and Neurocritical Waveform was downloaded locally to process the data. 
To run the code, download the dataset using the following command:

wget -r -N -c -np --user <username> --ask-password https://physionet.org/files/neurocritical-pediatric/1.0.0/

Then in the 'final.ipynb', run eacch code block to train and view results of regression models.

The hyperparameter tuning is performed in 'main.py'. Run the command 'python main.py' to see the results of hyperparameter tuning on the dataset. 
3. Installation
[Installing WFDB]
This project relies on the WFDB (WaveForm DataBase) Python package for handling waveform data. Follow these steps to install the WFDB package:

Install WFDB using pip: 
    pip install wfdb
