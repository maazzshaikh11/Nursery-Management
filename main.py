# main.py
from database import create_tables, insert_default_data

create_tables()
insert_default_data()


import tkinter as tk
from common import BG_COLOR, BUTTON_COLOR, HEADER_COLOR, TEXT_COLOR
from admin import admin_dashboard, add_product, delete_product, edit_product, view_reviews
from user import view_user_history, add_review
from datetime import datetime
from database import cursor, conn



def nursery_tour():
    def play_video():
        video_window = tk.Toplevel()
        video_window.title("Nursery Tour Video")
        video_window.geometry("800x600")
        video_window.configure(bg=BG_COLOR)
        tk.Label(video_window, text="Nursery Tour Video", font=("Arial", 16),
                 bg=HEADER_COLOR, fg=TEXT_COLOR).pack(fill=tk.X)
        tk.Label(video_window, text="Video Placeholder\n[Embed your video here]", bg=BG_COLOR, fg="black",
                 font=("Arial", 14), pady=20).pack(expand=True)
        tk.Button(video_window, text="Close", command=video_window.destroy,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
    nursery_window = tk.Toplevel()
    nursery_window.title("Nursery Tour")
    nursery_window.geometry("800x600")
    nursery_window.configure(bg=BG_COLOR)
    tk.Label(nursery_window, text="Nursery Tour", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR).pack(fill=tk.X)
    frame = tk.Frame(nursery_window, bg=BG_COLOR)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    cards = [
        ("Welcome to Our Nursery", "Experience a lush, green environment where plants thrive."),
        ("Our Greenhouse", "State-of-the-art greenhouse facilities to nurture delicate plants.")
    ]
    for title, content in cards:
        card = tk.Frame(frame, bg="white", bd=2, relief="raised")
        card.pack(fill=tk.X, pady=10, padx=10)
        tk.Label(card, text=title, font=("Arial", 14, "bold"), bg="white", fg=TEXT_COLOR).pack(anchor="w", padx=10, pady=5)
        tk.Label(card, text=content, font=("Arial", 12), bg="white", fg="black", wraplength=700, justify="left").pack(anchor="w", padx=10, pady=5)
    video_card = tk.Frame(frame, bg="white", bd=2, relief="raised")
    video_card.pack(fill=tk.X, pady=10, padx=10)
    tk.Label(video_card, text="Explore Our Nursery", font=("Arial", 14, "bold"),
             bg="white", fg=TEXT_COLOR).pack(anchor="w", padx=10, pady=5)
    tk.Label(video_card, text="Watch a video tour of our nursery to explore all the beautiful plants and facilities!",
             font=("Arial", 12), bg="white", fg="black", wraplength=700, justify="left").pack(anchor="w", padx=10, pady=5)
    tk.Button(video_card, text="Play Video", command=play_video,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)

def view_products(username, role):
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    product_window = tk.Toplevel()
    product_window.title("Available Products")
    product_window.geometry("800x600")
    product_window.configure(bg=BG_COLOR)
    tk.Label(product_window, text="Available Products", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(product_window, bg=BG_COLOR)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    for i, product in enumerate(products):
        product_frame = tk.Frame(frame, bg="#ffffff", borderwidth=2, relief="groove", padx=10, pady=10)
        product_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
        tk.Label(product_frame, text=product[1], font=("Arial", 14), bg="#ffffff").pack()
        tk.Label(product_frame, text=f"{product[2]}", font=("Arial", 10), bg="#ffffff", wraplength=150).pack()
        tk.Label(product_frame, text=f"Price: ₹{product[3]:.2f}", font=("Arial", 12), bg="#ffffff").pack()
        tk.Label(product_frame, text=f"Stock: {product[4]}", font=("Arial", 12), bg="#ffffff").pack()
        # For simplicity, we only include an "Order Now" button here.
        tk.Button(product_frame, text="Order Now", bg=BUTTON_COLOR, fg=TEXT_COLOR,
                  command=lambda p=product: order_product(p), font=("Arial", 12), width=10).pack(pady=5)
    for col in range(3):
        frame.columnconfigure(col, weight=1)

def place_order():
    def submit_order():
        product_id = entry_product_id.get()
        quantity = int(entry_quantity.get())
        cursor.execute("SELECT price, stock FROM Products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        price, stock = product
        if quantity > stock:
            messagebox.showerror("Error", "Insufficient stock!")
            return
        total_price = price * quantity
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO Orders (product_id, quantity, total_price, date) VALUES (?, ?, ?, ?)",
                       (product_id, quantity, total_price, date))
        cursor.execute("UPDATE Products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
        conn.commit()
        messagebox.showinfo("Success", f"Order placed successfully! Total: ₹{total_price:.2f}")
        order_window.destroy()
    order_window = tk.Toplevel()
    order_window.title("Place Order")
    order_window.geometry("400x200")
    order_window.configure(bg=BG_COLOR)
    tk.Label(order_window, text="Place an Order", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(order_window, bg=BG_COLOR)
    frame.pack(pady=10)
    tk.Label(frame, text="Product ID:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_product_id = tk.Entry(frame)
    entry_product_id.grid(row=0, column=1, pady=5)
    tk.Label(frame, text="Quantity:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_quantity = tk.Entry(frame)
    entry_quantity.grid(row=1, column=1, pady=5)
    tk.Button(order_window, text="Submit", command=submit_order,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)

############################################################
#                LOGIN / REGISTRATION FUNCTIONS          #
############################################################

def show_register():
    from database import cursor, conn  # in case not imported yet
    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.geometry("300x250")
    register_window.configure(bg=BG_COLOR)
    tk.Label(register_window, text="Register", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(register_window, bg=BG_COLOR)
    frame.pack(pady=20)
    tk.Label(frame, text="Username:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_reg_username = tk.Entry(frame)
    entry_reg_username.grid(row=0, column=1, pady=5)
    tk.Label(frame, text="Password:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_reg_password = tk.Entry(frame, show="*")
    entry_reg_password.grid(row=1, column=1, pady=5)
    tk.Label(frame, text="Confirm Password:", bg=BG_COLOR).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_reg_confirm = tk.Entry(frame, show="*")
    entry_reg_confirm.grid(row=2, column=1, pady=5)
    def submit_registration():
        username = entry_reg_username.get()
        password = entry_reg_password.get()
        confirm = entry_reg_confirm.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        try:
            cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", (username, password, "User"))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            register_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", "Username already exists!")
    tk.Button(register_window, text="Register", command=submit_registration,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
    tk.Button(register_window, text="Back", command=register_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=5)

def show_admin_login():
    login_window = tk.Tk()
    login_window.title("Admin Login")
    login_window.geometry("300x250")
    login_window.configure(bg=BG_COLOR)
    tk.Label(login_window, text="Admin Login", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(login_window, bg=BG_COLOR)
    frame.pack(pady=20)
    tk.Label(frame, text="Username:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_username = tk.Entry(frame)
    entry_username.grid(row=0, column=1, pady=5)
    tk.Label(frame, text="Password:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_password = tk.Entry(frame, show="*")
    entry_password.grid(row=1, column=1, pady=5)
    def authenticate():
        username = entry_username.get()
        password = entry_password.get()
        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            if user[3] != "Admin":
                messagebox.showerror("Error", "This account is not an Admin!")
                return
            login_window.destroy()
            show_main_window("Admin", username)
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    tk.Button(login_window, text="Login", command=authenticate,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
    tk.Button(login_window, text="Back", command=lambda: [login_window.destroy(), show_welcome()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=5)
    login_window.mainloop()

def show_user_login():
    login_window = tk.Tk()
    login_window.title("User Login")
    login_window.geometry("300x300")
    login_window.configure(bg=BG_COLOR)
    tk.Label(login_window, text="User Login", font=("Arial", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(login_window, bg=BG_COLOR)
    frame.pack(pady=10)
    tk.Label(frame, text="Username:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_username = tk.Entry(frame)
    entry_username.grid(row=0, column=1, pady=5)
    tk.Label(frame, text="Password:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_password = tk.Entry(frame, show="*")
    entry_password.grid(row=1, column=1, pady=5)
    def authenticate():
        username = entry_username.get()
        password = entry_password.get()
        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            if user[3] != "User":
                messagebox.showerror("Error", "This account is not a User account!")
                return
            login_window.destroy()
            show_main_window("User", username)
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    tk.Button(login_window, text="Login", command=authenticate,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=10)
    tk.Button(login_window, text="Register", command=show_register,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=5)
    tk.Button(login_window, text="Back", command=lambda: [login_window.destroy(), show_welcome()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=10).pack(pady=5)
    login_window.mainloop()

############################################################
#                   MAIN WINDOW (POST-LOGIN)               #
############################################################

def show_main_window(role, username):
    main_window = tk.Tk()
    main_window.title("Nursery Management System")
    main_window.geometry("800x600")
    main_window.configure(bg=BG_COLOR)
    
    tk.Label(main_window, text=f"Nursery Management System - {role}", font=("Arial", 20),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)
    
    button_frame = tk.Frame(main_window, bg=BG_COLOR)
    button_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
    
    # Common buttons for both roles (note the comma after "Plantation Guide")
    menu_buttons = [
        ("View Products", lambda: view_products(username, role)),
        ("Place Order", place_order),
        ("Nursery Tour", nursery_tour),
        ("Plantation Guide", plantation),  # Comma is important here!
        ("Order History", lambda: view_user_history(username))
    ]
    
    # If regular User, include "Add Review"; if Admin, include "View Reviews"
    if role == "User":
        menu_buttons.insert(2, ("Add Review", add_review))
    elif role == "Admin":
        menu_buttons.insert(2, ("View Reviews", view_reviews))
    
    for i, (text, command) in enumerate(menu_buttons):
        r = i // 3
        c = i % 3
        btn = tk.Button(button_frame, text=text, command=command, font=("Arial", 14),
                        bg=BUTTON_COLOR, fg=TEXT_COLOR, width=20, height=3)
        btn.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
    
    for col in range(3):
        button_frame.columnconfigure(col, weight=1)
    for row in range(2):  # 2 rows in a 2x3 grid
        button_frame.rowconfigure(row, weight=1)
    
    # If Admin, add extra admin controls in a 2x2 grid
    if role == "Admin":
        admin_frame = tk.Frame(main_window, bg=BG_COLOR)
        admin_frame.pack(pady=10)
        admin_buttons = [
            ("Dashboard", admin_dashboard),
            ("Add Product", add_product),
            ("Delete Product", delete_product),
            ("Edit Product", edit_product)
        ]
        for i, (text, command) in enumerate(admin_buttons):
            r = i // 2
            c = i % 2
            btn = tk.Button(admin_frame, text=text, command=command, font=("Arial", 14),
                            bg=BUTTON_COLOR, fg=TEXT_COLOR, width=20, height=3)
            btn.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        for col in range(2):
            admin_frame.columnconfigure(col, weight=1)
        for row in range(2):
            admin_frame.rowconfigure(row, weight=1)
    
    main_window.mainloop()

############################################################
#                    WELCOME SCREEN                        #
############################################################

def show_welcome():
    welcome_window = tk.Tk()
    welcome_window.title("Welcome")
    welcome_window.geometry("300x200")
    welcome_window.configure(bg=BG_COLOR)
    
    tk.Label(welcome_window, text="Welcome", font=("Arial", 18),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)
    
    tk.Button(welcome_window, text="Admin", command=lambda: [welcome_window.destroy(), show_admin_login()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR, width=15, height=2).pack(pady=10)
    tk.Button(welcome_window, text="User", command=lambda: [welcome_window.destroy(), show_user_login()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR, width=15, height=2).pack(pady=10)
    
    welcome_window.mainloop()

############################################################
#                       START APPLICATION                  #
############################################################

show_welcome()
