import os
from google.cloud import storage

# Set up Google Cloud Storage client
project_id = 'cse531a-project'
storage_client = storage.Client(project=project_id)

# Define bucket name
bucket_name = '531-project-team11'

# Define local directory
local_directory = "/Users/sominpark/Documents/531_filtered_final2"

def copy_hea_files_with_dash():
    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Iterate through directories in the local directory
    for root, dirs, files in os.walk(local_directory):
        # Ensure only two-layer patient folders are processed
        if root.count(os.sep) - local_directory.count(os.sep) == 2:
            # Define the cloud directory path corresponding to the local root
            cloud_directory = f"matched/matched/{os.path.relpath(root, local_directory)}"

            # List all objects in this specific cloud directory
            blobs = bucket.list_blobs(prefix=cloud_directory)
            for blob in blobs:
                if blob.name.endswith(".hea") and '-' in blob.name:
                    # Construct the destination path on local machine
                    local_file_path = os.path.join(root, os.path.basename(blob.name))
                    print(local_file_path)
                    
                    # Download the file
                    blob.download_to_filename(local_file_path)
                    print(f"Downloaded {blob.name} to {local_file_path}")

    print("DONE")

# Execute the function
copy_hea_files_with_dash()
