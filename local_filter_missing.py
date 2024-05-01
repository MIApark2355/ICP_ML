# import os
# import shutil
# import numpy as np
# import wfdb

# # Define the local directory where the records are stored
# local_directory = "/Volumes/SAMSUNG/531/"

# # Define the destination folder for saving records with missing values less than 0.25
# destination_folder = "/Users/sominpark/Documents/531_filtered/"

# def fetch_local_directory():
#     # Iterate through directories in the local directory
#     for root, dirs, files in os.walk(local_directory):
#         print("here")
#         for file in files:
#             if file.endswith("t.hea"):
#                 continue

#             elif file.endswith(".dat") and not file.endswith("n.hea") and (not file.endswith("layout.hea")):
#                 # Extract record name from .hea file
#                 record_name = os.path.basename(os.path.dirname(root)) + "/" + os.path.basename(root) + "/" + os.path.splitext(file)[0]

#                 # Read the WFDB record
#                 record_path = os.path.join(root, os.path.splitext(file)[0])
#                 record = wfdb.rdrecord(record_name=record_name)

#                 # Check missing value percentage
#                 missing_values_percentage = np.count_nonzero(np.isnan(record.p_signal)) / record.sig_len

#                 # Copy to the destination folder if missing value percentage is less than 0.25
#                 if missing_values_percentage < 0.25:
#                     # print(f"less with percent {missing_values_percentage}")
#                     # Get the relative path from the local directory
#                     relative_path = os.path.relpath(root, local_directory)
#                     # Construct the destination directory
#                     destination_record_path = os.path.join(destination_folder, relative_path)
#                     # Create the destination directory if it doesn't exist
#                     os.makedirs(destination_record_path, exist_ok=True)
#                     # Copy the .dat and .hea files to the destination directory
#                     shutil.copy(record_path + ".dat", destination_record_path)
#                     shutil.copy(record_path + ".hea", destination_record_path)
#                     print(f"Record {record_name} copied to {destination_record_path}")
#                 else:
#                     print(f"too many missing values with percent {missing_values_percentage}")

#     print("DONE")

# fetch_local_directory()

import os
import shutil
import numpy as np
import wfdb

# Define the local directory where the records are stored
local_directory = "/Volumes/SAMSUNG/531/"

# Define the destination folder for saving records with missing ICP and ABP values less than 0.25
destination_folder = "/Users/sominpark/Documents/531_filtered/"

def fetch_local_directory():
    # Iterate through directories in the local directory
    for root, dirs, files in os.walk(local_directory):
        print("here")
        for file in files:
            if file.endswith("t.hea"):
                continue

            elif file.endswith(".dat") and not file.endswith("n.hea") and (not file.endswith("layout.hea")):
                # Extract record name from .hea file
                record_name = os.path.basename(os.path.dirname(root)) + "/" + os.path.basename(root) + "/" + os.path.splitext(file)[0]

                # Read the WFDB record
                record_path = os.path.join(root, os.path.splitext(file)[0])
                record = wfdb.rdrecord(record_name=record_name)

                # Get the index of the "ICP" signal
                icp_signal_index = None
                abp_signal_index = None
                for i, signal in enumerate(record.sig_name):
                    if "ICP" in signal:
                        icp_signal_index = i
                    elif "ABP" in signal:
                        abp_signal_index = i

                # If both "ICP" and "ABP" signals are found, check missing value percentage for those signals
                if icp_signal_index is not None and abp_signal_index is not None:
                    # Extract the "ICP" and "ABP" signals
                    icp_signal = record.p_signal[:, icp_signal_index]
                    abp_signal = record.p_signal[:, abp_signal_index]

                    # Check missing value percentage for "ICP" signal
                    icp_missing_values_percentage = np.count_nonzero(np.isnan(icp_signal)) / len(icp_signal)

                    # Check missing value percentage for "ABP" signal
                    abp_missing_values_percentage = np.count_nonzero(np.isnan(abp_signal)) / len(abp_signal)

                    # Copy to the destination folder if missing ICP and ABP value percentages are less than 0.25
                    if icp_missing_values_percentage < 0.25 and abp_missing_values_percentage < 0.25:
                        # Get the relative path from the local directory
                        relative_path = os.path.relpath(root, local_directory)
                        # Construct the destination directory
                        destination_record_path = os.path.join(destination_folder, relative_path)
                        # Create the destination directory if it doesn't exist
                        os.makedirs(destination_record_path, exist_ok=True)
                        # Copy the .dat and .hea files to the destination directory
                        shutil.copy(record_path + ".dat", destination_record_path)
                        shutil.copy(record_path + ".hea", destination_record_path)
                        print(f"Record {record_name} copied to {destination_record_path}")
                    else:
                        print(f"too many missing values for record {record_name}")

    print("DONE")

fetch_local_directory()

