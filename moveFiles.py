#This code move the raw photos from the camera to a folder called RAW
#supprted extensions are .ARW .CR3 .PSD .JPG .PNG
import os
import glob
import shutil
 # Source folder path
source = r'I:\DCIM\100EOS_R'
folder_name = 'RAW'

# Creating the new folder path
destination = os.path.join(source, folder_name)

# Creating the new folder
os.makedirs(destination, exist_ok=True)  # Using exist_ok=True to avoid raising an error if the folder already exists

print(f"Folder '{destination}' created successfully.")

# gather all files
#allfiles = glob.glob(os.path.join(source, '*.ARW'))
allfiles = glob.glob(os.path.join(source, '*.CR3'))

print("Files to move:", allfiles)
 
# iterate on all files to move them to the destination folder
for file_path in allfiles:
    dst_path = os.path.join(destination, os.path.basename(file_path))
    shutil.move(file_path, dst_path)
    print(f"Moved {file_path} -> {dst_path}")

