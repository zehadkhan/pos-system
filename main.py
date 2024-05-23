import tkinter as tk
from tkinter import messagebox
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class InventoryManagementSystem:
    def __init__(self, master):
        self.name_label = None
        self.master = master
        master.title("Inventory Management System")
        self.create_widgets()

        # Initialize database connection
        self.conn = sqlite3.connect("data.db")
        self.create_table()

        # Refresh items list after initialization
        self.refresh_items_list()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        stock INTEGER NOT NULL)''')
        self.conn.commit()

    def create_widgets(self):
        self.name_label = tk.Label(self.master, text="Item Name:")
        self.name_entry = tk.Entry(self.master)
        self.price_label = tk.Label(self.master, text="Item Price:")
        self.price_entry = tk.Entry(self.master)
        self.stock_label = tk.Label(self.master, text="Initial Stock Level:")
        self.stock_entry = tk.Entry(self.master)
        self.add_button = tk.Button(self.master, text="Add Item", command=self.add_item)

        self.items_listbox = tk.Listbox(self.master, width=50, height=10)

        self.stock_update_label = tk.Label(self.master, text="Units to Add/Subtract:")
        self.stock_update_entry = tk.Entry(self.master)
        self.update_stock_button = tk.Button(self.master, text="Update Stock", command=self.update_stock)

        self.sale_units_label = tk.Label(self.master, text="Units Being Sold:")
        self.sale_units_entry = tk.Entry(self.master)
        self.make_sale_button = tk.Button(self.master, text="Make Sale", command=self.make_sale)

        # Place widgets on the grid
        self.name_label.grid(row=0, column=0, sticky="e")
        self.name_entry.grid(row=0, column=1)
        self.price_label.grid(row=1, column=0, sticky="e")
        self.price_entry.grid(row=1, column=1)
        self.stock_label.grid(row=2, column=0, sticky="e")
        self.stock_entry.grid(row=2, column=1)
        self.add_button.grid(row=3, columnspan=2, pady=5)

        self.items_listbox.grid(row=4, columnspan=2, pady=10)

        self.stock_update_label.grid(row=5, column=0, sticky="e")
        self.stock_update_entry.grid(row=5, column=1)
        self.update_stock_button.grid(row=6, columnspan=2, pady=5)

        self.sale_units_label.grid(row=7, column=0, sticky="e")
        self.sale_units_entry.grid(row=7, column=1)
        self.make_sale_button.grid(row=8, columnspan=2, pady=5)

    def add_item(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()

        if name and price and stock:
            try:
                price = float(price)
                stock = int(stock)
                self.save_item_to_db(name, price, stock)
                messagebox.showinfo("Success", "The item has been added to the menu!")
                self.refresh_items_list()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid price and stock values.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def update_stock(self):
        item_index = self.items_listbox.curselection()
        if item_index:
            item_index = item_index[0]
            try:
                units = int(self.stock_update_entry.get())
                cursor = self.conn.cursor()
                cursor.execute("UPDATE items SET stock = stock + ? WHERE id = ?", (units, item_index + 1))
                self.conn.commit()
                messagebox.showinfo("Success", "Stock level updated successfully!")
                self.refresh_items_list()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of units.")
        else:
            messagebox.showerror("Error", "Please select an item from the list.")

    def make_sale(self):
        item_index = self.items_listbox.curselection()
        if item_index:
            item_index = item_index[0]
            try:
                units = int(self.sale_units_entry.get())
                cursor = self.conn.cursor()
                cursor.execute("SELECT stock, price, name FROM items WHERE id = ?", (item_index + 1,))
                row = cursor.fetchone()
                if row[0] >= units:
                    cursor.execute("UPDATE items SET stock = stock - ? WHERE id = ?", (units, item_index + 1))
                    self.conn.commit()
                    total_cost = units * row[1]
                    messagebox.showinfo("Success", f"Sale successful! Total cost: {total_cost}")
                    self.refresh_items_list()

                    # Create invoice PDF
                    self.create_invoice(units, total_cost, row[2])
                else:
                    messagebox.showerror("Error", "Insufficient stock!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of units.")
        else:
            messagebox.showerror("Error", "Please select an item from the list.")

    def refresh_items_list(self):
        self.items_listbox.delete(0, tk.END)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM items")
        for row in cursor.fetchall():
            self.items_listbox.insert(tk.END, f"{row[1]} - Price: {row[2]}, Stock: {row[3]}")

    def save_item_to_db(self, name, price, stock):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO items (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        self.conn.commit()

    def create_invoice(self, units, total_cost, item_name):
        try:
            pdf_name = "invoice.pdf"
            c = canvas.Canvas(pdf_name, pagesize=letter)
            c.drawString(100, 750, "Item: " + item_name)
            c.drawString(100, 730, "Units Sold: " + str(units))
            c.drawString(100, 710, "Total Cost: $" + str(total_cost))
            c.save()
            messagebox.showinfo("Success", f"Invoice created successfully! Filename: {pdf_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create invoice: {e}")

# Initialize tkinter
root = tk.Tk()
app = InventoryManagementSystem(root)

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program terminated by user.")
