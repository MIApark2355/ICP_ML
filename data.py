import os
import wfdb

# Ensure the working directory is set to where the files are located
os.chdir('/Users/sominpark/Documents/GitHub/ICP_ML/data/waves')

# Now, read the record without specifying the path
record = wfdb.rdrecord('Patient01_Study01_RMCA_1')

# Plot the record
wfdb.plot_wfdb(record=record, title='Example signals')

