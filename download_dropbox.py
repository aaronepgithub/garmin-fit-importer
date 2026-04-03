import dropbox
import os
import logging

# Configuration
DROPBOX_REFRESH_TOKEN = "unOzPc0Ee3EAAAAAAAAAASvQlKA3vO_kcFSJzDHc6V4_l-0NbxunKwheFSjGxMmM"
DROPBOX_APP_KEY = "sis75c3mvg7zvr2"
DROPBOX_SECRET = "h1rmysh8h856sc6"
DROPBOX_FOLDER = "/Apps/WahooFitness"
DROPBOX_FILE_LOC = r"C:\Users\aaronep\Downloads"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def download_dropbox_files():
    # Ensure local directory exists
    if not os.path.exists(DROPBOX_FILE_LOC):
        logger.info(f"Creating local directory: {DROPBOX_FILE_LOC}")
        os.makedirs(DROPBOX_FILE_LOC, exist_ok=True)

    # Initialize Dropbox client
    try:
        dbx = dropbox.Dropbox(
            oauth2_refresh_token=DROPBOX_REFRESH_TOKEN,
            app_key=DROPBOX_APP_KEY,
            app_secret=DROPBOX_SECRET
        )
        logger.info("Successfully connected to Dropbox.")
    except Exception as e:
        logger.error(f"Failed to initialize Dropbox client: {e}")
        return

    # List files in the folder
    try:
        logger.info(f"Listing files in Dropbox folder: {DROPBOX_FOLDER}")
        res = dbx.files_list_folder(DROPBOX_FOLDER)
        
        while True:
            for entry in res.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    local_path = os.path.join(DROPBOX_FILE_LOC, entry.name)
                    logger.info(f"Downloading {entry.name} to {local_path}...")
                    
                    try:
                        # Overwrite if file exists
                        dbx.files_download_to_file(local_path, entry.path_display)
                    except Exception as e:
                        logger.error(f"Failed to download {entry.name}: {e}")
                
            # Check if there are more files
            if res.has_more:
                res = dbx.files_list_folder_continue(res.cursor)
            else:
                break
                
        logger.info("Finished downloading all files.")
        
    except dropbox.exceptions.ApiError as e:
        logger.error(f"Dropbox API Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    download_dropbox_files()
