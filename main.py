import os
# from replit import db
from flask import Flask, redirect, url_for, render_template, request, flash

# from Backend.Item import Item
# from Backend.Shipment import Shipment
from Backend.BackendManagement import *

template_dir = os.path.abspath("Frontend/Templates/")
app = Flask(__name__, template_folder=template_dir)
app.secret_key = "fswd-python"

items = {}
# for key in db.prefix("I-"):
#     items[key] = db[key]
item_shipments = {}
# for key in db.prefix("S-"):
#     item_shipments[key] = db[key]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inventory/", methods=["POST", "GET"])
def inventory():
    if request.method == "POST":
        id_num = request.form["id_num"]
        name = request.form["name"]
        quantity = int(request.form["quantity"])
        buy_price = float(request.form["buy_price"])
        sell_price = float(request.form["sell_price"])

        # item = Item(id_num, name, quantity, buy_price, sell_price)
        item = create_item(name, quantity, buy_price, sell_price)
        if id_num in items:
            # if items[id_num] == item:
            if compare_items(item, items[id_num]):
                # items[id_num].increment_quantity(quantity)
                items[id_num]["quantity"] += quantity
                # db[f"I-{id_num}"].increment_quantity(quantity)
                # db[f"I-{id_num}"]["quantity"] += quantity
                flash("Item already exists in the inventory, and its quantity has been incremented successfully!")
            else:
                flash("Unable to add item to inventory! Please check that the item ID# is not already being used " +
                      "by another item in the inventory.")
                print(request.form)
                return render_template("inventory.html", inventory=[string_item(id_num, items[id_num]) for id_num in
                                                                    items], info=request.form)
        else:
            items[id_num] = item
            # db[f"I-{id_num}"] = items[id_num]
            flash("Item added to inventory successfully!", "info")
    return render_template("inventory.html", inventory=[string_item(id_num, items[id_num]) for id_num in items])


@app.route("/shipments/", methods=["POST", "GET"])
def shipments():
    if request.method == "POST":
        if request.form["submit"] == "Create Shipment":
            id_num = request.form["id_num"]
            name = request.form["name"]
            address = {"street_address": request.form["street_address"], "town_city": request.form["town_city"],
                       "province_state": request.form["province_state"], "country": request.form["country"],
                       "postal_zip_code": request.form["postal_zip_code"]}

            # item_shipment = Shipment(id_num, name, address)
            item_shipment = create_shipment(name, address)
            if id_num in item_shipments:
                # if item_shipments[id_num] == item_shipment:
                if compare_shipments(item_shipment, item_shipments[id_num]):
                    flash("Shipment already exists! Please add more items to the existing shipment using the same " +
                          "shipment ID# or use a different shipment ID#.")
                else:
                    flash("Shipment with that ID# already exists! Please check that the shipment ID# is not already " +
                          "being used by another existing shipment.")
                return render_template("shipments.html", shipments=item_shipments, si_flag=True, info=request.form)
            else:
                item_shipments[id_num] = item_shipment
                # db[f"S-{id_num}] = item_shipments[id_num]
                flash("Shipment created successfully!")
        elif request.form["submit"] == "Add Item to Shipment":
            sid_num = request.form["sid_num"]
            iid_num = request.form["iid_num"]
            quantity = int(request.form["quantity"])

            if sid_num not in item_shipments:
                flash("The shipment with the given ID# currently does not exist. Please check that you are using the " +
                      "correct shipment ID#.")
                return render_template("shipments.html", shipments=item_shipments, si_flag=False, info=request.form)
            elif iid_num not in items:
                flash("The item(s) with the given ID# currently does not exist in the inventory. Please check that " +
                      "you are using the correct item ID#.")
                return render_template("shipments.html", shipments=item_shipments, si_flag=False, info=request.form)
            # success = items[iid_num].decrement_quantity(quantity)
            elif items[iid_num]["quantity"] >= quantity:
                items[iid_num]["quantity"] -= quantity
                # item_shipments[sid_num].add_item(iid_num, quantity)
                if iid_num in item_shipments[sid_num]["items"]:
                    item_shipments[sid_num]["items"][iid_num] += quantity
                else:
                    item_shipments[sid_num]["items"][iid_num] = quantity
                flash("Inventory item(s) successfully assigned to shipment!")
            # success = db["I-{iid_num}].decrement_quantity(quantity)
            # elif db[f"I-{iid_num}]["quantity"] >= quantity:
                # db[f"I-{iid_num}]["quantity"] -= quantity
                # db[f"S-{sid_num}].add_item(iid_num, quantity)
                # db[f"S-{sid_num}]["items"][iid_num] = quantity
                # flash("Inventory item(s) successfully assigned to shipment!")
            else:
                flash("Inventory item(s) assignment to shipment unsuccessful! Please check your inventory item levels" +
                      " and try again.")
                return render_template("shipments.html", shipments=item_shipments, si_flag=False, info=request.form)
    return render_template("shipments.html", shipments=item_shipments)


if __name__ == "__main__":
    app.run(debug=True)
