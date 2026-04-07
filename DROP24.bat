@echo off

:: Navigate to the script directory
cd /d "C:\Users\aaronep\Documents\Dev\garmin-fit-importer"

:: Activate the virtual environment
call .venv\Scripts\activate

:: Run the import script (past 24h by default)
python download_dropbox.py

:: Keep window open to see results
echo.
echo Import process finished.
echo Task ran at %date% %time% >> C:\task_test_log_dropbox.txt

pause