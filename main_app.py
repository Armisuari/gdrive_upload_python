from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import os
import logging

# Configuration
# SERVICE_ACCOUNT_FILE = r"angkasa-timelapse-657ac1e75cd3.json"  # Change this!
SERVICE_ACCOUNT_FILE = r"angkasa-timelapse-2657d62dcdab.json"  # Change this!
LOCAL_FOLDER = r"image"  # Change this!
DRIVE_FOLDER_ID = "1u8fcZtQnyEkCX81EvqYsTi2-Ly-Hvna8"  # Change this!
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")

def init_logger():
    logger = logging.getLogger('GoProLogger')
    logger.setLevel(logging.DEBUG)
    os.system('sudo chmod 666 app.log')
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(console_handler)
    return logger

def authenticate_service_account(service_account_file, logger):
    try:
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            service_account_file, 
            ["https://www.googleapis.com/auth/drive"]
        )
        logger.info("Service account authenticated successfully.")
        return GoogleDrive(gauth)
    except Exception as e:
        logger.error(f"Error authenticating service account: {e}")
        raise

def upload_images_to_drive(drive, local_folder, drive_folder_id, image_extensions, logger):
    if not os.path.exists(local_folder):
        logger.error(f"Error: The folder '{local_folder}' does not exist!")
        return

    if not os.listdir(local_folder):
        logger.info("The directory is empty. No files to upload.")
        return

    for filename in os.listdir(local_folder):
        if filename.lower().endswith(image_extensions):
            file_path = os.path.join(local_folder, filename)
            logger.info(f"Uploading: {filename}")

            try:
                gfile = drive.CreateFile({"title": filename, "parents": [{"id": drive_folder_id}]})
                gfile.SetContentFile(file_path)
                gfile.Upload()
                
                logger.info(f"Uploaded: {filename}")

                gfile = None
                os.remove(file_path)
                logger.info(f"Deleted: {filename} from local storage")
                logger.info("All images uploaded and deleted successfully.")

            except Exception as e:
                logger.error(f"Error uploading {filename}: {e}")


def main():
    logger = init_logger()
    try:
        drive = authenticate_service_account(SERVICE_ACCOUNT_FILE, logger)
        upload_images_to_drive(drive, LOCAL_FOLDER, DRIVE_FOLDER_ID, IMAGE_EXTENSIONS, logger)
    except Exception as e:
        logger.critical(f"Critical error in main: {e}")

if __name__ == "__main__":
    main()
