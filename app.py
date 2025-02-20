from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LoadClientConfigFile("D:\Python app\python-gdrive-upload\gdrive_upload_env\client_secret.json")
gauth.LocalWebserverAuth()  # Opens a web browser for authentication
drive = GoogleDrive(gauth)

# Define the local directory containing images
local_folder = "D:\Python app\python-gdrive-upload\gdrive_upload_env\image"  # Change this to your directory path

# Define the Google Drive folder ID where images will be uploaded
drive_folder_id = "1u8fcZtQnyEkCX81EvqYsTi2-Ly-Hvna8"  # Change this to your target folder ID

# Supported image extensions
image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")

# Check if the directory is empty
if not os.listdir(local_folder):
    print("The directory is empty. No files to upload.")
else:
    # Loop through files in the directory
    for filename in os.listdir(local_folder):
        if filename.lower().endswith(image_extensions):  # Filter only image files
            file_path = os.path.join(local_folder, filename)
            print(f"Uploading: {filename}")

            try:
                # Create a new file on Google Drive
                gfile = drive.CreateFile({"title": filename, "parents": [{"id": drive_folder_id}]})
                gfile.SetContentFile(file_path)
                gfile.Upload()
                
                print(f"Uploaded: {filename}")

                # Explicitly close the file handle
                gfile = None

                # Delete the file after successful upload
                os.remove(file_path)
                print(f"Deleted: {filename} from local storage")

            except Exception as e:
                print(f"Error uploading {filename}: {e}")

    print("All images uploaded and deleted successfully.")
