@echo off
title MINICT Smart Support Intake & Directed Advisory Portal
cls
echo ==============================================================================
echo   REPUBLIC OF RWANDA - MINISTRY OF ICT AND INNOVATION (MINICT)
echo   Smart Support Intake, Directed Concept Vetting ^& Automated Advisory Portal
echo ==============================================================================
echo.
echo Starting local prototype server at http://localhost:8080 ...
echo Browser will automatically launch shortly.
echo.
echo To stop the server, press Ctrl+C or close this window.
echo ==============================================================================
echo.
py serve.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying python.exe ...
    python serve.py
)
pause
