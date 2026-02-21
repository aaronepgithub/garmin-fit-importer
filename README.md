# Garmin Connect FIT Importer

A simple Python script to upload `.fit` files (e.g., from MyWhoosh) to Garmin Connect.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Set your credentials as environment variables to avoid prompts:
   ```bash
   # Windows (PowerShell)
   $env:GARMIN_EMAIL = "your-email@example.com"
   $env:GARMIN_PASSWORD = "your-password"
   ```

## Usage

### Upload a single file
```bash
python import_fit.py path/to/activity.fit
```

### Upload all FIT files in a directory
```bash
python import_fit.py path/to/mywhoosh/exports/
```

### Session Persistence
The script saves your session in `~/.garmin_session` to avoid frequent logins and MFA prompts. If the login fails, it will attempt a fresh login and refresh the session.
