# user.py
import tkinter as tk
from tkinter import messagebox, ttk
from database import cursor
from common import BG_COLOR, BUTTON_COLOR, HEADER_COLOR, TEXT_COLOR

def view_user_history(username):
    history_window = tk.Toplevel()
    history_window.title("My Order History")
    history_window.geometry("700x400")
    history_window.configure(bg=BG_COLOR)
    
    tk.Label(history_window, text="My Order History", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    frame = tk.Frame(history_window, bg=BG_COLOR)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    columns = ("OrderID", "Product", "Quantity", "Price", "Date")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    tree.heading("OrderID", text="Order ID")
    tree.heading("Product", text="Product")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")
    tree.heading("Date", text="Date")
    
    tree.column("OrderID", anchor="center", width=80)
    tree.column("Product", anchor="center", width=150)
    tree.column("Quantity", anchor="center", width=80)
    tree.column("Price", anchor="center", width=100)
    tree.column("Date", anchor="center", width=150)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    cursor.execute("""
        SELECT o.id, p.name, o.quantity, o.total_price, o.date
        FROM Orders o
        JOIN Products p ON o.product_id = p.id
        WHERE o.username=?
        ORDER BY o.date DESC
    """, (username,))
    
    orders = cursor.fetchall()
    for od in orders:
        tree.insert("", tk.END, values=(od[0], od[1], od[2], f"₹{od[3]:.2f}", od[4]))

def add_review():
    def submit_review():
        product_id = entry_product_id.get()
        username = entry_username.get()
        review_text = text_review.get("1.0", "end-1c")
        rating = entry_rating.get()
        cursor.execute("INSERT INTO Reviews (product_id, username, review_text, rating) VALUES (?, ?, ?, ?)",
                       (product_id, username, review_text, rating))
        conn.commit()
        messagebox.showinfo("Success", "Review added successfully!")
        review_window.destroy()

    review_window = tk.Toplevel()
    review_window.title("Add Review")
    review_window.geometry("400x300")
    review_window.configure(bg=BG_COLOR)
    
    tk.Label(review_window, text="Add a Review", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    frame = tk.Frame(review_window, bg=BG_COLOR)
    frame.pack(pady=10)
    
    tk.Label(frame, text="Product ID:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_product_id = tk.Entry(frame)
    entry_product_id.grid(row=0, column=1, pady=5)
    
    tk.Label(frame, text="Username:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_username = tk.Entry(frame)
    entry_username.grid(row=1, column=1, pady=5)
    
    tk.Label(frame, text="Review:", bg=BG_COLOR).grid(row=2, column=0, sticky="nw", padx=10, pady=5)
    text_review = tk.Text(frame, height=5, width=30)
    text_review.grid(row=2, column=1, pady=5)
    
    tk.Label(frame, text="Rating (1-5):", bg=BG_COLOR).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_rating = tk.Entry(frame)
    entry_rating.grid(row=3, column=1, pady=5)
    
    tk.Button(review_window, text="Submit", command=submit_review,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
