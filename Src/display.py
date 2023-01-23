import tkinter as tk
from tkinter import ttk


def display_user(db):
    cursor = db.cursor()
    columns = ("username", "first_name", "last_name", "address", "birthdate")
    column_names = ("username", "first name", "last name", "address", "Birthday")
    cursor.execute("select " + ",".join(map(str, columns)) + " from users;")
    show_table("User", cursor.fetchall(), columns, column_names)


def display_employee(db, id=None):
    cursor = db.cursor()
    if (id != None):
        cursor.execute(f"select * from display_employee_view where username in (select username from work_for where id = '{id}');")
    else:
        cursor.execute("select * from display_employee_view;")

    columns = ("username", "TaxID", "salary", "hired", "employee_experience", "licenseID", "piloting_experience", "manager_status")
    column_names = columns
    show_table("Employee", cursor.fetchall(), columns, column_names)


def display_pilot(db, id=None):
    cursor = db.cursor()
    if (id != None):
        cursor.execute(f"select * from display_pilot_view where username in (select username from work_for where id = '{id}');")
    else:
        cursor.execute("select * from display_pilot_view;")

    columns = ("username", "licenseID", "experience", "num_drones", "num_locations")
    column_names = ("username", "licenseID", "experience", "num drones", "num locations")
    show_table("Pilot", cursor.fetchall(), columns, column_names)


def display_drone(db, id=None):
    cursor = db.cursor()
    if (id != None):
        cursor.execute(f"select * from drones where id = '{id}';")
    else:
        cursor.execute("select * from drones;")

    columns = ("id", "tag", "fuel", "capacity", "sales", "flown_by", "swarm_id", "swarm_tag", "hover")
    column_names = columns
    show_table("Drones", cursor.fetchall(), columns, column_names)


def display_ingredient(db):
    cursor = db.cursor()
    cursor.execute("select * from ingredients;")
    columns = ("barcode", "iname", "weight")
    column_names = columns
    show_table("Ingredient", cursor.fetchall(), columns, column_names)

def display_avail_ingredient(db):
    cursor = db.cursor()
    cursor.execute("select * from display_ingredient_view;")
    columns = ("ingredient_name", "location", "amount_available", "low_price", "high_price")
    column_names = columns
    show_table("Available Ingredients", cursor.fetchall(), columns, column_names)


def display_restaurant(db, id=None):
    cursor = db.cursor()
    cursor.execute("select * from restaurants;")

    columns = ("long_name", "rating", "spent", "location", "funded_by")
    column_names = columns
    show_table("Restaurants", cursor.fetchall(), columns, column_names)


def display_location(db):
    cursor = db.cursor()
    columns = ("label", "x_coord", "y_coord", "space", "num_restaurants", "num_delivery_services", "num_drones")
    column_names = ("Label", "x coordinate", "y coordinate", "space", "number of restaurants", "number of delivery services", "number of drones")
    cols = ",".join(map(str, columns))
    cursor.execute(f"select {cols} from display_location_view natural join locations;")
    show_table("Locations", cursor.fetchall(), columns, column_names)


def display_payload(db):
    cursor = db.cursor()
    columns = ("id", "tag", "barcode", "quantity", "price")
    column_names = ("Drone ID", "Drone Tag", "Barcode", "Quantity", "Price")
    cursor.execute("select " + ",".join(map(str, columns)) + " from payload;")
    show_table("Payload", cursor.fetchall(), columns, column_names)


def display_service(db):
    cursor = db.cursor()
    columns = ("id", "long_name", "home_base", "manager", "revenue", "ingredients_carried", "cost_carried", "weight_carried")
    column_names = ("id", "long name", "home base", "manager", "revenue", "ingredients carried", "cost carried", "weight carried")
    cursor.execute("select * from display_service_view;")
    show_table("Service Stat", cursor.fetchall(), columns, column_names)


# def display_service(db):
#     cursor = db.cursor()
#     columns = ("id", "long_name", "home_base", "manager")
#     column_names = ("id", "long name", "home base", "manager")
#     cursor.execute("select * from delivery_services;")
#     show_table("Service", cursor.fetchall(), columns, column_names)


def display_owner(db):
    cursor = db.cursor()
    columns = ("username", "first_name", "last_name", "address", "num_restaurants", "num_places", "highs", "lows", "debt")
    column_names = ("username", "first name", "last name", "address", "num restaurants", "num places", "high rating", "low rating", "debt")
    cursor.execute("select * from display_owner_view;")
    show_table("Owner", cursor.fetchall(), columns, column_names)


def display_worker(db):
    cursor = db.cursor()
    columns = ("username", "first_name", "last_name", "address", "birthdate", "service_id")
    column_names = columns
    cursor.execute("select t1.username as username, first_name, last_name, address, birthdate, "
        + "group_concat(id) as service_id from "
        + "(select * from (workers natural join users)) as t1 "
        + "left outer join (select * from work_for) as t2 on t1.username = t2.username "
        + "group by t1.username;")
    show_table("Worker", cursor.fetchall(), columns, column_names)


def display_work_for(db):
    cursor = db.cursor()
    columns = ("username", "first_name", "last_name", "id", )
    column_names = columns
    cursor.execute("select username, first_name, last_name, id from work_for natural join users;")
    show_table("Work for", cursor.fetchall(), columns, column_names)


'''
    Show a table for the data in a new window
'''
def show_table(title, data, columns, column_names):
    new_window = tk.Tk()
    new_window.title(title)
    table = ttk.Treeview(new_window, columns=columns, show='headings', height=10)

    for i in range(len(columns)):
        table.column(columns[i], anchor=tk.CENTER, width=120)
        table.heading(columns[i], text=column_names[i])

    table.grid(row=0, column=0, sticky=tk.NSEW)

    # add a scrollbar
    scrollbar1 = ttk.Scrollbar(new_window, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscroll=scrollbar1.set)
    scrollbar1.grid(row=0, column=1, sticky='ns')


    for line in data:
        table.insert("", tk.END, values=line)

    exit_button = tk.Button(new_window, text="Exit", width=5, command=new_window.destroy)
    exit_button.grid(row=2, column=0, sticky='s')

    new_window.mainloop()