@echo off
setlocal enabledelayedexpansion

if not exist ".\lang_models\lang_models.txt" (
    echo File lang_models.txt is not found!
    pause
    exit /b 1
)

for /f "usebackq delims=" %%m in (".\lang_models\lang_models.txt") do (
    echo Pulling model: %%m
    ollama pull %%m
)

echo Ready!
pause