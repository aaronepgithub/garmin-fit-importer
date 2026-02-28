import argparse
import os
import sys
import logging
import glob
import time
from getpass import getpass
from garminconnect import Garmin

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

SESSION_DIR = os.path.expanduser("~/.garmin_session")

def login(email, password):
    """Log in to Garmin Connect with session persistence."""
    client = Garmin(email, password)
    
    try:
        if os.path.exists(SESSION_DIR):
            logger.info(f"Attempting to resume session from {SESSION_DIR}...")
            client.login(SESSION_DIR)
        else:
            logger.info(f"Logging in to Garmin Connect as {email}...")
            client.login()
            # Save session for next time
            os.makedirs(SESSION_DIR, exist_ok=True)
            client.garth.dump(SESSION_DIR)
            logger.info(f"Session saved to {SESSION_DIR}")
        return client
    except Exception as e:
        logger.error(f"Login failed: {e}")
        # If resume fails, try fresh login
        if os.path.exists(SESSION_DIR):
            logger.info("Retrying with fresh login...")
            try:
                client = Garmin(email, password)
                client.login()
                client.garth.dump(SESSION_DIR)
                return client
            except Exception as e2:
                logger.error(f"Fresh login also failed: {e2}")
        sys.exit(1)

def upload_file(client, file_path):
    """Upload a single activity file."""
    try:
        logger.info(f"Uploading {os.path.basename(file_path)}...")
        client.upload_activity(file_path)
        logger.info(f"Successfully uploaded: {file_path}")
        return True
    except Exception as e:
        # Check if it's already uploaded (common error)
        if "409" in str(e) or "Conflict" in str(e):
            logger.warning(f"File already exists on Garmin Connect: {file_path}")
        else:
            logger.error(f"Failed to upload {file_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Import FIT files (e.g., from MyWhoosh) to Garmin Connect.")
    parser.add_argument("path", nargs="?", help="Path to a FIT file or a directory containing FIT files (optional if GARMIN_FILE_LOC is set)")
    parser.add_argument("--email", help="Garmin Connect email")
    parser.add_argument("--all", action="store_true", help="Upload all files in directory even if GARMIN_FILE_LOC is used (ignore 24h filter)")
    
    args = parser.parse_args()

    # Get credentials
    email = args.email or os.environ.get("GARMIN_EMAIL")
    if not email:
        email = input("Garmin Connect Email: ")

    password = os.environ.get("GARMIN_PASSWORD")
    if not password:
        password = getpass("Garmin Connect Password: ")

    # Determine path (from arg or env)
    input_path = args.path or os.environ.get("GARMIN_FILE_LOC")
    if not input_path:
        logger.error("No path provided and GARMIN_FILE_LOC environment variable is not set.")
        parser.print_help()
        sys.exit(1)

    # Initialize client
    client = login(email, password)

    # Determine files to upload
    files = []
    if os.path.isdir(input_path):
        all_fit_files = glob.glob(os.path.join(input_path, "*.fit"))
        
        # If we're using the automated GARMIN_FILE_LOC, only take files from the past 24 hours
        # unless --all is specified
        if not args.path and os.environ.get("GARMIN_FILE_LOC") and not args.all:
            current_time = time.time()
            one_day_ago = current_time - (24 * 3600)
            files = [f for f in all_fit_files if os.path.getmtime(f) > one_day_ago]
            logger.info(f"Scanning {input_path} for recent .fit files (past 24h)...")
            if not files:
                logger.info("No .fit files found from the past 24 hours.")
                return
        else:
            files = all_fit_files
            
        if not files:
            logger.warning(f"No .fit files found in directory: {input_path}")
            return
        logger.info(f"Found {len(files)} .fit files to upload in {input_path}")
    else:
        files = [input_path]

    # Upload files
    success_count = 0
    for file_path in files:
        if upload_file(client, file_path):
            success_count += 1
    
    logger.info(f"Process complete. Uploaded {success_count}/{len(files)} files.")

if __name__ == "__main__":
    main()
