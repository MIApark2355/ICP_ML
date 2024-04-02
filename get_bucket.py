from google.cloud import storage
import wfdb
import io

# Initialize a Google Cloud Storage client
project_id = 'cse531a-project'
storage_client = storage.Client(project=project_id)

# Name of your Google Cloud Storage bucket
bucket_name = '531-project-team11'

# Prefix for the files you want to access (if they are in a folder)
prefix = 'matched/matched/p00/'

# Create a bucket object
bucket = storage_client.get_bucket(bucket_name)

# Recursively list the files in the specified bucket and prefix
def list_blobs_with_prefix(bucket, prefix):
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob for blob in blobs]

# Filter out the files that have ICP in the header
icp_files = []
count = 0
blobs = list_blobs_with_prefix(bucket, prefix)
for blob in blobs:
    # Read the header file (.hea) content
    if blob.name.endswith('n.hea'):
        header_content = blob.download_as_text()

        # Check if 'ICP' is in the header content
        if 'ICP' in header_content:
            # Extract the record name (without the .hea extension)
            record_name = blob.name[:-4]
            print(blob.name)
            icp_files.append(record_name)

# Print the list of files that have ICP in the header
print("Files with ICP in the header:", icp_files)