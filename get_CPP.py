import os
from google.cloud import storage

# Set up Google Cloud Storage client
project_id = 'cse531a-project'
storage_client = storage.Client(project=project_id)

# Define bucket name
bucket_name = '531-project-team11'

# Define local directory
local_directory = "/Volumes/SAMSUNG/531/"

def copy_n_dat_files():
    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Iterate through directories in the local directory
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            if file.endswith("n.hea"):
                print(file)
                hea_file_path = os.path.join(root,file)
                print(hea_file_path)

                # Read the .hea file to find the record name ending with "n"
                with open(hea_file_path, 'r') as hea_file:
                    for line in hea_file:
                        if line.endswith("n\n"):
                            record_name = os.path.splitext(os.path.basename(line.split()[0]))[0]
                            print(record_name)
                            break

                # Construct the source blob path in the Google Cloud Storage bucket
                source_blob_path = f"matched/matched/{os.path.relpath(root, local_directory)}/{record_name}.dat"

                # Construct the destination path
                destination_path = os.path.join(root, f"{record_name}.dat")

                # Copy the file from the bucket to the local directory
                blob = bucket.blob(source_blob_path)
                blob.download_to_filename(destination_path)
                print(f"File {source_blob_path} copied to {destination_path}")

    print("DONE")

copy_n_dat_files()
