import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkcalendar import DateEntry
from tkinter import messagebox


# add ingredient
def add_ingredient(db):
    window = tk.Toplevel()
    window.title('Add ingredient')

    tk.Label(window, text='barcode:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    barcode_var = tk.StringVar()
    ttk.Entry(window, textvariable=barcode_var).grid(row=1, column=0, padx=5)

    tk.Label(window, text='iname:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    iname_var = tk.StringVar()
    ttk.Entry(window, textvariable=iname_var).grid(row=1, column=1, padx=5)

    tk.Label(window, text='weight:', font=('Arial', 15)).grid(row=0, column=2, padx=5)
    weight_var = tk.IntVar()
    ttk.Entry(window, textvariable=weight_var).grid(row=1, column=2, padx=5)

    add_ingredient_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    add_ingredient_button.grid(row=9, column=2, sticky="e", padx=10, pady=5)

    def confirm():
        barcode = barcode_var.get()
        iname = iname_var.get()
        weight = weight_var.get()

        if weight < 0:
            messagebox.showinfo(title='Warning', message="Weight must be non-negative")
            return

        required = ['barcode', 'iname']

        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return

        cursor = db.cursor()
        cursor.execute(f"select * from ingredients where barcode = '{barcode}';")
        if len(cursor.fetchall()) > 0:
            msg = f'Ingredient already exists'
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            args = (barcode, iname, weight)
            cursor.callproc('add_ingredient', args)
            db.commit()
            msg = f'{barcode} is added'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# add drone
def add_drone(db):
    window = tk.Toplevel()
    window.title('Add drone')

    tk.Label(window, text='id:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    id_var = tk.StringVar()
    ttk.Entry(window, textvariable=id_var).grid(row=1, column=0, padx=5)

    tk.Label(window, text='tag:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    tag_var = tk.IntVar()
    ttk.Entry(window, textvariable=tag_var).grid(row=1, column=1, padx=5)

    tk.Label(window, text='fuel:', font=('Arial', 15)).grid(row=0, column=2, padx=5)
    fuel_var = tk.IntVar()
    ttk.Entry(window, textvariable=fuel_var).grid(row=1, column=2, padx=5)

    tk.Label(window, text='capacity:', font=('Arial', 15)).grid(row=0, column=3, padx=10)
    capacity_var = tk.IntVar()
    ttk.Entry(window, textvariable=capacity_var).grid(row=1, column=3, padx=5)

    tk.Label(window, text='sales:', font=('Arial', 15)).grid(row=2, column=0, padx=5)
    sales_var = tk.IntVar()
    ttk.Entry(window, textvariable=sales_var).grid(row=3, column=0, padx=5)

    tk.Label(window, text='flown_by:', font=('Arial', 15)).grid(row=2, column=1, padx=5)
    flown_by_var = tk.StringVar()
    ttk.Entry(window, textvariable=flown_by_var).grid(row=3, column=1, padx=5)

    add_drone_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    add_drone_button.grid(row=9, column=2, sticky="e", padx=10, pady=5)

    def confirm():
        id = id_var.get()
        tag = tag_var.get()
        fuel = fuel_var.get()
        capacity = capacity_var.get()
        sales = sales_var.get()
        flown_by = flown_by_var.get()

        required = ['id', 'flown_by']

        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return

        if tag < 0:
            messagebox.showinfo(title='Warning', message="Tag must be non-negative")
            return

        cursor = db.cursor()
        cursor.execute(f"select * from delivery_services where id = '{id}';")
        if len(cursor.fetchall()) == 0:
            msg = f'Invalid serivce id'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from drones where (id, tag) = ('{id}', {tag});")
        if len(cursor.fetchall()) > 0:
            msg = f'Drone already exists'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from pilots natural join work_for where username = '{flown_by}' and id = '{id}';")
        if len(cursor.fetchall()) == 0:
            msg = f'Invalid pilot'
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            args = (id, tag, fuel, capacity, sales, flown_by)
            cursor.callproc('add_drone', args)
            db.commit()
            msg = f'Drone {id}-{tag} is added'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# add restaurant

def add_restaurant(db):
    window = tk.Toplevel()
    window.title('Add restaurant')

    tk.Label(window, text='long_name:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    long_name_var = tk.StringVar()
    ttk.Entry(window, textvariable=long_name_var).grid(row=1, column=0, padx=5)

    tk.Label(window, text='rating:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    rating_var = tk.IntVar()
    ttk.Entry(window, textvariable=rating_var).grid(row=1, column=1, padx=5)

    tk.Label(window, text='spent:', font=('Arial', 15)).grid(row=0, column=2, padx=5)
    spent_var = tk.IntVar()
    ttk.Entry(window, textvariable=spent_var).grid(row=1, column=2, padx=5)

    tk.Label(window, text='location:', font=('Arial', 15)).grid(row=0, column=3, padx=10)
    location_var = tk.StringVar()
    ttk.Entry(window, textvariable=location_var).grid(row=1, column=3, padx=5)

    add_restaurant_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    add_restaurant_button.grid(row=9, column=2, sticky="e", padx=10, pady=5)

    def confirm():
        long_name = long_name_var.get()
        rating = rating_var.get()
        spent = spent_var.get()
        location = location_var.get()

        required = ['long_name', 'location']

        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return

        if rating > 5 or rating < 1:
            msg = f'Range of rating is between 1~5'
            messagebox.showinfo(title='Warning', message=msg)
            return

        if spent < 0:
            msg = f'the amount of spend should be equal or greater than 0'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor = db.cursor()
        cursor.execute(f"select * from restaurants where long_name = '{long_name}';")
        if len(cursor.fetchall()) > 0:
            msg = f'Invalid long_name'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor = db.cursor()
        cursor.execute(f"select * from restaurants where location = '{location}';")
        if len(cursor.fetchall()) == 0:
            msg = f'Invalid location'
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            cursor = db.cursor()
            args = (long_name, rating, spent, location)
            cursor.callproc('add_restaurant', args)
            db.commit()
            msg = f'{long_name} is added'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# remove ingredient

def remove_ingredient(db):
    window = tk.Toplevel()
    window.title('Remove ingredient')
    window.geometry("400x300")

    tk.Label(window, text='Ingredients', font=('Arial', 15)).pack()

    cursor = db.cursor()
    cursor.execute("select barcode, iname from ingredients where barcode not in (select barcode from payload);")
    ingredients = cursor.fetchall()

    var = tk.Variable(value=ingredients)

    ingredient_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE, exportselection=False)
    ingredient_select.pack(expand=True, fill=tk.BOTH)

    remove_ingredient_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    remove_ingredient_button.pack()

    def confirm():
        selected = ingredient_select.get(ingredient_select.curselection())
        barcode = selected[0]

        try:
            cursor = db.cursor()
            args = (barcode,)
            cursor.callproc('remove_ingredient', args)
            db.commit()
            msg = f'{barcode} is removed'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# remove_drone
def remove_drone(db):
    window = tk.Toplevel()
    window.title('Remove drone')
    window.geometry("400x300")

    tk.Label(window, text='id:', font=('Arial', 15)).pack()
    cursor = db.cursor()
    cursor.execute("select id, tag from drones where (id, tag) in (select swarm_id, swarm_tag from drones) is not true "
                   + "and (id, tag) not in (select id, tag from payload);")
    drones = cursor.fetchall()

    var = tk.Variable(value=drones)

    drone_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE, exportselection=False)
    drone_select.pack(expand=True, fill=tk.BOTH)

    remove_drone_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    remove_drone_button.pack()

    def confirm():
        selected = drone_select.get(drone_select.curselection())
        id = selected[0]
        tag = selected[1]

        try:
            args = (id, tag)
            cursor.callproc('remove_drone', args)
            db.commit()
            msg = f'{id}-{tag} is removed'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# purchase_ingredient
def purchase_ingredient(db):
    window = tk.Toplevel()
    window.title('Purchase Ingredient')
    window.geometry("400x600")

    cursor = db.cursor()

    tk.Label(window, text='Restaurants', font=("Arial", 10)).pack()

    cursor.execute("select long_name, location from restaurants;")
    restaurants = cursor.fetchall()

    var = tk.Variable(value=restaurants)

    restaurant_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE, exportselection=False)
    restaurant_select.pack(expand=True, fill=tk.BOTH)

    tk.Label(window, text='Available Ingredients', font=("Arial", 10)).pack()
    payload_select = tk.Listbox(window, listvariable=[], height=6, selectmode=tk.SINGLE, exportselection=False)
    payload_select.pack(expand=True, fill=tk.BOTH)

    tk.Label(window, text='Purchase quantity', font=("Arial", 10)).pack()
    quantity_var = tk.IntVar()
    ttk.Entry(window, textvariable=quantity_var).pack()

    confirm_button = tk.Button(window, text="confirm", width=10, command=lambda: confirm())
    confirm_button.pack()

    def update(event):
        curr_location = restaurant_select.get(restaurant_select.curselection())[1]
        cursor.execute(f"select id, tag, barcode, iname, quantity, price from payload natural join ingredients " +
                       f"where (id, tag) in (select id, tag from drones where hover = '{curr_location}')")

        payloads = cursor.fetchall()
        payload_select.delete(0, tk.END)
        for l in payloads:
            payload_select.insert(tk.END, l)

    restaurant_select.bind('<<ListboxSelect>>', update)

    def confirm():
        resturant = restaurant_select.get(restaurant_select.curselection())
        long_name = resturant[0]
        payload = payload_select.get(payload_select.curselection())
        id = payload[0]
        tag = payload[1]
        barcode = payload[2]
        max_quantity = payload[4]
        quantity = quantity_var.get()

        if quantity > max_quantity:
            msg = f'Quantity cannot exceed {max_quantity}'
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            cursor = db.cursor()
            args = (long_name, id, tag, barcode, quantity)
            cursor.callproc('purchase_ingredient', args)
            db.commit()
            msg = f'{quantity} of {barcode} is purchased'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)

