import os
import numpy as np
import wfdb
from google.cloud import storage

# Set up Google Cloud Storage client
project_id = 'cse531a-project'
storage_client = storage.Client(project=project_id)

# Define bucket name and destination folder
bucket_name = '531-project-team11'
destination_folder = 'icp_files_filtered/'

def fetch_bucket():
    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Iterate through blobs in the bucket
    for blob in bucket.list_blobs(prefix='icp_files_cpp/'):
        # Download the record from PhysioNet MIMIC-III
        record_name = os.path.basename(blob.name)
        record_name = os.path.splitext(record_name)[0]
        print(f"record_name is {record_name}")

        # Extract the relevant PhysioNet directory structure from the GCS blob name
        mimic_directory = os.path.join('mimic3wdb-matched/1.0', os.path.dirname(blob.name)[14:])  # Remove 'icp_files_cpp/' from the prefix

        # Download PhysioNet files locally
        wfdb.dl_database('mimic3wdb-matched', '1.0', mimic_directory)

        # Construct local file paths
        record_path = os.path.join(mimic_directory, record_name)

        # Read the downloaded WFDB record
        record = wfdb.rdrecord(record_name=record_name, pn_dir='.')

        # Check missing value percentage
        missing_values_percentage = np.count_nonzero(np.isnan(record.p_signal)) / record.sig_len

        # Copy to Google Cloud Storage if missing value percentage is less than 0.25
        if missing_values_percentage < 0.25:
            # Upload the record to the filtered folder in Google Cloud Storage
            path = os.path.join(mimic_directory, record_name)
            print(f"{record_name}.dat missing value is {missing_values_percentage} // path is {path}")
            destination_blob_name_dat = os.path.join(destination_folder, path + ".dat")
            destination_blob_name_hea = os.path.join(destination_folder, path + ".hea")
            print(f"{destination_blob_name_dat} and {destination_blob_name_hea}")

            # Upload .dat file
            blob_dat = bucket.blob(destination_blob_name_dat)
            blob_dat.upload_from_filename(record_path + ".dat")
            print(f"Record {record_name} (dat) copied to {destination_blob_name_dat}")

            # Upload .hea file
            blob_hea = bucket.blob(destination_blob_name_hea)
            blob_hea.upload_from_filename(record_path + ".hea")
            print(f"Record {record_name} (hea) copied to {destination_blob_name_hea}")

    print("DONE")

fetch_bucket()



