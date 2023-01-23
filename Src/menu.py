import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error

from display import *
from operate_drones import *
from Qian import *
from Yuchen1212 import *
from Chenyu44 import *

class menu:

    def __init__(self, db):
        self.db = db
        self.login()

    '''
        Login window
    '''

    def login(self):

        global login_window
        login_window = tk.Tk()
        login_window.title("Restaurant Supply Express! Drone Delivery")
        login_window.geometry("400x220")
        login_window.resizable(False, False)

        frame = tk.Frame(login_window)
        frame.place(relx=0.5, rely=0.5, anchor="c")

        tk.Label(frame, text='User Login', font=("Arial", 20)).grid(row=0, column=0, columnspan=10)

        # username entry
        tk.Label(frame, text='Username:', font=('Arial', 15)).grid(row=1, column=0, padx=10)
        username_var = tk.StringVar()
        tk.Entry(frame, textvariable=username_var).grid(row=1, column=1, padx=5)

        # password entry
        tk.Label(frame, text='Password:', font=('Arial', 15)).grid(row=2, column=0, padx=10)
        password_var = tk.StringVar()
        tk.Entry(frame, textvariable=password_var, show='*').grid(row=2, column=1, padx=5)

        # login button
        tk.Button(frame, text='login', font=('Arial'), width=10, command=lambda: login()).grid(row=3, column=0,
                                                                                               columnspan=10)

        # registration
        tk.Label(frame, text='Not signed up?', font=('Arial', 10)).grid(row=4, column=0, columnspan=5)
        tk.Button(frame, text='Register', font=('Arial', 10), command=lambda: register()).grid(row=5, column=0,
                                                                                               columnspan=5)

        def login():
            username = username_var.get()
            password = password_var.get()
            cursor = self.db.cursor()
            if username == 'admin':
                self.menu_admin()
                login_window.withdraw()
                return

            try:
                cursor.execute("select first_name from users where username = '" + username + "';")
            except Error as e:
                messagebox.showinfo(title='Error', message=e)

            first_name = cursor.fetchall()
            if len(first_name) == 1:
                messagebox.showinfo(title='Login Success', message="Welcome back, " + first_name[0][0])
                login_window.withdraw()
                self.menu_main(username)
            else:
                messagebox.showinfo(title='Login Failed', message="User not found")

        def register():
            reg = tk.Toplevel()
            reg.title("User Registration")
            reg.geometry("720x300")

            tk.Label(reg, text='Register', font=("Arial", 20)).grid(row=0, column=0, columnspan=20)

            tk.Label(reg, text='Username', font=('Arial', 15)).grid(row=1, column=0, padx=10)
            username_var = tk.StringVar()
            tk.Entry(reg, textvariable=username_var).grid(row=1, column=1, padx=5)

            tk.Label(reg, text='First Name', font=('Arial', 15)).grid(row=2, column=0, padx=10)
            fname_var = tk.StringVar()
            tk.Entry(reg, textvariable=fname_var).grid(row=2, column=1, padx=5)

            tk.Label(reg, text='Last Name', font=('Arial', 15)).grid(row=3, column=0, padx=10)
            lname_var = tk.StringVar()
            tk.Entry(reg, textvariable=lname_var).grid(row=3, column=1, padx=5)

            tk.Label(reg, text='Address', font=('Arial', 15)).grid(row=4, column=0, padx=10)
            addr_var = tk.StringVar()
            tk.Entry(reg, textvariable=addr_var).grid(row=4, column=1, padx=5)

            tk.Label(reg, text='Birthday', font=('Arial', 15)).grid(row=5, column=0, padx=10)
            date = DateEntry(reg, date_pattern='yyyy-MM-dd')
            date.grid(row=5, column=1, padx=10)

        login_window.mainloop()

    '''
        Main Menu
    '''

    def menu_main(self, username):
        self.username = username
        window = tk.Tk()
        window.title("Main Menu")
        window.geometry("400x300")

        tk.Label(window, text='Main Menu', font=("Arial", 20)).grid(row=0, column=0, columnspan=10)

        row = 1
        col = 0
        cursor = self.db.cursor()

        # determine manager role
        cursor.execute("select id from delivery_services where manager = '" + username + "';")
        service_id = cursor.fetchall()
        if len(service_id) > 0:
            manager_button = tk.Button(window, text="Manager Home", width=20,
                                       command=lambda: self.menu_manager(service_id[0][0]))
            manager_button.grid(row=row, column=col, sticky="s", padx=10, pady=5)
            row += 1

        # determine pilot role
        cursor.execute("select * from pilots where username = '" + username + "';")
        if len(cursor.fetchall()) > 0:
            pilot_button = tk.Button(window, text="Pilot Home", width=20, command=lambda: self.menu_pilot(username))
            pilot_button.grid(row=row, column=col, sticky="s", padx=10, pady=5)
            row += 1

        # determine worker role
        cursor.execute("select * from workers where username = '" + username + "';")
        if len(cursor.fetchall()) > 0:
            worker_button = tk.Button(window, text="Worker Home", width=20, command=lambda: self.menu_worker(username))
            worker_button.grid(row=row, column=col, sticky="s", padx=10, pady=5)
            row += 1

        # determine owner role
        cursor.execute("select * from restaurant_owners where username = '" + username + "';")
        if len(cursor.fetchall()) > 0:
            owner_button = tk.Button(window, text="Owner Home", width=20, command=lambda: self.menu_owner(username))
            owner_button.grid(row=row, column=col, sticky="s", padx=10, pady=5)
            row += 1

        logout_button = tk.Button(window, text="Logout", width=10, command=lambda: logout())
        logout_button.grid(row=row + 2, columnspan=20)

        def logout():
            window.destroy()
            login_window.deiconify()

    '''
        Admin Menu
    '''

    def menu_admin(self):
        window = tk.Toplevel()
        window.title("Administrator Home")
        window.geometry("720x400")

        tk.Label(window, text='Administrator Home', font=("Arial", 20)).grid(row=0, column=0, columnspan=10)

        add_service_button = tk.Button(window, text="Add Service", width=20, command=lambda: add_service(self.db))
        add_service_button.grid(row=2, column=0, sticky="e", padx=10, pady=5)

        add_owner_button = tk.Button(window, text="Add Owner", width=20, command=lambda: add_owner(self.db))
        add_owner_button.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        add_location_button = tk.Button(window, text="Add Location", width=20, command=lambda: add_location(self.db))
        add_location_button.grid(row=2, column=2, sticky="e", padx=10, pady=5)

        manage_service_button = tk.Button(window, text="Manage Service", width=20, command=lambda: manage_service(self.db))
        manage_service_button.grid(row=2, column=3, sticky="e", padx=10, pady=5)

        purchase_ingredient_button = tk.Button(window, text="Purchase Ingredient", width=20, command=lambda: purchase_ingredient(self.db))
        purchase_ingredient_button.grid(row=3, column=0, sticky="e", padx=10, pady=5)

        display_user_button = tk.Button(window, text="User", width=20, command=lambda:display_user(self.db))
        display_user_button.grid(row=4, column=0, sticky="s", padx=10, pady=5)

        display_employee_button = tk.Button(window, text="Employee", width=20, command=lambda:display_employee(self.db))
        display_employee_button.grid(row=4, column=1, sticky="s", padx=10, pady=5)

        display_pilot_button = tk.Button(window, text="Pilot", width=20, command=lambda:display_pilot(self.db))
        display_pilot_button.grid(row=4, column=2, sticky="s", padx=10, pady=5)

        display_worker_button = tk.Button(window, text="Worker", width=20, command=lambda:display_worker(self.db))
        display_worker_button.grid(row=4, column=3, sticky="s", padx=10, pady=5)

        display_location_button = tk.Button(window, text="Location", width=20, command=lambda:display_location(self.db))
        display_location_button.grid(row=5, column=0, sticky="s", padx=10, pady=5)

        display_service_button = tk.Button(window, text="Service", width=20, command=lambda: display_service(self.db))
        display_service_button.grid(row=5, column=1, sticky="e", padx=10, pady=5)

        display_drone_button = tk.Button(window, text="Drone", width=20, command=lambda: display_drone(self.db))
        display_drone_button.grid(row=5, column=2, sticky="e", padx=10, pady=5)

        display_payload_button = tk.Button(window, text="Payloads", width=20, command=lambda:display_payload(self.db))
        display_payload_button.grid(row=5, column=3, sticky="s", padx=10, pady=5)

        display_owner_button = tk.Button(window, text="Owner", width=20, command=lambda: display_owner(self.db))
        display_owner_button.grid(row=6, column=0, sticky="e", padx=10, pady=5)

        display_restaurant_button = tk.Button(window, text="Restaurant", width=20, command=lambda: display_restaurant(self.db))
        display_restaurant_button.grid(row=6, column=1, sticky="e", padx=10, pady=5)

        display_ingredient_button = tk.Button(window, text="Ingredient", width=20, command=lambda: display_ingredient(self.db))
        display_ingredient_button.grid(row=6, column=2, sticky="e", padx=10, pady=5)


        display_avail_ingredient_button = tk.Button(window, text="Available Ingredient", width=20, command=lambda: display_avail_ingredient(self.db))
        display_avail_ingredient_button.grid(row=6, column=3, sticky="e", padx=10, pady=5)

        display_work_for_button = tk.Button(window, text="Work for", width=20, command=lambda: display_work_for(self.db))
        display_work_for_button.grid(row=7, column=1, sticky="e", padx=10, pady=5)

        logout_button = tk.Button(window, text="Logout", width=20, command=lambda: logout())
        logout_button.grid(row=8, columnspan=20)

        def logout():
            window.destroy()
            login_window.deiconify()

    '''
        Manager Menu
    '''

    def menu_manager(self, id):
        window = tk.Toplevel()
        window.title("Manager Home")
        window.geometry("720x300")

        cursor = self.db.cursor()
        cursor.execute("select long_name from delivery_services where id = '" + id + "';")
        long_name = cursor.fetchone()[0]
        tk.Label(window, text=long_name + ' - Manager Home', font=("Arial", 20)).grid(row=0, column=0, columnspan=10)

        display_employee_button = tk.Button(window, text="Employees", width=20, command=lambda: display_employee(self.db))
        display_employee_button.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        display_ingredient_button = tk.Button(window, text="Ingredient", width=20, command=lambda: display_ingredient(self.db))
        display_ingredient_button.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        display_restaurant_button = tk.Button(window, text="Restaurant", width=20, command=lambda: display_restaurant(self.db))
        display_restaurant_button.grid(row=1, column=2, sticky="e", padx=10, pady=5)

        display_drone_button = tk.Button(window, text="Drone", width=20, command=lambda: display_drone(self.db))
        display_drone_button.grid(row=1, column=3, sticky="e", padx=10, pady=5)

        add_employee_button = tk.Button(window, text="Add Employee", width=20, command=lambda: add_employee(self.db))
        add_employee_button.grid(row=2, column=0, sticky="e", padx=10, pady=5)

        hire_employee_button = tk.Button(window, text="Hire Employee", width=20, command=lambda: hire_employee(self.db))
        hire_employee_button.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        fire_employee_button = tk.Button(window, text="Fire Employee", width=20, command=lambda: fire_employee(self.db))
        fire_employee_button.grid(row=2, column=2, sticky="e", padx=10, pady=5)

        add_pilot_role_button = tk.Button(window, text="Add Pilot Role", width=20, command=lambda: add_pilot_role(self.db))
        add_pilot_role_button.grid(row=3, column=0, sticky="e", padx=10, pady=5)

        add_worker_role_button = tk.Button(window, text="Add Worker Role", width=20, command=lambda: add_worker_role(self.db))
        add_worker_role_button.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        remove_pilot_role_button = tk.Button(window, text="Remove Pilot Role", width=20, command=lambda: remove_pilot_role(self.db))
        remove_pilot_role_button.grid(row=3, column=2, sticky="e", padx=10, pady=5)

######

        add_ingredient_button = tk.Button(window, text="Add Ingredient", width=20, command=lambda: add_ingredient(self.db))
        add_ingredient_button.grid(row=4, column=0, sticky="e", padx=10, pady=5)

        add_drone_button = tk.Button(window, text="Add Drone", width=20, command=lambda: add_drone(self.db))
        add_drone_button.grid(row=4, column=1, sticky="e", padx=10, pady=5)

        add_restaurant_button = tk.Button(window, text="Add Restaurant", width=20, command=lambda: add_restaurant(self.db))
        add_restaurant_button.grid(row=4, column=2, sticky="e", padx=10, pady=5)

        remove_ingredient_button = tk.Button(window, text="Remove Ingredient", width=20, command=lambda: remove_ingredient(self.db))
        remove_ingredient_button.grid(row=4, column=3, sticky="e", padx=10, pady=5)

        remove_drone_button = tk.Button(window, text="Remove Drone", width=20, command=lambda: remove_drone(self.db))
        remove_drone_button.grid(row=5, column=0, sticky="e", padx=10, pady=5)

######
        exit_button = tk.Button(window, text="Exit", width=10, command=window.destroy)
        exit_button.grid(row=8, columnspan=20, sticky="s", padx=10, pady=5)

    '''
        Pilot Menu
    '''

    def menu_pilot(self, username):
        window = tk.Toplevel()
        window.title("Pilot Home")
        window.geometry("720x300")

        tk.Label(window, text='Pilot Home', font=("Arial", 20)).grid(row=0, column=0, columnspan=10)

        display_drone_button = tk.Button(window, text="Drones", width=20, command=lambda:display_drone(self.db))
        display_drone_button.grid(row=1, column=0, sticky="s", padx=10, pady=5)

        display_location_button = tk.Button(window, text="Locations", width=20, command=lambda:display_location(self.db))
        display_location_button.grid(row=1, column=1, sticky="s", padx=10, pady=5)

        takeover_button = tk.Button(window, text="Take over drone", width=20, command=lambda:takeover_drone(self.db, username))
        takeover_button.grid(row=2, column=0, sticky="s", padx=10, pady=5)

        join_swarm_button = tk.Button(window, text="Join swarm", width=20, command=lambda:join_swarm(self.db, username))
        join_swarm_button.grid(row=2, column=1, sticky="s", padx=10, pady=5)

        leave_swarm_button = tk.Button(window, text="Leave swarm", width=20, command=lambda:leave_swarm(self.db, username))
        leave_swarm_button.grid(row=2, column=2, sticky="s", padx=10, pady=5)

        fly_drone_button = tk.Button(window, text="Fly drone", width=20, command=lambda:fly_drone(self.db, username))
        fly_drone_button.grid(row=2, column=3, sticky="s", padx=10, pady=5)

        exit_button = tk.Button(window, text="Exit", width=10, command=window.destroy)
        exit_button.grid(row=4, columnspan=20, sticky="s", padx=10, pady=5)


    '''
        Worker Menu
    '''

    def menu_worker(self, username):
        window = tk.Toplevel()
        window.title("Worker Home")
        window.geometry("720x300")

        tk.Label(window, text='Worker Home', font=("Arial", 20)).grid(row=0, column=0, columnspan=10)

        display_drone_button = tk.Button(window, text="Drones", width=20, command=lambda:display_drone(self.db))
        display_drone_button.grid(row=1, column=0, sticky="s", padx=10, pady=5)

        display_payload_button = tk.Button(window, text="Payloads", width=20, command=lambda:display_payload(self.db))
        display_payload_button.grid(row=1, column=1, sticky="s", padx=10, pady=5)

        load_drone_button = tk.Button(window, text="Load drone", width=20, command=lambda:load_drone(self.db, username))
        load_drone_button.grid(row=2, column=0, sticky="s", padx=10, pady=5)

        refuel_drone_button = tk.Button(window, text="Refuel drone", width=20, command=lambda:refuel_drone(self.db, username))
        refuel_drone_button.grid(row=2, column=1, sticky="s", padx=10, pady=5)

        exit_button = tk.Button(window, text="Exit", width=10, command=window.destroy)
        exit_button.grid(row=4, columnspan=20, sticky="s", padx=10, pady=5)


    '''
        Owner Menu
    '''

    def menu_owner(self, username):
        window = tk.Toplevel()
        window.title("Owner Home")
        window.geometry("720x300")

        tk.Label(window, text='Owner Home', font=("Arial", 20)).grid(row=0, column=0, columnspan=10)

        display_restaurant_button = tk.Button(window, text="Restaurant", width=20, command=lambda: display_restaurant(self.db))
        display_restaurant_button.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        start_funding_button = tk.Button(window, text="Start Funding", width=20, command=lambda:start_funding(self.db, username))
        start_funding_button.grid(row=2, column=0, sticky="s", padx=10, pady=5)

        exit_button = tk.Button(window, text="Exit", width=5, command=window.destroy)
        exit_button.grid(row=4, columnspan=20, sticky="s", padx=10, pady=5)


