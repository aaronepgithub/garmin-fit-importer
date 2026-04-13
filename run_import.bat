@echo off
SET GARMIN_EMAIL=aaronep@gmail.com
SET GARMIN_PASSWORD=Felber02!
SET GARMIN_FILE_LOC=C:\Users\aaronep\Downloads

:: Navigate to the script directory
cd /d "C:\Users\aaronep\Documents\Dev\garmin-fit-importer"

:: Activate the virtual environment
call .venv\Scripts\activate

:: Download files from Dropbox first
python download_dropbox.py

:: Run the import script (past 24h by default)
python import_fit.py

:: Delete all .fit files from the download folder
del /q "C:\Users\aaronep\Downloads\*.fit"

:: Keep window open to see results
echo
echo Import process finished.
pause


