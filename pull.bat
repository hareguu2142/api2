@echo off
setlocal

REM URL of the Git repository
title Pull or Clone api2 Repository
set "REPO_URL=https://github.com/hareguu2142/api2.git"
set "REPO_DIR=api2"

if not exist "%REPO_DIR%\.git" (
    echo Repository not found in "%CD%\%REPO_DIR%".
    echo Cloning repository...
    git clone "%REPO_URL%" "%REPO_DIR%"
    if errorlevel 1 (
        echo Error: Failed to clone repository.
        pause
        exit /b 1
    )
) else (
    echo Repository found. Pulling latest changes...
    pushd "%REPO_DIR%"
    git pull origin main
    if errorlevel 1 (
        echo Error: Failed to pull changes.
        popd
        pause
        exit /b 1
    )
    popd
)

echo Update complete.
pause
endlocal
