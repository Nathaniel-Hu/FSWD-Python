from flask import Flask, render_template, request, flash
import os
# note: the next line is only needed for local use, and can be commented
# out otherwise; this url will need to be updated periodically to work
# os.environ["REPLIT_DB_URL"] = "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2NTMzMDE0OTgsImlhdCI6MTY1MzE4OTg5OCwiZGF0YWJhc2VfaWQiOiJlZmQyMjRjYi1iZWZmLTRkYjQtOGYxNy0yMmMyNjJmODgyZjkifQ.TaVTiNeH-QqfkHB-iUCw8ckmHUovCpK7nvQmLVfI25D7RZqDARt6ju12eS78cdzNlKE_JdGxS3ldLOsgsOIfGQ"
from replit import db

from Backend.ItemDB import get_add_item_info, create_item, add_item, \
    string_items, get_edit_item_info, edit_item, get_delete_item_info, \
    delete_item
from Backend.ShipmentDB import get_create_shipment_info, create_shipment, \
    add_shipment, get_add_to_shipment_info, add_to_shipment, string_shipments
from Backend.BackendManagement import submit_pressed

template_dir = os.path.abspath("Frontend/Templates/")
app = Flask(__name__, template_folder=template_dir)
app.secret_key = "fswd-python"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inventory/", methods=["POST", "GET"])
def inventory():
    if request.method == "POST":
        # "Add Item to Inventory" submit button was pressed
        if submit_pressed(request.form) == "Add Item to Inventory":
            id_num, name, quantity, buy_price, sell_price = get_add_item_info(
                request.form)
            item = create_item(name, quantity, buy_price, sell_price)
            match add_item(id_num, item):
                case (True, True):
                    flash("Item already exists in the inventory, and its "
                          "quantity has been incremented successfully!")
                case (False, False):
                    flash("Unable to add item to inventory! Please check that "
                          "the item ID# is not already being used by another "
                          "item in the inventory.")
                    return render_template("inventory.html",
                                           inventory=string_items(),
                                           a_flag=True, info=request.form)
                case (True, False):
                    flash("Item added to inventory successfully!")
        # "Edit Item in Inventory" submit button was pressed
        elif submit_pressed(request.form) == "Edit Item in Inventory":
            old_id_num, id_num, name, quantity, buy_price, sell_price = \
                get_edit_item_info(request.form)
            match edit_item(old_id_num, id_num, name, quantity, buy_price,
                            sell_price):
                case (True, True):
                    flash("Changes for the item hve been made successfully!")
                case (False, True):
                    flash("No (valid) changes for item detected! Please check "
                          " that you have (valid) item changes entered, and "
                          "that the (new) item ID# is not already used in the "
                          "inventory.")
                    return render_template("inventory.html",
                                           inventory=string_items(),
                                           e_flag=True, info=request.form)
                case (False, False):
                    flash("Item does not exist in the inventory! Please check "
                          "that the old item ID# is used in the inventory.")
                    return render_template("inventory.html",
                                           inventory=string_items(),
                                           e_flag=True, info=request.form)
        # "Delete Item from Inventory" submit button was pressed (assumed)
        else:
            id_num = get_delete_item_info(request.form)
            match delete_item(id_num):
                case (True, True):
                    flash("Item deleted from the inventory successfully! Item "
                          "also deleted from all assigned shipments "
                          "successfully!")
                case (True, False):
                    flash("Item deleted from the inventory successfully!")
                case (False, False):
                    flash("Item deletion from the inventory unsuccessful! "
                          "Please check that the item ID# is being used by an "
                          "existing item in the inventory.")
                    return render_template("inventory.html",
                                           inventory=string_items(),
                                           d_flag=True, info=request.form)
    return render_template("inventory.html", inventory=string_items())


@app.route("/shipments/", methods=["POST", "GET"])
def shipments():
    if request.method == "POST":
        # "Create Shipment" submit button was pressed
        if submit_pressed(request.form) == "Create Shipment":
            id_num, name, address = get_create_shipment_info(request.form)
            item_shipment = create_shipment(name, address)
            match add_shipment(id_num, item_shipment):
                case (False, True):
                    flash("Shipment already exists! Please add more items to "
                          "the existing shipment using the same shipment ID# "
                          "or use a different shipment ID#.")
                    return render_template("shipments.html",
                                           inventory=string_items(),
                                           shipments=string_shipments(),
                                           si_flag=True, info=request.form)
                case (False, False):
                    flash("Shipment with that ID# already exists! Please "
                          "check that the shipment ID# is not already being "
                          "used by another existing shipment.")
                    return render_template("shipments.html",
                                           inventory=string_items(),
                                           shipments=string_shipments(),
                                           si_flag=True, info=request.form)
                case (True, False):
                    flash("Shipment created successfully!")
        # "Add Item to Shipment" submit button was pressed
        elif submit_pressed(request.form) == "Add Item to Shipment":
            sid_num, iid_num, quantity = get_add_to_shipment_info(request.form)
            match add_to_shipment(sid_num, iid_num, quantity):
                case (False, True):
                    flash("The shipment with the given ID# currently does not "
                          "exist. Please check that you are using the correct "
                          "shipment ID#.")
                    return render_template("shipments.html",
                                           inventory=string_items(),
                                           shipments=string_shipments(),
                                           si_flag=False, info=request.form)
                case (True, False):
                    flash("The item(s) with the given ID# currently does not "
                          "exist in the inventory. Please check that you are "
                          "using the correct item ID#.")
                    return render_template("shipments.html",
                                           inventory=string_items(),
                                           shipments=string_shipments(),
                                           si_flag=False, info=request.form)
                case (True, True):
                    flash("Inventory item(s) successfully assigned to "
                          "shipment!")
                case (False, False):
                    flash("Inventory item(s) assignment to shipment "
                          "unsuccessful! Please check your inventory item "
                          "levels and try again.")
                    return render_template("shipments.html",
                                           inventory=string_items(),
                                           shipments=string_shipments(),
                                           si_flag=False, info=request.form)
    return render_template("shipments.html", inventory=string_items(),
                           shipments=string_shipments())


if __name__ == "__main__":
    app.run(debug=True)
