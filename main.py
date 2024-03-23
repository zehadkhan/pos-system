import tkinter as tk
from tkinter import messagebox

def add_item():
    name = name_entry.get()
    price = price_entry.get()
    stock = stock_entry.get()

    if name and price and stock:
        try:
            price = float(price)
            stock = int(stock)
            new_item = {
                "name": name,
                "price": price,
                "stock": stock
            }
            items.append(new_item)
            messagebox.showinfo("Success", "The item has been added to the menu!")
            refresh_items_list()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid price and stock values.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def update_stock():
    item_index = items_listbox.curselection()
    if item_index:
        item_index = item_index[0]
        try:
            units = int(stock_update_entry.get())
            items[item_index]["stock"] += units
            messagebox.showinfo("Success", "Stock level updated successfully!")
            refresh_items_list()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of units.")
    else:
        messagebox.showerror("Error", "Please select an item from the list.")

def make_sale():
    item_index = items_listbox.curselection()
    if item_index:
        item_index = item_index[0]
        try:
            units = int(sale_units_entry.get())
            if items[item_index]["stock"] >= units:
                items[item_index]["stock"] -= units
                total_cost = units * items[item_index]["price"]
                messagebox.showinfo("Success", f"Sale successful! Total cost: {total_cost}")
                refresh_items_list()
            else:
                messagebox.showerror("Error", "Insufficient stock!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of units.")
    else:
        messagebox.showerror("Error", "Please select an item from the list.")

def refresh_items_list():
    items_listbox.delete(0, tk.END)
    for item in items:
        items_listbox.insert(tk.END, f"{item['name']} - Price: {item['price']}, Stock: {item['stock']}")

# Initialize tkinter
root = tk.Tk()
root.title("Inventory Management System")

# Create widgets
name_label = tk.Label(root, text="Item Name:")
name_entry = tk.Entry(root)
price_label = tk.Label(root, text="Item Price:")
price_entry = tk.Entry(root)
stock_label = tk.Label(root, text="Initial Stock Level:")
stock_entry = tk.Entry(root)
add_button = tk.Button(root, text="Add Item", command=add_item)

items_listbox = tk.Listbox(root, width=50, height=10)

stock_update_label = tk.Label(root, text="Units to Add/Subtract:")
stock_update_entry = tk.Entry(root)
update_stock_button = tk.Button(root, text="Update Stock", command=update_stock)

sale_units_label = tk.Label(root, text="Units Being Sold:")
sale_units_entry = tk.Entry(root)
make_sale_button = tk.Button(root, text="Make Sale", command=make_sale)

# Place widgets on the grid
name_label.grid(row=0, column=0, sticky="e")
name_entry.grid(row=0, column=1)
price_label.grid(row=1, column=0, sticky="e")
price_entry.grid(row=1, column=1)
stock_label.grid(row=2, column=0, sticky="e")
stock_entry.grid(row=2, column=1)
add_button.grid(row=3, columnspan=2, pady=5)

items_listbox.grid(row=4, columnspan=2, pady=10)

stock_update_label.grid(row=5, column=0, sticky="e")
stock_update_entry.grid(row=5, column=1)
update_stock_button.grid(row=6, columnspan=2, pady=5)

sale_units_label.grid(row=7, column=0, sticky="e")
sale_units_entry.grid(row=7, column=1)
make_sale_button.grid(row=8, columnspan=2, pady=5)

# Initialize items list
items = []

# Refresh items list after initialization
refresh_items_list()

# Start the tkinter event loop
root.mainloop()
