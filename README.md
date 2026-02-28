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
   $env:GARMIN_EMAIL = "aaronep@gmail.com"
   $env:GARMIN_PASSWORD = ""
   $env:GARMIN_FILE_LOC = "C:\Users\aaronep\Downloads"
   ```

### Command Line Usage
#### Upload a single file
```bash
python import_fit.py path/to/activity.fit
```

#### Upload all FIT files in a directory
```bash
python import_fit.py path/to/mywhoosh/exports/
```

#### Automated Import (New!)
If you have set the `GARMIN_FILE_LOC` environment variable, you can simply run:
```bash
python import_fit.py
```
This will automatically scan your `GARMIN_FILE_LOC` and upload any `.fit` files modified in the **past 24 hours**. To upload all files in that directory regardless of time, use:
```bash
python import_fit.py --all
```

### Streamlit Web App Usage
Run the interactive web application:
```bash
streamlit run app.py
```
This will open a browser window where you can enter your credentials and drag-and-drop your FIT files.

### Session Persistence
The script saves your session in `~/.garmin_session` to avoid frequent logins and MFA prompts. If the login fails, it will attempt a fresh login and refresh the session.
