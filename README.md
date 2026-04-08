# SL LAB PROJECT

## What this project contains
- `src/billing.py` — Main Python script for billing (Tkinter GUI).
- `data/product.csv` — Product data.
- `data/customer.csv` — Customer data.
- `dist/` — Empty folder (where your EXE will be created).
- `build/` — Empty folder for PyInstaller build files.
- `make_exe.bat` — Windows batch script to create an executable using PyInstaller.
- `requirements.txt` — Python dependencies.

## How to run (development)
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   python src/billing.py
   ```

## How to build a Windows EXE (on Windows machine)
1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Place a copy of this folder on your Windows PC.
3. Double-click `make_exe.bat` or run it in Command Prompt. This will create an exe in the `dist/` folder.

## Notes
- The app expects `product.csv` and `customer.csv` to be in the `data/` folder. `src/billing.py` currently uses `CSV_DIR = "../data"` to load them.
