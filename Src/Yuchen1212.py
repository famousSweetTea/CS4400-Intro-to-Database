import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

import mysql.connector
from mysql.connector import Error


def add_pilot_role(db):
    window = tk.Toplevel()
    window.title('Add pilot role')
    tk.Label(window, text='Username:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    username_var = tk.StringVar()
    ttk.Entry(window, textvariable=username_var).grid(row=1, column=0, padx=5)
    
    tk.Label(window, text='license ID:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    license_var = tk.StringVar()
    ttk.Entry(window, textvariable=license_var).grid(row=1, column=1, padx=5)
    
    tk.Label(window, text='experience:', font=('Arial', 15)).grid(row=0, column=2, padx=5)
    experience_var = tk.IntVar()
    ttk.Entry(window, textvariable=experience_var).grid(row=1, column=2, padx=5)
    
    add_employee_button = tk.Button(window, text="confirm", width=20, command=lambda:confirm(db))
    add_employee_button.grid(row=3, column=2, sticky="e", padx=10, pady=5)
    
    def confirm(db):
        username = username_var.get()
        licenseID = license_var.get()
        exp = experience_var.get()
        required = ['username','licenseID']
        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return
            
        cursor = db.cursor()
        cursor.execute("select username from employees where username = '"+username+"';")
        selected  = cursor.fetchall()
        if len(selected) < 1:
            messagebox.showinfo(title='Error', message="Username Does not exist")
            return
                
        cursor.execute("select username from pilots where username = '"+username+"';")
        selected  = cursor.fetchall()
        if len(selected) == 1:
            messagebox.showinfo(title='Error', message="duplicate username in pilot")
            return

        cursor.execute(f"select username from pilots where licenseID = '{licenseID}';")
        if len(cursor.fetchall()) >= 1:
            messagebox.showinfo(title='Error', message="duplicate license ID in pilot")
            return
        
        try:
            cursor = db.cursor()
            args = (username,licenseID, exp)
            cursor.callproc('add_pilot_role', args)
            db.commit()
            msg = f'{username} is added to a pilot role'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)
            


def remove_pilot_role(db):
    window = tk.Toplevel()
    window.title('Remove pilot role')
    tk.Label(window, text='Pilots not flying a drone', font=('Arial', 15)).pack()

    cursor = db.cursor()
    cursor.execute("select username from pilots where username not in (select flown_by from drones where flown_by is not null);")
    pilots = cursor.fetchall()

    var = tk.Variable(value=pilots)

    pilot_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE, exportselection=False)
    pilot_select.pack(expand=True, fill=tk.BOTH)
    
    confirm_button = tk.Button(window, text="confirm", width=20, command=lambda:confirm(db))
    confirm_button.pack()
    
    def confirm(db):
        selected = pilot_select.get(pilot_select.curselection())
        username = selected[0]
        
        try:
            cursor = db.cursor()
            cursor.execute("call remove_pilot_role('" + username+ "');")
            db.commit()
            msg = f'{username} is removed from a pilot role'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)
            
            
            
def add_worker_role(db):
    window = tk.Toplevel()
    window.title('Add worker role')
    tk.Label(window, text='Username:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    username_var = tk.StringVar()
    ttk.Entry(window, textvariable=username_var).grid(row=1, column=0, padx=5)
    
    add_employee_button = tk.Button(window, text="confirm", width=20, command=lambda:confirm(db))
    add_employee_button.grid(row=3, column=2, sticky="e", padx=10, pady=5)
    
    def confirm(db):
        username = username_var.get()
        if username == None or len(username) == 0:
            msg = f'{username} is required'
            messagebox.showinfo(title='Warning', message=msg)
            return
            
        cursor = db.cursor()
        cursor.execute("select username from employees where username = '"+username+"';")
        selected  = cursor.fetchall()
        if len(selected) < 1:
            messagebox.showinfo(title='Error', message="employee does not exist" )
            return
                
        try:
            cursor = db.cursor()
            cursor.execute("call add_worker_role('" + username+ "');")
            db.commit()
            msg = f'{username} is added from a worker role'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)
            
            
def add_location(db):
    window = tk.Toplevel()
    window.title('Add location')
    tk.Label(window, text='label:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    label_var = tk.StringVar()
    ttk.Entry(window, textvariable=label_var).grid(row=1, column=0, padx=5)
    
    tk.Label(window, text='x coord:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    x_var = tk.IntVar()
    ttk.Entry(window, textvariable=x_var).grid(row=1, column=1, padx=5)
    
    tk.Label(window, text='y coord:', font=('Arial', 15)).grid(row=0, column=2, padx=5)
    y_var = tk.IntVar()
    ttk.Entry(window, textvariable=y_var).grid(row=1, column=2, padx=5)
    
    tk.Label(window, text='space:', font=('Arial', 15)).grid(row=2, column=0, padx=5)
    space_var = tk.IntVar()
    ttk.Entry(window, textvariable=space_var).grid(row=3, column=0, padx=5)
    
    add_location_button = tk.Button(window, text="confirm", width=20, command=lambda:confirm(db))
    add_location_button.grid(row=3, column=2, sticky="e", padx=10, pady=5)
    
    def confirm(db):
        label = label_var.get()
        x = x_var.get()
        y = y_var.get()
        space = space_var.get()
        
        if label == None or len(label)==0:
            msg = f'{label} is required'
            messagebox.showinfo(title='Warning', message=msg)
            return

        if space < 0:
            msg = f'Number of space must be non-negative'
            messagebox.showinfo(title='Warning', message=msg)
            return
        
        required = ['x','y','space']
        for varname in required:
            var = locals()[varname]
            if var == None or var == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return
            
        cursor = db.cursor()
        cursor.execute("select label from locations where label = '"+label+"';")
        selected  = cursor.fetchall()
        if len(selected) >= 1:
            messagebox.showinfo(title='Error', message="Duplicate label" )
            return
        
        ##-----------x, y coord duplicate required-----------###
        cursor.execute(f"select * from locations where (x_coord, y_coord) =  ({x}, {y});")
        selected  = cursor.fetchall()
        if len(selected) >= 1:
            messagebox.showinfo(title='Error', message="Duplicate coordinates")
            return
                
        
        try:
            cursor = db.cursor()
            args = (label,x,y,space)
            cursor.callproc('add_location', args)
            db.commit()
            msg = f'{label} is added to a location'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)
            
            
            
def manage_service(db):
    window = tk.Toplevel()
    window.title('Manage Service')
    tk.Label(window, text='Username:', font=('Arial', 15)).grid(row=0, column=0, padx=10)
    username_var = tk.StringVar()
    ttk.Entry(window, textvariable=username_var).grid(row=1, column=0, padx=5)
    
    tk.Label(window, text='Service ID:', font=('Arial', 15)).grid(row=0, column=1, padx=5)
    service_var = tk.StringVar()
    ttk.Entry(window, textvariable=service_var).grid(row=1, column=1, padx=5)
    
    manage_service_button = tk.Button(window, text="confirm", width=20, command=lambda:confirm(db))
    manage_service_button.grid(row=3, column=2, sticky="e", padx=10, pady=5)
    
    def confirm(db):
        username = username_var.get()
        service = service_var.get()
        required = ['username','service']
        for varname in required:
            var = locals()[varname]
            if var == None or len(var) == 0:
                msg = f'{varname} is required'
                messagebox.showinfo(title='Warning', message=msg)
                return
            
        cursor = db.cursor()
        cursor.execute("select username from employees where username = '"+username+"';")
        selected  = cursor.fetchall()
        if len(selected) < 1:
            messagebox.showinfo(title='Error', message="Employee does not exist" )
            return
                
        cursor.execute(f"select id from delivery_services where id = '{service}';")
        selected  = cursor.fetchall()
        if len(selected) < 1:
            messagebox.showinfo(title='Error', message="Delivery service does not exist" )
            return

        cursor.execute(f"select * from work_for where (username, id) = ('{username}', '{service}');")
        selected  = cursor.fetchall()
        if len(selected) < 1:
            messagebox.showinfo(title='Error', message=f"{username} does not work for {service}" )
            return

        cursor.execute("select flown_by from drones where flown_by = '"+username+"';")
        selected  = cursor.fetchall()
        if len(selected) >= 1:
            messagebox.showinfo(title='Error', message="pilot "+username+" is flying a drone" )
            return
        
        cursor.execute("select username from work_for where id != '"+service+"' and username ='"+username+ "';")
        selected  = cursor.fetchall()
        if len(selected) >= 1:
            messagebox.showinfo(title='Error', message=username+" is working for other service" )
            return
        
        try:
            cursor = db.cursor()
            args = (username,service)
            cursor.callproc('manage_service', args)
            db.commit()
            msg = f'{username} is set to the service'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)