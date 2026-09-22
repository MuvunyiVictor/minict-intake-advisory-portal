@echo off
title Push MINICT Portal to GitHub
cls
echo ====================================================================
echo   Pushing MINICT Smart Support Intake Portal to GitHub
echo   Repository: https://github.com/MuvunyiVictor/minict-intake-advisory-portal.git
echo ====================================================================
echo.
echo Make sure you have created an empty repository on GitHub named:
echo   'minict-intake-advisory-portal'
echo under your GitHub account: https://github.com/new
echo.
pause
echo.
echo Pushing commits to GitHub...
"C:\Program Files\Git\cmd\git.exe" push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Code successfully pushed to your GitHub repository!
) else (
    echo [NOTE] If repository does not exist yet, visit:
    echo        https://github.com/new
    echo        Set repository name: minict-intake-advisory-portal
    echo        Then re-run this script.
)
echo.
pause
