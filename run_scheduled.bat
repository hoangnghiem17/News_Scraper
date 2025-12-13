@echo off
REM Batch file to run news summarizer - can be scheduled via Windows Task Scheduler
cd /d "%~dp0"
python news_summarizer.py
pause

