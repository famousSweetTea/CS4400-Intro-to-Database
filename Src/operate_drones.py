import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import mysql.connector
from mysql.connector import Error

# takeover an available drone from the list
def takeover_drone(db, username):
    window = tk.Toplevel()
    window.title('Takeover Drone')
    window.geometry("400x300")

    title = tk.Label(window, text='Available drones', font=("Arial", 10))
    title.pack()

    cursor = db.cursor()
    cursor.execute(f"select id from work_for where username = '{username}';")
    service_id = cursor.fetchall()

    drones = []

    for id in service_id:
        cursor.execute(f"select id, tag, flown_by from drones where id = '{id[0]}' "
            + f"and flown_by is not null and flown_by <> '{username}';")
        drones += cursor.fetchall()

    var = tk.Variable(value=drones)

    drone_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE)
    drone_select.pack(expand=True, fill=tk.BOTH)

    confirm_button = tk.Button(window, text="confirm", width=10, command=lambda:confirm())
    confirm_button.pack()

    def confirm():
        selected = drone_select.get(drone_select.curselection())
        drone_id = selected[0]
        drone_tag = selected[1]
        try:
            args = (username, drone_id, drone_tag)
            cursor.callproc('takeover_drone', args)
            db.commit()
            msg = f'Now you are flying: {drone_id}-{drone_tag}'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# set a drone controlled by the pilot to join a swarm
def join_swarm(db, username):
    window = tk.Toplevel()
    window.title('Join swarm')
    window.geometry("400x300")
    
    cursor = db.cursor()

    tk.Label(window, text='Available drones', font=("Arial", 10)).pack()

    cursor.execute(f"select id from work_for where username = '{username}';")
    service_id = cursor.fetchall()

    drones = []

    for id in service_id:
        cursor.execute(f"select id, tag, hover from drones where id = '{id[0]}' "
            + "and flown_by is not null "
            + "and ((id, tag) in (select swarm_id, swarm_tag from drones) is not true);")
        drones += cursor.fetchall()

    var = tk.Variable(value=drones)

    drone_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE, exportselection=False)
    drone_select.pack(expand=True, fill=tk.BOTH)


    tk.Label(window, text='Available leaders', font=("Arial", 10)).pack()
    leader_select = tk.Listbox(window, listvariable=[], height=6, selectmode=tk.SINGLE, exportselection=False)
    leader_select.pack(expand=True, fill=tk.BOTH)
    
    confirm_button = tk.Button(window, text="confirm", width=10, command=lambda:confirm())
    confirm_button.pack()

    def update(event):
        curr_tag = drone_select.get(drone_select.curselection())[1]
        curr_hover = drone_select.get(drone_select.curselection())[2]
        cursor.execute(f"select id, tag, hover from drones where id = '{id[0]}'"
            + f"and flown_by is not null and tag <> {curr_tag} and hover = '{curr_hover}';")
        leaders = cursor.fetchall()
        leader_select.delete(0, tk.END)
        for l in leaders:
            leader_select.insert(tk.END, l)
    
    drone_select.bind('<<ListboxSelect>>', update)
        

    def confirm():
        drone_selected = drone_select.get(drone_select.curselection())
        drone_id = drone_selected[0]
        drone_tag = drone_selected[1]
        drone_hover = drone_selected[2]
        leader_selected = leader_select.get(leader_select.curselection())
        leader_id = leader_selected[0]
        leader_tag = leader_selected[1]
        leader_hover = leader_selected[2]

        # ensure the drone won't join the swarm of itself
        if drone_tag == leader_tag:
            msg = f'Select another drone as the leader'
            messagebox.showinfo(title='Warning', message=msg)
            return

        if drone_hover != leader_hover:
            msg = f'The drone and the leader must hover at the same location'
            messagebox.showinfo(title='Warning', message=msg)
            return
        
        try:
            args = (drone_id, drone_tag, leader_tag)
            cursor.callproc('join_swarm', args)
            db.commit()
            msg = f'Now {drone_id}-{drone_tag} is following {drone_id}-{leader_tag}'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# set a drone in the swarm being controlled by the pilot of the leader
def leave_swarm(db, username):
    window = tk.Toplevel()
    window.title('Leave swarm')
    window.geometry("400x300")

    title = tk.Label(window, text='Drones in a swarm', font=("Arial", 10))
    title.pack()

    cursor = db.cursor()
    cursor.execute(f"select id from work_for where username = '{username}';")
    service_id = cursor.fetchall()

    drones = []

    for id in service_id:
        cursor.execute(f"select id, tag, swarm_id, swarm_tag from drones where id = '{id[0]}' "
            + f"and swarm_id is not null;")
        drones += cursor.fetchall()

    var = tk.Variable(value=drones)

    drone_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE)
    drone_select.pack(expand=True, fill=tk.BOTH)

    confirm_button = tk.Button(window, text="confirm", width=10, command=lambda:confirm())
    confirm_button.pack()

    def confirm():
        selected = drone_select.get(drone_select.curselection())
        drone_id = selected[0]
        drone_tag = selected[1]
        try:
            args = (drone_id, drone_tag)
            cursor.callproc('leave_swarm', args)
            db.commit()
            cursor.execute(f"select flown_by from drones where (id, tag) = ('{drone_id}', {drone_tag});")
            pilot = cursor.fetchone()
            msg = f'{drone_id}-{drone_tag} left the swarm, now controlled by {pilot[0]}'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# fly a drone from one location to another
def fly_drone(db, username):
    window = tk.Toplevel()
    window.title('Fly drone')
    window.geometry("400x300")

    title = tk.Label(window, text='Drones controlling', font=("Arial", 10))
    title.pack()

    cursor = db.cursor()
    cursor.execute(f"select id from work_for where username = '{username}';")
    service_id = cursor.fetchall()

    cursor.execute(f"select id, tag, hover, fuel from drones where flown_by = '{username}';")

    drones = cursor.fetchall()

    drones_disp = []
    fuels = []
    count = []

    for i in drones:
        cnt = 1
        line = f"{i[0]}-{i[1]} @ {i[2]} fuel:{i[3]}, swarms: "
        min_fuel = int(i[3])
        cursor.execute(f"select id, tag, fuel from drones where (swarm_id, swarm_tag) = ('{i[0]}', {i[1]});")
        for s in cursor.fetchall():
            line += f"{s[0]}-{s[1]} fuel:{s[2]}, "
            min_fuel = min(min_fuel, int(s[2]))
            cnt += 1
        drones_disp.append(line[0:-2])
        fuels.append(min_fuel)
        count.append(cnt)

    var = tk.Variable(value=drones_disp)

    drone_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE, exportselection=False)
    drone_select.pack(expand=True, fill=tk.BOTH)

    tk.Label(window, text='Available destinations', font=("Arial", 10)).pack()
    dest_select = tk.Listbox(window, listvariable=[], height=6, selectmode=tk.SINGLE, exportselection=False)
    dest_select.pack(expand=True, fill=tk.BOTH)

    confirm_button = tk.Button(window, text="confirm", width=10, command=lambda:confirm())
    confirm_button.pack()

    def update(event):
        idx = int(drone_select.curselection()[0])
        curr_id = drones[idx][0]
        curr_tag = drones[idx][1]
        curr_hover = drones[idx][2]
        fuel = fuels[idx]
        space_req = count[idx]

        cursor.execute("select label, space from locations;")
        dest = cursor.fetchall()

        cursor.execute(f"select home_base from delivery_services where id = '{curr_id}'")
        home_base = cursor.fetchone()[0]
        fuel_est = []
        fuel_safety = []
        space_avail = []
        for d in dest:
            cursor.execute(f"select count(*) from drones where hover = '{d[0]}';")
            space_avail.append(int(d[1]) - int(cursor.fetchone()[0]))
            cursor.execute(f"select fuel_required('{curr_hover}', '{d[0]}');")
            fuel_req = cursor.fetchone()[0]
            cursor.execute(f"select fuel_required('{home_base}', '{d[0]}');")
            fuel_ret = cursor.fetchone()[0]
            fuel_est.append(int(fuel_req))
            fuel_safety.append(int(fuel_req)+int(fuel_ret))
        
        dest_select.delete(0, tk.END)
        for i in range(len(dest)):
            # rule out the locations not feasible
            if dest[i][0] == curr_hover or space_avail[i] < space_req or fuel < fuel_safety[i]:
                continue
            l = (dest[i][0], space_avail[i], f"fuel: single {fuel_est[i]}, safety {fuel_safety[i]}")
            dest_select.insert(tk.END, l)
    
    drone_select.bind('<<ListboxSelect>>', update)

    def confirm():
        idx = drone_select.curselection()[0]
        drone_selected = drones[idx]
        drone_id = drone_selected[0]
        drone_tag = drone_selected[1]
        destination = dest_select.get(dest_select.curselection())[0]

        try:
            args = (drone_id, drone_tag, destination)
            cursor.callproc('fly_drone', args)
            db.commit()
            msg = f'{drones_disp[idx]} fly to {destination}'
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)


# load a drone at the homebase with ingredients
def load_drone(db, username):
    window = tk.Toplevel()
    window.title('Load drone')
    window.geometry("400x600")

    title = tk.Label(window, text='Drones at the homebase', font=("Arial", 10))
    title.pack()

    cursor = db.cursor()
    cursor.execute(f"select id from work_for where username = '{username}'")
    service_id = cursor.fetchall()

    drones = []

    for id in service_id:
        # fetch the drones currently at the homebase
        cursor.execute(f"select id, tag, hover, capacity from drones where id = '{id[0]}' "
            + f"and hover = (select home_base from delivery_services where id = '{id[0]}');")
        drones += cursor.fetchall()
    
    updated_drones = []
    for drone in drones:
        cursor.execute(f"select sum(quantity) from payload group by id, tag having (id, tag) = ('{drone[0]}', {drone[1]});")
        occupied = cursor.fetchone()
        if occupied == None or len(occupied) == 0:
            occupied = 0
        else:
            occupied = int(occupied[0])
        capacity = int(drone[3]) - occupied
        updated_drones.append((drone[0], drone[1], drone[2], capacity))

    drones = updated_drones

    var_drones = tk.Variable(value=drones)
    drone_select = tk.Listbox(window, listvariable=var_drones, height=6, selectmode=tk.SINGLE, exportselection=False)
    drone_select.pack(expand=True, fill=tk.BOTH)

    cursor.execute("select barcode, iname, weight from ingredients;")
    ingredients = cursor.fetchall()
    var_ingredients = tk.Variable(value=ingredients)

    tk.Label(window, text='Available ingredients to load', font=("Arial", 10)).pack()
    ingredient_select = tk.Listbox(window, listvariable=var_ingredients, height=6, selectmode=tk.SINGLE, exportselection=False)
    ingredient_select.pack(expand=True, fill=tk.BOTH)

    tk.Label(window, text='Amount to load', font=("Arial", 10)).pack()
    amount_var = tk.IntVar()
    ttk.Entry(window, textvariable=amount_var).pack()

    tk.Label(window, text='Price to sell', font=("Arial", 10)).pack()
    price_var = tk.IntVar()
    ttk.Entry(window, textvariable=price_var).pack()

    confirm_button = tk.Button(window, text="confirm", width=10, command=lambda:confirm())
    confirm_button.pack()

    def confirm():
        drone = drone_select.get(drone_select.curselection())
        drone_id = drone[0]
        drone_tag = drone[1]
        capacity = int(drone[3])
        ingredient = ingredient_select.get(ingredient_select.curselection())
        barcode = ingredient[0]
        amount = amount_var.get()
        price = price_var.get()

        if price <= 0:
            msg = f"The price must be positive"
            messagebox.showinfo(title='Warning', message=msg)
            return

        if amount <= 0:
            msg = f"The amount must be positive"
            messagebox.showinfo(title='Warning', message=msg)
            return

        if amount > capacity:
            msg = f"The amount cannot exceed {capacity}"
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            args = (drone_id, drone_tag, barcode, amount, price)
            cursor.callproc('load_drone', args)
            db.commit()
            cursor.execute(f"select quantity, price from payload where (id, tag, barcode) = ('{drone_id}', {drone_tag}, '{barcode}');")
            result = cursor.fetchone()
            msg = f"Now {drone_id}-{drone_tag} holds {result[0]} bags of {barcode} with price {result[1]}"
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)



# refuel a drone at the home base
def refuel_drone(db, username):
    window = tk.Toplevel()
    window.title('Refuel drone')
    window.geometry("400x300")

    title = tk.Label(window, text='Drones at the homebase', font=("Arial", 10))
    title.pack()

    cursor = db.cursor()
    cursor.execute(f"select id from work_for where username = '{username}'")
    service_id = cursor.fetchall()

    drones = []

    for id in service_id:
        # fetch the drones currently at the homebase
        cursor.execute(f"select id, tag, hover, fuel from drones where id = '{id[0]}' "
            + f"and hover = (select home_base from delivery_services where id = '{id[0]}');")
        drones += cursor.fetchall()

    var = tk.Variable(value=drones)

    drone_select = tk.Listbox(window, listvariable=var, height=6, selectmode=tk.SINGLE)
    drone_select.pack(expand=True, fill=tk.BOTH)

    tk.Label(window, text='Amount to refuel', font=("Arial", 10)).pack()
    refuel_var = tk.IntVar()
    ttk.Entry(window, textvariable=refuel_var).pack()

    confirm_button = tk.Button(window, text="confirm", width=10, command=lambda:confirm())
    confirm_button.pack()

    def confirm():
        selected = drone_select.get(drone_select.curselection())
        drone_id = selected[0]
        drone_tag = selected[1]
        refuel = refuel_var.get()

        if refuel < 0:
            msg = f"Refuel amount cannot be negative"
            messagebox.showinfo(title='Warning', message=msg)
            return

        try:
            args = (drone_id, drone_tag, refuel)
            cursor.callproc('refuel_drone', args)
            db.commit()
            msg = f"Added {drone_id}-{drone_tag} with {refuel} units of fuel"
            messagebox.showinfo(title='Success', message=msg)
            window.destroy()
        except Error as e:
            msg = e
            messagebox.showinfo(title='Fail', message=msg)
