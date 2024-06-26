import os

def count_patients(directory):
    patient_count = 0
    # Traverse first level of directories
    for root, dirs, files in os.walk(directory):
        # Traverse second level of directories
        for dir in dirs:
            subdirectory = os.path.join(root, dir)
            if os.path.isdir(subdirectory):  # Ensure it's a directory
                # Count directories in this subdirectory
                print(subdirectory)
                patient_subdirs = [name for name in os.listdir(subdirectory) if os.path.isdir(os.path.join(subdirectory, name))]
                patient_count += len(patient_subdirs)
    return patient_count

patient_directory = "/Users/sominpark/Documents/531_filtered_final2/"  # Adjust to your base directory
patient_count = count_patients(patient_directory)
print(f"Number of patients: {patient_count}")

def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

folder_path =  "/Users/sominpark/Documents/531_filtered_final2/" # Adjust to the specific folder
folder_size = get_folder_size(folder_path)
def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

# Example usage:
readable_size = human_readable_size(folder_size)
print(f"Total size of '{folder_path}' is {readable_size}.")
