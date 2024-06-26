import os
from google.cloud import storage

# Set up Google Cloud Storage client
project_id = 'cse531a-project'
storage_client = storage.Client(project=project_id)

# Define bucket name
bucket_name = '531-project-team11'

# Define local directory
local_directory = "/Volumes/SAMSUNG/531/"

def list_2depth_paths(root_dir):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        if len(os.path.relpath(root, root_dir).split(os.sep)) == 2:
            paths.append(os.path.relpath(root, root_dir))
    return paths

def copy_layout_files():
    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # List all 2-depth paths in local directory
    local_paths = list_2depth_paths(local_directory)

    # Iterate through local paths
    for local_path in local_paths:
        # Access corresponding path in Google Cloud Storage
        gcs_path = f'icp_files/{local_path}'
        blobs = bucket.list_blobs(prefix=gcs_path)
        for blob in blobs:
            # Extract file name
            file_name = os.path.basename(blob.name)
            # Check if the file ends with "t.hea"
            if file_name.endswith("t.hea"):
                # Construct the destination path in the local directory
                destination_path = os.path.join(local_directory, local_path, file_name)
                # Download the file from Google Cloud Storage to the local directory
                blob.download_to_filename(destination_path)
                print(f"File {file_name} copied to {destination_path}")

    print("DONE")

copy_layout_files()

