import os
import wfdb

# Ensure the working directory is set to where the files are located
os.chdir('/Users/sominpark/Documents/GitHub/ICP_ML/data/waves')

# Now, read the record without specifying the path
record = wfdb.rdrecord('Patient01_Study01_RMCA_1')


# Displaying the content of the record
print("Signal Names: ", record.sig_name)  # Names of the signals
print("Signal Units: ", record.units)    # Units of each signal
print("Sampling Frequency: ", record.fs, "Hz")  # Sampling frequency
print("Number of Samples: ", record.sig_len)    # Total number of samples in the record

# Displaying the first few samples of each signal
print("First few samples of each signal:")
for i, signal in enumerate(record.p_signal.T, start=1):
    print(f"Signal {i}: {signal[:10]}...")  # Prints the first 10 samples of each signal

# Plot the record
wfdb.plot_wfdb(record=record, title='Example signals')

