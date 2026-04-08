# Smart Billing & Inventory Management System

🚀 A Python-based billing and inventory system designed to handle real-world business use cases like billing, stock tracking, and GST calculation.

---

## Features
- Billing system with GST (CGST + SGST)
- Customer-based discounts
- Product inventory management
- Stock updates and shortage logging
- Invoice generation

---

## Tech Stack
- Python
- Pandas
- CSV (File Handling)
- Tkinter (GUI)

---

## Project Structure
- src/ → Main application logic  
- data/ → CSV files (customers, products)  
- sample_output/ → Example outputs  
- Documentation.pdf → Project documentation  

---

## What this project contains
- `src/billing.py` → Main Python script for billing (Tkinter GUI)
- `data/product.csv` → Product data
- `data/customer.csv` → Customer data
- `make_exe.bat` → Script to create executable using PyInstaller
- `requirements.txt` → Python dependencies

---

## How to Run (Development)

1. Install dependencies:
   pip install -r requirements.txt
2. Run the application:
   python src/billing.py
   ---
## How to Build a Windows EXE

1. Install PyInstaller:
  pip install pyinstaller
2. Run:
  make_exe.bat
3. The `.exe` file will be created inside the `dist/` folder.

---

## Notes
- The app expects `product.csv` and `customer.csv` to be inside the `data/` folder.
- The file path used in code:

CSV_DIR = "../data"


---

## Documentation
Detailed project documentation is available in the repository (`Documentation.pdf`).

---

## Learning Outcomes
- Implemented real-world billing logic using Python
- Worked with CSV for data storage and handling
- Applied GST calculation (CGST + SGST)
- Built a GUI application using Tkinter
- Designed a basic inventory management system

---

## Author
Darshan Fanse
   
