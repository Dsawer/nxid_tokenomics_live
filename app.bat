@echo off
chcp 65001 >nul
echo NXID Enhanced Tokenomics - Unicode  Desktop EXE Builder
echo ==============================================================

echo Checking Python packages...
python -c "import tkinter; print('OK: tkinter')" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: tkinter not found
    pause
    exit /b 1
)

python -c "import streamlit; print('OK: streamlit')" 2>nul
if %errorlevel% neq 0 (
    echo Installing streamlit...
    pip install streamlit
)

python -c "import requests; print('OK: requests')" 2>nul
if %errorlevel% neq 0 (
    echo Installing requests...
    pip install requests
)

echo.
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec
echo Cleanup completed

echo.
echo Building NXID Desktop Application (Unicode Fixed)...
echo This may take 3-5 minutes...

pyinstaller ^
    --onefile ^
    --windowed ^
    --name=NXID_Enhanced_Tokenomics ^
    --add-data="main.py;." ^
    --add-data="config.py;." ^
    --add-data="models.py;." ^
    --add-data="visualizations.py;." ^
    --add-data="sidebar.py;." ^
    --add-data="analytics.py;." ^
    --add-data="utils.py;." ^
    --add-data="*.json;." ^
    --add-data="requirements.txt;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=streamlit ^
    --hidden-import=streamlit.web.cli ^
    --hidden-import=pandas ^
    --hidden-import=numpy ^
    --hidden-import=plotly ^
    --hidden-import=plotly.graph_objects ^
    --hidden-import=plotly.express ^
    --hidden-import=requests ^
    --hidden-import=webbrowser ^
    --hidden-import=threading ^
    --hidden-import=subprocess ^
    --hidden-import=locale ^
    --hidden-import=codecs ^
    --collect-submodules=streamlit ^
    --collect-data=streamlit ^
    --noconfirm ^
    --clean ^
    tkinter_desktop.py

if %errorlevel% equ 0 (
    echo.
    echo BUILD SUCCESSFUL!
    echo ==============================================================
    echo EXE File: dist\NXID_Enhanced_Tokenomics.exe
    
    REM Get file size
    for %%A in (dist\NXID_Enhanced_Tokenomics.exe) do (
        set size=%%~zA
        set /a sizeMB=!size! / 1048576
    )
    
    echo File Size: ~%sizeMB%MB
    echo.
    echo How to use:
    echo    1. Double-click: NXID_Enhanced_Tokenomics.exe
    echo    2. Click "Uygulamayi Baslat"
    echo    3. App opens in browser automatically
    echo    4. Use the tokenomics application
    echo    5. Click "Durdur" to stop
    echo.
    
    REM Copy to desktop for easy access
    echo Creating desktop shortcut...
    copy "dist\NXID_Enhanced_Tokenomics.exe" "%USERPROFILE%\Desktop\NXID_Tokenomics.exe" >nul 2>&1
    if %errorlevel% equ 0 (
        echo Desktop shortcut created: NXID_Tokenomics.exe
    ) else (
        echo Could not create desktop shortcut
    )
    
    echo.
    echo Creating distribution README...
    echo # NXID Enhanced Tokenomics Desktop Application > dist\README.txt
    echo. >> dist\README.txt
    echo ## How to Use: >> dist\README.txt
    echo 1. Double-click NXID_Enhanced_Tokenomics.exe >> dist\README.txt
    echo 2. Click "Uygulamayi Baslat" button >> dist\README.txt
    echo 3. Application will open in your browser automatically >> dist\README.txt
    echo 4. Configure parameters in left sidebar >> dist\README.txt
    echo 5. Select scenario (Bear/Base/Bull) >> dist\README.txt
    echo 6. Click "Enhanced NXID Tokenomics Launch" >> dist\README.txt
    echo 7. Analyze results >> dist\README.txt
    echo. >> dist\README.txt
    echo ## Features: >> dist\README.txt
    echo • Simple Interest Presale System >> dist\README.txt
    echo • Advanced Maturity Damping >> dist\README.txt
    echo • Dynamic Staking with Price Velocity >> dist\README.txt
    echo • Real Circulating Supply Calculations >> dist\README.txt
    echo • 16-Quarter Scenario Analysis >> dist\README.txt
    echo • Enhanced Visualizations >> dist\README.txt
    echo. >> dist\README.txt
    echo ## System Requirements: >> dist\README.txt
    echo • Windows 7/8/10/11 >> dist\README.txt
    echo • 4GB RAM minimum (8GB recommended) >> dist\README.txt
    echo • Modern web browser (Chrome, Firefox, Edge) >> dist\README.txt
    echo • No additional software installation required >> dist\README.txt
    echo. >> dist\README.txt
    echo Version: Enhanced 6.0 Desktop (Unicode Fixed) >> dist\README.txt
    echo README.txt created in dist folder
    
    echo.
    set /p choice="Test the desktop application now? (y/n): "
    if /i "!choice!"=="y" (
        echo.
        echo Starting NXID Enhanced Tokenomics Desktop...
        start "" "dist\NXID_Enhanced_Tokenomics.exe"
        echo Application launched!
        echo Check your screen for the desktop window
    )
    
    echo.
    echo BUILD COMPLETED SUCCESSFULLY!
    echo Your executable is ready for distribution
    
) else (
    echo.
    echo BUILD FAILED!
    echo ==============================================================
    echo Common issues and solutions:
    echo.
    echo 1. Missing tkinter:
    echo    • Reinstall Python with "Add to PATH" and "tcl/tk" options
    echo.
    echo 2. PyInstaller not found:
    echo    • Run: pip install pyinstaller
    echo.
    echo 3. Missing files:
    echo    • Make sure all .py files are in the same folder
    echo    • Check that tkinter_desktop.py exists
    echo.
    echo 4. Permission errors:
    echo    • Run as Administrator
    echo    • Temporarily disable antivirus
    echo.
    echo 5. Import errors:
    echo    • Run: pip install streamlit pandas numpy plotly requests
    echo.
    echo Check the error messages above for specific issues
)

echo.
echo Need help? Check the error messages above or:
echo    • Make sure Python 3.7+ is installed
echo    • All required .py files are in the same folder
echo    • Run as Administrator if permission issues occur
echo.
pause