@echo off
SET GARMIN_EMAIL=aaronep@gmail.com
SET GARMIN_PASSWORD=
SET GARMIN_FILE_LOC=C:\Users\aaronep\Downloads

:: Navigate to the script directory
cd /d "C:\Users\aaronep\Documents\Dev\garmin-fit-importer"

:: Activate the virtual environment
call .venv\Scripts\activate

:: Run the import script (past 24h by default)
python import_fit.py

:: Keep window open to see results
echo.
echo Import process finished.
pause
