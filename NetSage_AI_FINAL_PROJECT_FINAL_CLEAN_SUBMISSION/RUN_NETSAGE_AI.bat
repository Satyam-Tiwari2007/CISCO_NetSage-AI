@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo        NetSage AI - Launch Console
echo ========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on this computer.
    echo Please install Python and try again.
    pause
    exit /b 1
)

python -m streamlit --version >nul 2>nul
if errorlevel 1 (
    echo Streamlit is not installed.
    echo Installing required packages...
    python -m pip install streamlit pandas
    if errorlevel 1 (
        echo Installation failed. Please install streamlit and pandas manually.
        pause
        exit /b 1
    )
)

echo Starting NetSage AI...
echo The browser will open at http://localhost:8501
python -m streamlit run "09_Integrated_App\netsage_app.py"

endlocal
