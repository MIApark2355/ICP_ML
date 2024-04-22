from google.cloud import storage
import wfdb
import io

project_id = 'cse531a-project'
storage_client = storage.Client(project=project_id)

bucket_name = '531-project-team11'

prefix = 'icp_files_24' #filtered dataset folder

bucket = storage_client.get_bucket(bucket_name)

blobs = bucket.list_blobs(prefix=prefix)

# Filter out the files that have ICP in the header
icp_files = []
count = 0
for blob in blobs:
    # Read the header file (n.hea) content
    if blob.name.endswith('.hea'):
        header_content = blob.download_as_text()

        # Check if 'ICP' 
        if 'ICP' in header_content:
            count +=1
            print("icp contained")
            # record_name = blob.name[:-4]
            # print(blob.name)
            # icp_files.append(record_name)

print("number of Files with ICP in the header:", count)