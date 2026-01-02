@echo off
REM Script pour lancer l'agent de nettoyage CSV
REM Usage: nettoyer.bat mon_fichier.csv

echo ========================================
echo Agent de Nettoyage CSV avec Gemini Pro
echo ========================================
echo.

REM Verifier si un fichier est fourni
if "%~1"=="" (
    echo Erreur: Aucun fichier specifie
    echo Usage: nettoyer.bat mon_fichier.csv
    echo.
    pause
    exit /b 1
)

REM Verifier si le fichier existe
if not exist "%~1" (
    echo Erreur: Le fichier "%~1" n'existe pas
    echo.
    pause
    exit /b 1
)

REM Verifier si la cle API est definie
if "%GEMINI_API_KEY%"=="" (
    echo.
    echo ATTENTION: La cle API Gemini n'est pas configuree!
    echo.
    echo Pour configurer votre cle API:
    echo 1. Obtenez votre cle sur: https://makersuite.google.com/app/apikey
    echo 2. Executez: set GEMINI_API_KEY=votre_cle_api
    echo.
    echo Ou definissez-la maintenant:
    set /p GEMINI_API_KEY="Entrez votre cle API Gemini: "
)

REM Lancer l'agent
python csv_cleaner_agent.py "%~1"

echo.
echo ========================================
pause
