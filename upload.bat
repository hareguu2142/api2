@echo off
REM ========================================================
REM update_main.bat
REM Automate adding, committing, and pushing to main branch
REM ========================================================

REM Change to the directory of this script (i.e. your repo root)
cd /d %~dp0

REM Stage all changes
echo Staging all changes...
git add .

REM Prompt for a commit message
set /p COMMIT_MSG="Enter commit message (leave blank for 'Auto-update'): "
if "%COMMIT_MSG%"=="" (
    set "COMMIT_MSG=Auto-update"
)

REM Commit
echo Committing with message: "%COMMIT_MSG%"
git commit -m "%COMMIT_MSG%"

REM Push to main branch on origin
echo Pushing to origin/main...
git push origin main

REM Check for errors
if errorlevel 1 (
    echo.
    echo ERROR: Something went wrong during push.
    pause
    exit /b 1
)

echo.
echo ✅ Successfully pushed to main!
pause
