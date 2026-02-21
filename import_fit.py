import argparse
import os
import sys
import logging
import glob
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
    parser.add_argument("path", help="Path to a FIT file or a directory containing FIT files")
    parser.add_argument("--email", help="Garmin Connect email")
    
    args = parser.parse_args()

    # Get credentials
    email = args.email or os.environ.get("GARMIN_EMAIL")
    if not email:
        email = input("Garmin Connect Email: ")

    password = os.environ.get("GARMIN_PASSWORD")
    if not password:
        password = getpass("Garmin Connect Password: ")

    # Initialize client
    client = login(email, password)

    # Determine files to upload
    if os.path.isdir(args.path):
        files = glob.glob(os.path.join(args.path, "*.fit"))
        if not files:
            logger.warning(f"No .fit files found in directory: {args.path}")
            return
        logger.info(f"Found {len(files)} .fit files in {args.path}")
    else:
        files = [args.path]

    # Upload files
    success_count = 0
    for file_path in files:
        if upload_file(client, file_path):
            success_count += 1
    
    logger.info(f"Process complete. Uploaded {success_count}/{len(files)} files.")

if __name__ == "__main__":
    main()
