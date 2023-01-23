import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkcalendar import DateEntry
from tkinter import messagebox


# add employee
def add_employee(db):
    window = tk.Toplevel()
    window.title('Add employee')

    tk.Label(window, text='Username:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    username_var = tk.StringVar()
    ttk.Entry(window, textvariable=username_var).grid(row=1, column=0, padx=5)

    tk.Label(window, text='first name:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    fname_var = tk.StringVar()
    ttk.Entry(window, textvariable=fname_var).grid(row=1, column=1, padx=5)

    tk.Label(window, text='last name:', font=('Arial', 15)).grid(row=0, column=2, padx=5)
    lname_var = tk.StringVar()
    ttk.Entry(window, textvariable=lname_var).grid(row=1, column=2, padx=5)

    tk.Label(window, text='Address:', font=('Arial', 15)).grid(row=0, column=3, padx=5)
    address_var = tk.StringVar()
    ttk.Entry(window, textvariable=address_var).grid(row=1, column=3, padx=10)

    tk.Label(window, text='birthday: yyyy-mm-dd', font=('Arial', 15)).grid(row=2, column=0, padx=5)
    bdate_var = DateEntry(window, date_pattern='yyyy-MM-dd')
    bdate_var.grid(row=3, column=0, padx=10)

    tk.Label(window, text='taxID', font=('Arial', 15)).grid(row=2, column=1, padx=5)
    taxID_var = tk.StringVar()
    ttk.Entry(window, textvariable=taxID_var).grid(row=3, column=1, padx=5)

    tk.Label(window, text='hired: yyyy-mm-dd', font=('Arial', 15)).grid(row=2, column=2, padx=5)
    hired_var = DateEntry(window, date_pattern='yyyy-MM-dd')
    hired_var.grid(row=3, column=2, padx=5)

    tk.Label(window, text='experience (hours)', font=('Arial', 15)).grid(row=2, column=3, padx=5)
    exp_var = tk.IntVar()
    ttk.Entry(window, textvariable=exp_var).grid(row=3, column=3, padx=5)

    tk.Label(window, text='salary', font=('Arial', 15)).grid(row=4, column=0, padx=5)
    salary_var = tk.IntVar()
    ttk.Entry(window, textvariable=salary_var).grid(row=5, column=0, padx=5)

    add_employee_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    add_employee_button.grid(row=9, column=2, sticky="e", padx=10, pady=5)

    def confirm():
        username = username_var.get()
        fname = fname_var.get()
        lname = lname_var.get()
        address = address_var.get()
        bdate = bdate_var.get_date()
        taxID = taxID_var.get()
        hired = hired_var.get_date()
        exp = exp_var.get()
        salary = salary_var.get()

        required = ['username', 'fname', 'lname', 'taxID']

        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return

        cursor = db.cursor()
        cursor.execute(f"select * from users where username = '{username}';")
        if len(cursor.fetchall()) > 0:
            msg = f'User already exists'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from employees where taxID = '{taxID}';")
        if len(cursor.fetchall()) > 0:
            msg = f'New employee must has a unique tax identifier'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from pilots where username = '{username}';")
        if len(cursor.fetchall()) > 0:
            msg = f'New employee already has a designated pilot roles'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from workers where username = '{username}';")
        if len(cursor.fetchall()) > 0:
            msg = f'New employee already has a designated workers roles'
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            cursor = db.cursor()
            args = (username, fname, lname, address, bdate, taxID, hired, exp, salary)
            cursor.callproc('add_employee', args)
            db.commit()
            msg = f'{username} is added'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


''' ------------------- Chenyu Wang ----------------------- '''
# add Service
def add_service(db):
    window = tk.Toplevel()
    window.title('Add service')

    tk.Label(window, text='id:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    id_var = tk.StringVar()
    ttk.Entry(window, textvariable=id_var).grid(row=1, column=0, padx=5)

    tk.Label(window, text='long name:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    long_name_var = tk.StringVar()
    ttk.Entry(window, textvariable=long_name_var).grid(row=1, column=1, padx=5)

    tk.Label(window, text='home base:', font=('Arial', 15)).grid(row=0, column=2, padx=5)
    home_base_var = tk.StringVar()
    ttk.Entry(window, textvariable=home_base_var).grid(row=1, column=2, padx=5)

    tk.Label(window, text='manager:', font=('Arial', 15)).grid(row=0, column=3, padx=5)
    manager_var = tk.StringVar()
    ttk.Entry(window, textvariable=manager_var).grid(row=1, column=3, padx=10)


    add_service_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    add_service_button.grid(row=9, column=2, sticky="e", padx=10, pady=5)

    def confirm():
        id = id_var.get()
        long_name = long_name_var.get()
        home_base = home_base_var.get()
        manager = manager_var.get()

        required = ['id', 'long_name', 'home_base', 'manager']

        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return

        cursor = db.cursor()
        cursor.execute(f"select * from delivery_services where id = '{id}';")
        if len(cursor.fetchall()) > 0:
            msg = f'Service id already exists'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from locations where label = '{home_base}';")
        if len(cursor.fetchall()) == 0:
            msg = f'Invalid Home base'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from employees where username = '{manager}';")
        if len(cursor.fetchall()) == 0:
            msg = f'Invalid manager'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from work_for where username = '{manager}';")
        if len(cursor.fetchall()) > 0:
            msg = f'Manager already works for another service'
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            cursor = db.cursor()
            args = (id, long_name, home_base, manager)
            cursor.callproc('add_service', args)
            db.commit()
            msg = f'Service{long_name}, id: {id} is added'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)

############
# Add Owner
def add_owner(db):
    window = tk.Toplevel()
    window.title('Add owner')

    tk.Label(window, text='Username:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    username_var = tk.StringVar()
    ttk.Entry(window, textvariable=username_var).grid(row=1, column=0, padx=5)

    tk.Label(window, text='first name:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    fname_var = tk.StringVar()
    ttk.Entry(window, textvariable=fname_var).grid(row=1, column=1, padx=5)

    tk.Label(window, text='last name:', font=('Arial', 15)).grid(row=0, column=2, padx=5)
    lname_var = tk.StringVar()
    ttk.Entry(window, textvariable=lname_var).grid(row=1, column=2, padx=5)

    tk.Label(window, text='Address:', font=('Arial', 15)).grid(row=0, column=3, padx=5)
    address_var = tk.StringVar()
    ttk.Entry(window, textvariable=address_var).grid(row=1, column=3, padx=10)

    tk.Label(window, text='birthday: yyyy-mm-dd', font=('Arial', 15)).grid(row=2, column=0, padx=5)
    bdate_var = DateEntry(window, date_pattern='yyyy-MM-dd')
    bdate_var.grid(row=3, column=0, padx=10)

    add_owner_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    add_owner_button.grid(row=9, column=2, sticky="e", padx=10, pady=5)

    def confirm():
        username = username_var.get()
        fname = fname_var.get()
        lname = lname_var.get()
        address = address_var.get()
        bdate = bdate_var.get_date()

        required = ['username', 'fname', 'lname']

        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return

        cursor = db.cursor()
        cursor.execute(f"select * from users where username = '{username}';")
        if len(cursor.fetchall()) > 0:
            msg = f'Username already exists'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from restaurant_owners where username = '{username}';")
        if len(cursor.fetchall()) > 0:
            msg = f'Restaurant Owner already exists'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from employees where username = '{username}';")
        if len(cursor.fetchall()) > 0:
            msg = f'User already serves in employee role'
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            cursor = db.cursor()
            args = (username, fname, lname, address, bdate)
            cursor.callproc('add_owner', args)
            db.commit()
            msg = f'Owner {username} is added'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)

## Fire employee
def fire_employee(db):
    window = tk.Toplevel()
    window.title('Fire employee')
    window.geometry("400x300")

    tk.Label(window, text='Services', font=('Arial', 15)).pack()

    cursor = db.cursor()
    cursor.execute("select id, long_name, manager from delivery_services;")
    services = cursor.fetchall()

    var = tk.Variable(value=services)

    service_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE, exportselection=False)
    service_select.pack(expand=True, fill=tk.BOTH)

    tk.Label(window, text='Employees', font=('Arial', 15)).pack()

    employee_select = tk.Listbox(window, listvariable=[], height=6, selectmode=tk.SINGLE, exportselection=False)
    employee_select.pack(expand=True, fill=tk.BOTH)

    fire_employee_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    fire_employee_button.pack()

    def update(event):
        id = service_select.get(service_select.curselection())[0]
        cursor.execute(f"select username from work_for where id = '{id}' and "
            + "username not in (select manager from delivery_services where manager is not null) and "
            + "username not in (select flown_by from drones where flown_by is not null);")

        employees = cursor.fetchall()
        employee_select.delete(0, tk.END)
        for l in employees:
            employee_select.insert(tk.END, l)

    service_select.bind('<<ListboxSelect>>', update)

    def confirm():
        id = service_select.get(service_select.curselection())[0]
        username = employee_select.get(employee_select.curselection())[0]

        try:
            cursor = db.cursor()
            args = (username, id)
            cursor.callproc('fire_employee', args)
            db.commit()
            msg = f'Employee {username} is fired from {id}'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


def hire_employee(db):
    window = tk.Toplevel()
    window.title('Hire employee')

    tk.Label(window, text='Username:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    username_var = tk.StringVar()
    ttk.Entry(window, textvariable=username_var).grid(row=1, column=0, padx=5)

    tk.Label(window, text='ID:', font=('Arial', 15)).grid(row=0, column=1, padx=10)
    id_var = tk.StringVar()
    ttk.Entry(window, textvariable=id_var).grid(row=1, column=1, padx=5)

    hire_employee_button = tk.Button(window, text="confirm", width=20, command=lambda: confirm())
    hire_employee_button.grid(row=9, column=2, sticky="e", padx=10, pady=5)


    def confirm():
        username = username_var.get()
        id = id_var.get()

        required = ['username', 'id']

        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return

        cursor = db.cursor()
        cursor.execute(f"select * from work_for where (username, id) = ('{username}', '{id}');")
        if len(cursor.fetchall()) > 0:
            msg = f'Employee has already been hired by {id}'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from employees where username = '{username}';")
        if len(cursor.fetchall()) == 0:
            msg = f'Invalid employee'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from delivery_services where id = '{id}';")
        if len(cursor.fetchall()) == 0:
            msg = f'Invalid service'
            messagebox.showinfo(title='Warning', message=msg)
            return


        cursor.execute(f"select * from delivery_services where manager = '{username}'"
                       + f"and id <> '{id}';")
        if len(cursor.fetchall()) > 0:
            msg = f'Employee has already managing another service'
            messagebox.showinfo(title='Warning', message=msg)
            return

        cursor.execute(f"select * from drones where id <> '{id}' and flown_by = '{username}';")
        if len(cursor.fetchall()) > 0:
            msg = f'Employee is flying a drone'
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            cursor = db.cursor()
            args = (username, id)
            cursor.callproc('hire_employee', args)
            db.commit()
            msg = f'{username} hired by {id}'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)

## Start_funding
def start_funding(db, username):
    window = tk.Toplevel()
    window.title('Start Funding')
    window.geometry("400x600")

    cursor = db.cursor()

    tk.Label(window, text='Restaurants', font=("Arial", 10)).pack()

    cursor.execute("select long_name, location, funded_by from restaurants;")
    restaurants = cursor.fetchall()

    var = tk.Variable(value=restaurants)

    restaurant_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE)
    restaurant_select.pack(expand=True, fill=tk.BOTH)

    confirm_button = tk.Button(window, text="confirm", width=10, command=lambda:confirm())
    confirm_button.pack()

    def confirm():
        restaurant = restaurant_select.get(restaurant_select.curselection())
        long_name = restaurant[0]

        try:
            cursor = db.cursor()
            args = (username, long_name)
            cursor.callproc('start_funding', args)
            db.commit()
            msg = f'{username} starts funding {long_name}'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


''' -------------------Chenyu End ------------------------------- '''

