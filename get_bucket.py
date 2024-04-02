from google.cloud import storage
import wfdb
import io

project_id = 'cse531a-project'
storage_client = storage.Client(project=project_id)

bucket_name = '531-project-team11'

prefix = 'matched/matched/p00/'

bucket = storage_client.get_bucket(bucket_name)

def list_blobs_with_prefix(bucket, prefix):
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob for blob in blobs]

# Filter out the files that have ICP in the header
icp_files = []
count = 0
blobs = list_blobs_with_prefix(bucket, prefix)
for blob in blobs:
    # Read the header file (n.hea) content
    if blob.name.endswith('n.hea'):
        header_content = blob.download_as_text()

        # Check if 'ICP' 
        if 'ICP' in header_content:
            record_name = blob.name[:-4]
            print(blob.name)
            icp_files.append(record_name)

print("Files with ICP in the header:", icp_files)