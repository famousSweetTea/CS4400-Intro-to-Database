import os
import tkinter as tk
from tkinter import ttk
import mysql.connector

from menu import menu

def main():
    # configure database connection HERE
    db = mysql.connector.connect(user="root",
                                  password=os.environ["DATABASE_PASSWORD"],
                                  host="127.0.0.1",
                                  database="restaurant_supply_express")
    menu(db)
    db.close()


if __name__ == "__main__":
    main()
