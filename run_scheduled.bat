@echo off
REM Batch file with logging for Task Scheduler
REM Logs all output to a file for debugging

REM Change to script directory
cd /d "%~dp0"

REM Log start time
echo ========================================== >> task_scheduler.log
echo Task started: %date% %time% >> task_scheduler.log
echo ========================================== >> task_scheduler.log

REM Run the script and capture all output
python news_summarizer.py >> task_scheduler.log 2>&1

REM Log completion time
echo. >> task_scheduler.log
echo Task completed: %date% %time% >> task_scheduler.log
echo ========================================== >> task_scheduler.log
echo. >> task_scheduler.log

REM Exit with Python's exit code
exit /b %ERRORLEVEL%

