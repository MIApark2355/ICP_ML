import wfdb

def process_data(blob):
  filename = blob.name
  record = wfdb.rdrecord(str(filename.with_suffix('')), sampfrom=0)
  return record.sig_len

def fetch_bucket():
  record = wfdb.rdrecord(record_name='3300295_0025', pn_dir='mimic3wdb-matched/1.0/p00/p007184')
  print(record.sig_len)

fetch_bucket()

