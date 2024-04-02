from google.cloud import storage
import wfdb
import io

# Initialize a Google Cloud Storage client
project_id = 'cse531a-project'
storage_client = storage.Client(project=project_id)

# Name of your Google Cloud Storage bucket
bucket_name = '531-project-team11'

# Prefix for the files you want to access (if they are in a folder)
source_prefix = 'matched/matched/'
target_prefix = 'ICP/'

# Create a bucket object
bucket = storage_client.get_bucket(bucket_name)

# Function to copy a directory from one prefix to another
def copy_directory(bucket, source_prefix, target_prefix):
    blobs = bucket.list_blobs(prefix=source_prefix)
    for blob in blobs:
        # Create new blob for the target prefix
        new_blob = bucket.blob(blob.name.replace(source_prefix, target_prefix))
        # Copy data from the source blob to the new blob
        new_blob.rewrite(blob)

# Recursively list the files in the specified bucket and prefix
def list_blobs_with_prefix(bucket, prefix):
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob for blob in blobs]

# Filter out the directories that have ICP in the header and copy them to the new prefix
blobs = list_blobs_with_prefix(bucket, source_prefix)
for blob in blobs:
    if blob.name.endswith('.hea'):
        header_content = blob.download_as_text()
        if 'ICP' in header_content:
            # Extract the directory path
            directory_path = '/'.join(blob.name.split('/')[:-1]) + '/'
            # Copy the directory to the new prefix
            copy_directory(bucket, directory_path, directory_path.replace(source_prefix, target_prefix))

print("Directories with ICP in the header have been copied to the ICP prefix.")
