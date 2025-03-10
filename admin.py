# admin.py
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from database import cursor, conn
from common import BG_COLOR, BUTTON_COLOR, HEADER_COLOR, TEXT_COLOR

def admin_dashboard():
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Admin Dashboard")
    dashboard_window.geometry("800x600")
    dashboard_window.configure(bg=BG_COLOR)
    
    tk.Label(dashboard_window, text="Admin Dashboard", font=("Arial", 20),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)
    
    total_orders = cursor.execute("SELECT COUNT(*) FROM Orders").fetchone()[0]
    total_withdrawal = cursor.execute("SELECT SUM(total_price) FROM Orders").fetchone()[0] or 0.0
    summary_frame = tk.Frame(dashboard_window, bg=BG_COLOR)
    summary_frame.pack(pady=10)
    tk.Label(summary_frame, text=f"Total Orders: {total_orders}", font=("Arial", 14),
             bg=BG_COLOR).grid(row=0, column=0, padx=20)
    tk.Label(summary_frame, text=f"Total Withdrawal Amount: ₹{total_withdrawal:.2f}", font=("Arial", 14),
             bg=BG_COLOR).grid(row=0, column=1, padx=20)
    
    tree_frame = tk.Frame(dashboard_window)
    tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    columns = ("order_id", "product", "quantity", "total_price", "date", "status")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.heading("order_id", text="Order ID")
    tree.column("order_id", anchor="center", width=80)
    tree.heading("product", text="Product")
    tree.column("product", anchor="center", width=120)
    tree.heading("quantity", text="Quantity")
    tree.column("quantity", anchor="center", width=80)
    tree.heading("total_price", text="Total Price")
    tree.column("total_price", anchor="center", width=100)
    tree.heading("date", text="Date")
    tree.column("date", anchor="center", width=150)
    tree.heading("status", text="Status")
    tree.column("status", anchor="center", width=100)
    tree.pack(fill=tk.BOTH, expand=True)
    
    cursor.execute("""
    SELECT o.id, p.name, o.quantity, o.total_price, o.date 
    FROM Orders o 
    JOIN Products p ON o.product_id = p.id
    """)
    orders = cursor.fetchall()
    for order in orders:
        tree.insert("", tk.END, values=(order[0], order[1], order[2],
                                         f"₹{order[3]:.2f}", order[4], "Completed"))
    
    tk.Button(dashboard_window, text="Back", command=dashboard_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
    
# In admin.py, add this function:
def view_reviews():
    cursor.execute("""
    SELECT r.username, r.review_text, r.rating, p.name 
    FROM Reviews r 
    JOIN Products p ON r.product_id = p.id
    """)
    reviews = cursor.fetchall()
    reviews_window = tk.Toplevel()
    reviews_window.title("Customer Reviews")
    reviews_window.geometry("600x400")
    reviews_window.configure(bg=BG_COLOR)
    tk.Label(reviews_window, text="Customer Reviews", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(reviews_window, bg=BG_COLOR)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    for review in reviews:
        review_frame = tk.Frame(frame, bg="#ffffff", borderwidth=2, relief="groove", padx=10, pady=10)
        review_frame.pack(pady=5, fill=tk.X)
        tk.Label(review_frame, text=f"Product: {review[3]}", font=("Arial", 12), bg="#ffffff").pack(anchor="w")
        tk.Label(review_frame, text=f"User: {review[0]}", font=("Arial", 10), bg="#ffffff").pack(anchor="w")
        tk.Label(review_frame, text=f"Rating: {review[2]}/5", font=("Arial", 10), bg="#ffffff").pack(anchor="w")
        tk.Label(review_frame, text=f"Review: {review[1]}", font=("Arial", 10), bg="#ffffff", wraplength=500).pack(anchor="w")


def add_product():
    add_window = tk.Toplevel()
    add_window.title("Add New Product")
    add_window.geometry("400x300")
    add_window.configure(bg=BG_COLOR)
    tk.Label(add_window, text="Add New Product", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(add_window, bg=BG_COLOR)
    frame.pack(pady=10)
    tk.Label(frame, text="Name:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_name = tk.Entry(frame)
    entry_name.grid(row=0, column=1, pady=5)
    tk.Label(frame, text="Description:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_description = tk.Entry(frame)
    entry_description.grid(row=1, column=1, pady=5)
    tk.Label(frame, text="Price:", bg=BG_COLOR).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_price = tk.Entry(frame)
    entry_price.grid(row=2, column=1, pady=5)
    tk.Label(frame, text="Stock:", bg=BG_COLOR).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_stock = tk.Entry(frame)
    entry_stock.grid(row=3, column=1, pady=5)
    def submit_product():
        name = entry_name.get()
        description = entry_description.get()
        try:
            price = float(entry_price.get())
            stock = int(entry_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock!")
            return
        if not name:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        cursor.execute("INSERT INTO Products (name, description, price, stock) VALUES (?, ?, ?, ?)",
                       (name, description, price, stock))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        add_window.destroy()
    tk.Button(add_window, text="Add Product", command=submit_product,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
    tk.Button(add_window, text="Back", command=add_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=5)

def delete_product():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Product")
    delete_window.geometry("300x200")
    delete_window.configure(bg=BG_COLOR)
    tk.Label(delete_window, text="Delete Product", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(delete_window, bg=BG_COLOR)
    frame.pack(pady=20)
    tk.Label(frame, text="Product ID:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_id = tk.Entry(frame)
    entry_id.grid(row=0, column=1, pady=5)
    def submit_delete():
        product_id = entry_id.get()
        cursor.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        cursor.execute("DELETE FROM Products WHERE id = ?", (product_id,))
        conn.commit()
        messagebox.showinfo("Success", "Product deleted successfully!")
        delete_window.destroy()
    tk.Button(delete_window, text="Delete Product", command=submit_delete,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
    tk.Button(delete_window, text="Back", command=delete_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=5)

def edit_product():
    edit_window = tk.Toplevel()
    edit_window.title("Edit Product")
    edit_window.geometry("400x400")
    edit_window.configure(bg=BG_COLOR)
    tk.Label(edit_window, text="Edit Product", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame_id = tk.Frame(edit_window, bg=BG_COLOR)
    frame_id.pack(pady=10)
    tk.Label(frame_id, text="Product ID:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_id = tk.Entry(frame_id)
    entry_id.grid(row=0, column=1, pady=5)
    def load_product():
        product_id = entry_id.get()
        cursor.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        frame_edit = tk.Frame(edit_window, bg=BG_COLOR)
        frame_edit.pack(pady=10)
        tk.Label(frame_edit, text="Name:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        entry_name = tk.Entry(frame_edit)
        entry_name.grid(row=0, column=1, pady=5)
        entry_name.insert(0, product[1])
        tk.Label(frame_edit, text="Description:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        entry_description = tk.Entry(frame_edit)
        entry_description.grid(row=1, column=1, pady=5)
        entry_description.insert(0, product[2])
        tk.Label(frame_edit, text="Price:", bg=BG_COLOR).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        entry_price = tk.Entry(frame_edit)
        entry_price.grid(row=2, column=1, pady=5)
        entry_price.insert(0, product[3])
        tk.Label(frame_edit, text="Stock:", bg=BG_COLOR).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        entry_stock = tk.Entry(frame_edit)
        entry_stock.grid(row=3, column=1, pady=5)
        entry_stock.insert(0, product[4])
        def update_product():
            new_name = entry_name.get()
            new_description = entry_description.get()
            try:
                new_price = float(entry_price.get())
                new_stock = int(entry_stock.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid price or stock!")
                return
            cursor.execute("UPDATE Products SET name = ?, description = ?, price = ?, stock = ? WHERE id = ?",
                           (new_name, new_description, new_price, new_stock, product_id))
            conn.commit()
            messagebox.showinfo("Success", "Product updated successfully!")
            edit_window.destroy()
        tk.Button(edit_window, text="Update Product", command=update_product,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
    tk.Button(edit_window, text="Load Product", command=load_product,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=5)
    tk.Button(edit_window, text="Back", command=edit_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=5)
