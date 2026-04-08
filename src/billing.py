import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
from scipy.optimize import minimize

# =================== Data Loading ===================
products = pd.read_csv(r'C:\Users\PRANAY SINGH\OneDrive\文档\PYTHON PROJECT\product.csv')
customers = pd.read_csv(r'C:\Users\PRANAY SINGH\OneDrive\文档\PYTHON PROJECT\customer.csv')

DISCOUNTS = {'Regular': 0.05, 'Premium': 0.10}


# =================== Helper Function ===================
def log_stock_shortage(item_name, requested, available):
    log_entry = pd.DataFrame([{
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Item': item_name,
        'RequestedQty': requested,
        'AvailableQty': available,
        'Shortage': requested - available
    }])
    try:
        existing = pd.read_csv('stock_log.csv')
        updated = pd.concat([existing, log_entry], ignore_index=True)
    except FileNotFoundError:
        updated = log_entry
    updated.to_csv('stock_log.csv', index=False)


# =================== Billing Logic ===================
def generate_bill():
    customer_id = customer_var.get()
    if not customer_id:
        messagebox.showwarning("Select Customer", "Please select a customer before billing.")
        return

    customer = customers.loc[customers['CustomerID'] == customer_id].iloc[0]
    discount_rate = DISCOUNTS.get(customer['Type'], 0)
    total_before_discount = 0
    bill_items = []

    for item_id, qty_var in item_vars.items():
        qty = qty_var.get()
        if qty <= 0:
            continue

        product = products.loc[products['ItemID'] == item_id].iloc[0]
        available = product['StockQty']
        name = product['ItemName']
        price = product['Price']

        if available == 0:
            log_stock_shortage(name, qty, 0)
            continue
        if qty > available:
            log_stock_shortage(name, qty, available)
            qty = available

        subtotal = price * qty
        total_before_discount += subtotal
        products.loc[products['ItemID'] == item_id, 'StockQty'] -= qty
        bill_items.append([name, qty, price, subtotal])

    if not bill_items:
        messagebox.showinfo("No Items", "No valid items selected.")
        return

    discount = total_before_discount * discount_rate
    taxable_amount = total_before_discount - discount
    avg_tax_rate = products.loc[products['ItemID'].isin(item_vars.keys()), 'TaxRate'].mean()
    total_tax = taxable_amount * avg_tax_rate
    cgst = sgst = total_tax / 2
    grand_total = taxable_amount + total_tax

    products.to_csv(r'C:\Users\PRANAY SINGH\OneDrive\文档\PYTHON PROJECT\product.csv', index=False)

    bill_text.delete("1.0", tk.END)
    bill_text.insert(tk.END, f"🧾  SMART BILLING SYSTEM\n")
    bill_text.insert(tk.END, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    bill_text.insert(tk.END, f"Customer: {customer['Name']} ({customer['Type']})\n\n")
    bill_text.insert(tk.END, f"{'Item':20} {'Qty':>5} {'Price':>10} {'Subtotal':>10}\n")
    bill_text.insert(tk.END, "-" * 55 + "\n")

    for name, qty, price, subtotal in bill_items:
        bill_text.insert(tk.END, f"{name:20} {qty:>5} {price:>10.2f} {subtotal:>10.2f}\n")

    bill_text.insert(tk.END, "-" * 55 + "\n")
    bill_text.insert(tk.END, f"Total Before Discount : ₹{total_before_discount:.2f}\n")
    bill_text.insert(tk.END, f"Discount ({discount_rate*100:.0f}%)     : -₹{discount:.2f}\n")
    bill_text.insert(tk.END, f"Taxable Amount         : ₹{taxable_amount:.2f}\n")
    bill_text.insert(tk.END, f"CGST: ₹{cgst:.2f}   SGST: ₹{sgst:.2f}\n")
    bill_text.insert(tk.END, f"Grand Total: ₹{grand_total:.2f}\n\n")
    bill_text.insert(tk.END, "✅ Transaction completed successfully.\n")


# =================== UI SETUP ===================
root = tk.Tk()
root.title("💼 Smart Billing System")
root.geometry("1100x700")
root.configure(bg="#f3f6fa")

# --- Header ---
header = tk.Frame(root, bg="#283593", height=60)
header.pack(fill="x")
tk.Label(header, text="Smart Billing System", bg="#283593", fg="white",
         font=("Segoe UI", 20, "bold")).pack(pady=10)

# --- Main Layout ---
main_frame = tk.Frame(root, bg="#f3f6fa")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

left_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
left_frame.place(x=10, y=10, width=450, height=640)

right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
right_frame.place(x=480, y=10, width=600, height=640)

# --- Customer Section ---
tk.Label(left_frame, text="🧍 Customer Details", font=("Segoe UI", 13, "bold"),
         bg="white", fg="#1a237e").pack(pady=10)

frame_customer = tk.Frame(left_frame, bg="white")
frame_customer.pack(pady=5)

tk.Label(frame_customer, text="Select Customer ID:", bg="white",
         font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5)

customer_var = tk.StringVar()
customer_menu = ttk.Combobox(frame_customer, textvariable=customer_var,
                             values=list(customers['CustomerID']),
                             state='readonly', width=25)
customer_menu.grid(row=0, column=1, padx=5, pady=5)

# --- Product Entry Section ---
tk.Label(left_frame, text="🛒 Product Selection", font=("Segoe UI", 13, "bold"),
         bg="white", fg="#1a237e").pack(pady=10)

product_frame = tk.Frame(left_frame, bg="white")
product_frame.pack(pady=5, fill="both", expand=True)

canvas = tk.Canvas(product_frame, bg="white", highlightthickness=0)
scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

item_vars = {}
for idx, row in enumerate(products.itertuples(), start=1):
    frame_row = tk.Frame(scrollable_frame, bg="white")
    frame_row.pack(fill="x", pady=3, padx=10)
    tk.Label(frame_row, text=f"{row.ItemName}", bg="white",
             font=("Segoe UI", 10)).pack(side="left", padx=5)
    tk.Label(frame_row, text=f"₹{row.Price}", bg="white",
             font=("Segoe UI", 10, "bold"), fg="#2e7d32").pack(side="left", padx=5)
    qty_var = tk.IntVar(value=0)
    tk.Entry(frame_row, textvariable=qty_var, width=8,
             font=("Segoe UI", 10)).pack(side="right", padx=5)
    item_vars[row.ItemID] = qty_var

# --- Generate Bill Button ---
tk.Button(left_frame, text="🧾 Generate Bill", command=generate_bill,
          bg="#4CAF50", fg="white", font=("Segoe UI", 12, "bold"),
          relief="flat", height=2, width=25).pack(pady=10)

# --- Right Frame (Invoice Output) ---
tk.Label(right_frame, text="🧾 Invoice Summary", font=("Segoe UI", 13, "bold"),
         bg="white", fg="#1a237e").pack(pady=10)

bill_text = tk.Text(right_frame, wrap="word", font=("Consolas", 10), bg="#fafafa",
                    bd=2, relief="solid", height=30)
bill_text.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
