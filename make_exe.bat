@echo off
REM One-click EXE builder using PyInstaller
REM Make sure you run this on a Windows machine with Python installed.

pip install pyinstaller
cd src
pyinstaller --onefile --noconsole billing.py
move dist\billing.exe ..\dist\
echo Build finished. Check the dist folder.
pause
