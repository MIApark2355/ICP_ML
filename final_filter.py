import os
import shutil

# Define the source and destination directories
source_dir = "/Users/sominpark/Documents/531_filtered/"
destination_dir = "/Users/sominpark/Documents/531_filtered_final2/"

# Iterate through the directories in the source folder
for root, dirs, files in os.walk(source_dir):
    # Store .dat files to check for matches with .hea files
    dat_files = {file for file in files if file.endswith(".dat")}
    
    for file in files:

        if file.endswith(".hea"):
            # print(file)
            # Get the first 7 letters of the .hea file name
            base_name = file[:7]
            
            # Look for the corresponding .dat file
            corresponding_dat_file1 = base_name + "n.dat"
            corresponding_dat_file2 = file[:-4] + ".dat"

            print(corresponding_dat_file2)
            
            if corresponding_dat_file1 in dat_files and corresponding_dat_file2 in dat_files:
                # Construct the destination path based on the current root
                print("found")
                dest_path = root.replace(source_dir, destination_dir)
                
                # Check if the destination path exists, if not create it
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                
                # Copy the .hea and .dat files
                shutil.copy(os.path.join(root, file), os.path.join(dest_path, file))
                shutil.copy(os.path.join(root, corresponding_dat_file1), os.path.join(dest_path, corresponding_dat_file1))
                shutil.copy(os.path.join(root, corresponding_dat_file2), os.path.join(dest_path, corresponding_dat_file2))

print("Copying complete.")
