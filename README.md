# CS 4400 Project Phase 4 - Group 50

## Preparations

1. **Python 3.10** - Follow instructions to install python 3.10 for your platform in the [python docs](https://docs.python.org/3.10/using/)

2. **Virtual Environment** - It is recommended to work within a virtual environment whenever using Python for projects. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) 

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies we selected within the `requirements.txt` file by executing:
```
pip install -r requirements.txt
```


## Set Up the Database

1. Execute the SQL script [cs4400_database_v2 schema_and_data.sql](./cs4400_database_v2%20schema_and_data.sql) to initialize the database for testing.
2. Execute the SQL script [cs4400_phase3_stored_procedures_team90_rev.sql](./cs4400_phase3_stored_procedures_team90_rev.sql) to import the stored procedures used by the app.


## Run the App

Modify the configurations in [src/main.py](./src/main.py) to set up the connection to your MySQL database. Export the password of the database as the environment variable `DATABASE_PASSWORD` before running.

To run the app, execute:
```bash
python3 src/main.py
```

Then login with the corresponding username to conduct operations. Note that 'admin' is also a username for certain operations and all table views. Example usernames for the functionalities to be tested can be found in [login_usernames.xlsx](./login_usernames.xlsx)

## Technologies Used in the App

The app is built on python with the following two key packages

- [**Tkinter**](https://docs.python.org/3/library/tkinter.html) is the standard Python toolkit for GUI. All of the windows for database operations and views of our app are built using Tkinter.

- [**MySQL Connector/Python**](https://dev.mysql.com/doc/connector-python/en/) is the official API for Python programs to access the MySQL databases. The app uses the API to connect to the `restaurant_supply_express` database, to execute SQL commands, and to call the stored precedures.


## Teamwork

The work was distributed in our team based on functionality

- Feng, Xianle: load_drone, refuel_drone, takeover_drone, join_swarm, leave_swarm, fly_drone, main menu, views
- Li, Qian: add_ingredient, add_drone, add_restaurant, remove_ingredient, remove_drone, purchase_ingredient
- Wang, Chenyu: add_employee, add_service, hire_employee, fire_employee, add_owner, start_funding
- Wang, Yuchen: add_pilot_role, add_worker_role, remove_pilot_role, add_location, manage_service