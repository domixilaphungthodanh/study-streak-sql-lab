@echo off
cd /d "%~dp0"
py -3.12 --version >nul 2>&1
if errorlevel 1 (
 python run_streak.py --notebook %*
) else (
 py -3.12 run_streak.py --notebook %*
)
pause



