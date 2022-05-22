from replit import db


# ======================================================================
# Item Dictionary Functions
# ----------------------------------------------------------------------
# These functions provide the methods to manage items in the inventory
# backend (stored in dictionary format). It will be used in the Python
# Flask web application (hosted on repl.it with db being used), as these
# item dictionaries can be stored (in repl.it db).
# ======================================================================

# return item information tuple
def get_add_item_info(item_info):
    return (item_info["id_num"],
            item_info["name"],
            int(item_info["quantity"]),
            float(item_info["buy_price"]),
            float(item_info["sell_price"])
            )


# return item dictionary; id_num forms identifying part of access key to
# this item inside repl.it db
def create_item(name, quantity, buy_price, sell_price) -> dict:
    return {"name": name,
            "quantity": quantity,
            "buy_price": buy_price,
            "sell_price": sell_price
            }


# attempt to add item to inventory or increment same existing item count
def add_item(id_num, item) -> (bool, bool):
    db_id_num = item_id_wrapper(id_num)
    if db_id_num in db:
        if compare_items(item, db[db_id_num]):
            increment_item_quantity(id_num, item["quantity"])
            # return (True, True) if successful and same item exists
            return True, True
        else:
            # return (False, False) if unsuccessful and different
            # item with matching ID# to this item already exists
            return False, False
    else:
        db[db_id_num] = item
        # return (True, False) if successful and item didn't exist
        return True, False


# return item information tuple; the "" or -1 placeholders indicate that
# the specified value stays unchanged
def get_edit_item_info(item_info):
    return (item_info["old_id_num"],
            item_info["id_num"],
            item_info["name"],
            int(item_info["quantity"]) if item_info["quantity"] else -1,
            float(item_info["buy_price"]) if item_info["buy_price"] else -1.0,
            float(item_info["sell_price"]) if item_info["sell_price"] else -1.0
            )


# attempt to edit item in inventory
def edit_item(old_id_num, id_num, name, quantity, buy_price, sell_price) \
        -> (bool, bool):
    changes_made = False
    db_old_id_num = item_id_wrapper(old_id_num)
    db_id_num = item_id_wrapper(id_num)
    if db_old_id_num in db:
        if id_num == "" or old_id_num == id_num:
            if id_num == "":
                db_id_num = db_id_num + old_id_num
            if name != "" and name != db[db_id_num]["name"]:
                db[db_id_num]["name"] = name
                changes_made = True
            if quantity >= 0 and quantity != db[db_id_num]["quantity"]:
                db[db_id_num]["quantity"] = quantity
                changes_made = True
            if buy_price >= 0 and buy_price != db[db_id_num]["buy_price"]:
                db[db_id_num]["buy_price"] = buy_price
                changes_made = True
            if sell_price >= 0 and sell_price != db[db_id_num]["sell_price"]:
                db[db_id_num]["sell_price"] = sell_price
                changes_made = True

            if changes_made:
                # return (True, True) if successful and item exists
                # (i.e. (valid) changes were detected and made)
                return True, True
            else:
                # return (False, True) if unsuccessful and item exists
                # (i.e. no (valid) changes were detected)
                return False, True
        else:
            if db_id_num in db:
                # return (False, True) if unsuccessful and item exists
                # (i.e. new id_num already being used in inventory)
                return False, True
            else:
                if name == "":
                    name = db[db_old_id_num]["name"]
                if quantity < 0:
                    quantity = db[db_old_id_num]["quantity"]
                if buy_price < 0:
                    buy_price = db[db_old_id_num]["buy_price"]
                if sell_price < 0:
                    sell_price = db[db_old_id_num]["sell_price"]
                item = create_item(name, quantity, buy_price, sell_price)
                db[db_id_num] = item
                del db[db_old_id_num]
                # return (True, True) if successful and item exists
                # (i.e. (valid) changes were detected and made)
                return True, True
    else:
        # return (False, False) if unsuccessful and item didn't exist
        return False, False


# increment the quantity of an item in the inventory
def increment_item_quantity(id_num, quantity):
    db[item_id_wrapper(id_num)]["quantity"] += quantity


# attempt to decrement the quantity of an item in the inventory
def decrement_item_quantity(id_num, quantity) -> bool:
    if db[item_id_wrapper(id_num)]["quantity"] >= quantity:
        db[item_id_wrapper(id_num)]["quantity"] -= quantity
        # return True if able to decrement item quantity without it
        # becoming negative
        return True
    else:
        # return False if unable to decrement item quantity without it
        # becoming negative
        return False


# return item information tuple; the "" or -1 placeholders indicate that
# the specified value stays unchanged
def get_delete_item_info(item_info):
    return item_info["id_num"]


# attempt to delete item from inventory
def delete_item(id_num) -> bool:
    db_id_num = item_id_wrapper(id_num)
    if db_id_num in db:
        del db[db_id_num]
        delete_item_from_shipments(id_num)
        # return True if successful in deleting item from inventory and
        # all assigned shipments
        return True
    else:
        # return False if unsuccessful in deleting item from inventory
        # and all assigned shipments (i.e. item not in inventory)
        return False


# attempt to find and delete item from given shipment
def delete_item_from_shipment(db_sid_num, iid_num):
    if iid_num in db[db_sid_num]["items"]:
        del db[db_sid_num]["items"][iid_num]


# attempt to find and delete item from all assigned shipments
def delete_item_from_shipments(iid_num):
    for db_sid_num in db.prefix("S-"):
        delete_item_from_shipment(db_sid_num, iid_num)


# return string representation of item
def string_item(id_num, item) -> str:
    return f"ID#: {id_num} | " \
           f"Name: {item['name']} | " \
           f"Available Quantity: {item['quantity']} | " \
           f"Buy Price: {item['buy_price']:.2f} | " \
           f"Sell Price {item['sell_price']:.2f}"


# return list of string representation of all items in inventory
def string_items():
    return [string_item(item_id_unwrapper(db_id_num), db[db_id_num])
            for db_id_num in db.prefix("I-")]


# print string representation of item to console for debugging purposes
def print_item(id_num, item):
    print(f"ID#: {id_num} | "
          f"Name: {item['name']} | "
          f"Available Quantity: {item['quantity']} | "
          f"Buy Price: {item['buy_price']:.2f} | "
          f"Sell Price {item['sell_price']:.2f}")


# compare two items to see if both represent same item; return True if
# so, else False; item quantities may vary
def compare_items(item1, item2) -> bool:
    return item1["name"] == item2["name"] \
           and item1["buy_price"] == item2["buy_price"] \
           and item1["sell_price"] == item2["sell_price"]


# add the "I-" prefix to be used in the repl.it db to differentiate
# between items ("I-") and shipments ("S-")
def item_id_wrapper(id_num):
    return f"I-{id_num}"


# remove the "I-" prefix used in the repl.it db to differentiate between
# items ("I-") and shipments ("S-")
def item_id_unwrapper(db_id_num):
    return db_id_num.removeprefix("I-")
