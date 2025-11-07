import tkinter as tk
from tkinter import messagebox, ttk

car_inventory = []        # Main Inventory
deleted_cars = []         # Deleted Cars List
updated_cars = []         # Updated Cars List

# ---------------- Functions ----------------
def add_car():
    name = name_entry.get()
    model = model_entry.get()
    price = price_entry.get()
    stock = stock_entry.get()

    if not name or not model or not price or not stock:
        messagebox.showerror("Error", "All fields are required!")
        return

    car = {
        "name": name,
        "model": model,
        "price": float(price),
        "stock": int(stock)
    }

    car_inventory.append(car)
    update_tables()
    clear_fields()
    messagebox.showinfo("Success", "Car added successfully!")

def delete_car():
    selected = car_table.selection()
    if not selected:
        messagebox.showerror("Error", "Select a car to delete")
        return

    index = car_table.index(selected[0])

    # Add to deleted list
    deleted_cars.append(car_inventory[index].copy())

    car_inventory.pop(index)
    update_tables()
    messagebox.showinfo("Deleted", "Car deleted successfully!")

def update_stock():
    selected = car_table.selection()
    if not selected:
        messagebox.showerror("Error", "Select a car to update")
        return

    index = car_table.index(selected[0])
    new_stock = stock_entry.get()

    if not new_stock.isdigit():
        messagebox.showerror("Error", "Enter valid stock number!")
        return

    # Store old record for update history
    old = car_inventory[index].copy()
    updated_cars.append(old)

    # Update stock
    car_inventory[index]["stock"] = int(new_stock)

    update_tables()
    messagebox.showinfo("Updated", "Stock updated successfully!")

def update_tables():
    # MAIN TABLE
    for row in car_table.get_children():
        car_table.delete(row)
    for car in car_inventory:
        car_table.insert("", "end", values=(car["name"], car["model"], car["price"], car["stock"]))

    # DELETED TABLE
    for row in deleted_table.get_children():
        deleted_table.delete(row)
    for car in deleted_cars:
        deleted_table.insert("", "end", values=(car["name"], car["model"], car["price"], car["stock"]))

    # UPDATED TABLE
    for row in updated_table.get_children():
        updated_table.delete(row)
    for car in updated_cars:
        updated_table.insert("", "end", values=(car["name"], car["model"], car["price"], car["stock"]))

def clear_fields():
    name_entry.delete(0, tk.END)
    model_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Car Inventory Management System")
root.geometry("900x700")
root.config(bg="#e8f1f8")

# ---- Title ----
title = tk.Label(root,
                 text="🚗 Car Inventory Management System",
                 font=("Arial", 20, "bold"),
                 fg="#0a3d62", bg="#e8f1f8")
title.pack(pady=15)

# ---- Input Frame ----
frame = tk.Frame(root, bg="#e8f1f8")
frame.pack(pady=10)

labels = ["Car Name:", "Model:", "Price:", "Stock:"]

for i, text in enumerate(labels):
    tk.Label(frame, text=text, font=("Arial", 11, "bold"),
             bg="#e8f1f8", fg="#0a3d62").grid(row=i, column=0, sticky="w", pady=4)

name_entry = tk.Entry(frame, width=25, font=("Arial", 11))
model_entry = tk.Entry(frame, width=25, font=("Arial", 11))
price_entry = tk.Entry(frame, width=25, font=("Arial", 11))
stock_entry = tk.Entry(frame, width=25, font=("Arial", 11))

name_entry.grid(row=0, column=1, padx=10, pady=4)
model_entry.grid(row=1, column=1, padx=10, pady=4)
price_entry.grid(row=2, column=1, padx=10, pady=4)
stock_entry.grid(row=3, column=1, padx=10, pady=4)

# ---- Buttons ----
btn_frame = tk.Frame(root, bg="#e8f1f8")
btn_frame.pack(pady=10)

button_style = {
    "width": 14,
    "font": ("Arial", 11, "bold"),
    "bd": 0,
    "relief": "flat",
    "fg": "white",
    "height": 1,
    "cursor": "hand2"
}

tk.Button(btn_frame, text="Add Car", bg="#27ae60", command=add_car, **button_style).grid(row=0, column=0, padx=8)
tk.Button(btn_frame, text="Delete Car", bg="#e74c3c", command=delete_car, **button_style).grid(row=0, column=1, padx=8)
tk.Button(btn_frame, text="Update Stock", bg="#2980b9", command=update_stock, **button_style).grid(row=0, column=2, padx=8)
tk.Button(btn_frame, text="Clear Fields", bg="#8e44ad", command=clear_fields, **button_style).grid(row=0, column=3, padx=8)


# ---------------- Main Inventory Table ----------------
tk.Label(root, text="Current Inventory", bg="#e8f1f8",
         font=("Arial", 14, "bold"), fg="#0a3d62").pack()

columns = ("Name", "Model", "Price", "Stock")
car_table = ttk.Treeview(root, columns=columns, show="headings", height=8)
for col in columns:
    car_table.heading(col, text=col)
    car_table.column(col, width=150)
car_table.pack(pady=10)


# ---------------- Deleted Cars Table ----------------
tk.Label(root, text="Deleted Cars", bg="#e8f1f8",
         font=("Arial", 14, "bold"), fg="#c0392b").pack()

deleted_table = ttk.Treeview(root, columns=columns, show="headings", height=5)
for col in columns:
    deleted_table.heading(col, text=col)
    deleted_table.column(col, width=150)
deleted_table.pack(pady=10)


# ---------------- Updated Cars Table ----------------
tk.Label(root, text="Updated Cars (Stock Changed)", bg="#e8f1f8",
         font=("Arial", 14, "bold"), fg="#8e44ad").pack()

updated_table = ttk.Treeview(root, columns=columns, show="headings", height=5)
for col in columns:
    updated_table.heading(col, text=col)
    updated_table.column(col, width=150)
updated_table.pack(pady=10)

root.mainloop()
