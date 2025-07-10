@echo off
echo Installing Python packages from requirements.txt...
pip install -r .\libs\requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Error occurred during installation.
) else (
    echo.
    echo All packages installed successfully!
)
pause
