@echo off
::  WEAVE LAUNCHER
::  A Simple Pchtxt to IPS Converter
::  Copyright (c) 2025. All rights reserved.

setlocal enabledelayedexpansion
title WEAVE: PCHTXT TO IPS CONVERTER
mode con: cols=100 lines=30
chcp 65001 >NUL

:: Check for Python Installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [CRITICAL ERROR] Python environment not found.
    echo  Please install Python 3.8+ and add it to your system PATH.
    echo.
    pause
    exit /b 1
)

python weave-script.py %*

if %errorlevel% neq 0 (
    echo.
    echo  [!] The application exited with an error code.
    pause
)

endlocal
