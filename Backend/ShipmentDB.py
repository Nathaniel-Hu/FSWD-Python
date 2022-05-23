from replit import db

from Backend.ItemDB import item_id_wrapper, decrement_item_quantity


# ======================================================================
# Shipment Dictionary Functions
# ----------------------------------------------------------------------
# These functions provide the methods to manage shipments in the backend
# (stored in dictionary format). It will be used in the Python Flask web
# application (hosted on repl.it with db being used), as these shipment
# dictionaries can be stored (in repl.it db).
# ======================================================================

# return shipment information tuple
def get_create_shipment_info(shipment_info):
    return (shipment_info["id_num"],
            shipment_info["name"],
            create_address(shipment_info)
            )


# return address dictionary; "address" used as key to access this
# address dictionary inside the shipment dictionary
def create_address(shipment_info) -> dict:
    return {"street_address": shipment_info["street_address"],
            "town_city": shipment_info["town_city"],
            "province_state": shipment_info["province_state"],
            "country": shipment_info["country"],
            "postal_zip_code": shipment_info["postal_zip_code"]
            }


# return shipment dictionary; id_num forms identifying part of access
# key to this shipment inside repl.it db
def create_shipment(deliveree, address, items_info=None) -> dict:
    if items_info is None:
        items = {}
    else:
        # item_info = (item_id_num, item_quantity)
        items = {item_info[0]: item_info[1] for item_info in items_info}
    return {"deliveree": deliveree, "address": address, "items": items}


# attempt to add shipment to log of shipments
def add_shipment(id_num, shipment) -> (bool, bool):
    db_id_num = shipment_id_wrapper(id_num)
    if db_id_num in db:
        if compare_shipments(shipment, db[db_id_num]):
            # return (False, True) if unsuccessful and same shipment
            # already exists
            return False, True
        else:
            # return (False, False) if unsuccessful and different
            # shipment with matching ID# to this shipment already exists
            return False, False
    else:
        db[db_id_num] = shipment
        # return (True, False) if successful and shipment didn't exist
        return True, False


# return item information tuple; the "" or -1 placeholders indicate that
# the specified value stays unchanged
def get_add_to_shipment_info(item_info):
    return (item_info["sid_num"],
            item_info["iid_num"],
            int(item_info["quantity"])
            )


# attempt to add item(s) to shipment
def add_to_shipment(sid_num, iid_num, quantity) -> (bool, bool):
    db_sid_num = shipment_id_wrapper(sid_num)
    db_iid_num = item_id_wrapper(iid_num)
    if db_sid_num not in db:
        # return (False, True) if shipment doesn't exist and item to be
        # added exists (assumed)
        return False, True
    elif db_iid_num not in db:
        # return (True, False) if shipment exists and item to be added
        # doesn't exist
        return True, False
    elif decrement_item_quantity(iid_num, quantity):
        if shipment_contains_item(sid_num, iid_num):
            increment_item_to_shipment(sid_num, iid_num, quantity)
        else:
            add_item_to_shipment(sid_num, iid_num, quantity)
        return True, True
    else:
        # return (False, False) if unsuccessful and item quantity in
        # inventory is not high enough (i.e. not enough of item to
        # assign to this shipment)
        return False, False


# add item quantity to shipment
def add_item_to_shipment(sid_num, iid_num, quantity):
    db[shipment_id_wrapper(sid_num)]["items"][iid_num] = quantity


# increment item quantity of shipment
def increment_item_to_shipment(sid_num, iid_num, quantity):
    db[shipment_id_wrapper(sid_num)]["items"][iid_num] += quantity


# check shipment to see if already contains the item to be added
def shipment_contains_item(sid_num, iid_num):
    return iid_num in db[shipment_id_wrapper(sid_num)]["items"]


# return string representation of shipment info
def string_shipment_info(id_num, shipment) -> str:
    return f"Shipment ID#: {id_num}\n" \
           f"Deliveree: {shipment['deliveree']}\n" \
           f"Address:\n{shipment['address']['street_address']}\n" \
           f"{shipment['address']['town_city']}, " \
           f"{shipment['address']['province_state']}, " \
           f"{shipment['address']['country']}\n" \
           f"{shipment['address']['postal_zip_code']}\n"


# return list of string representations of shipment items
def string_shipment_items(shipment) -> [str]:
    return [f"Item ID#: {id_num} | Item Quantity: {shipment['items'][id_num]}"
            for id_num in shipment["items"]]


# return dictionary of shipment info strings and shipments item strings
# for all existing shipments and all items assigned to each shipment
def string_shipments() -> dict:
    return {shipment_id_unwrapper(db_id_num): {
        "shipment_info": string_shipment_info(shipment_id_unwrapper(db_id_num),
                                              db[db_id_num]),
        "shipment_items": string_shipment_items(db[db_id_num])}
        for db_id_num in db.prefix("S-")}


# print string representation of shipment info to console (for debugging
# purposes)
def print_shipment_info(id_num, shipment):
    print(f"Shipment ID#: {id_num}\n"
          f"Deliveree: {shipment['deliveree']}\n"
          f"Address:\n{shipment['address']['street_address']}\n"
          f"{shipment['address']['town_city']}, "
          f"{shipment['address']['province_state']}, "
          f"{shipment['address']['country']}\n"
          f"{shipment['address']['postal_zip_code']}\n")


# print list of string representations of shipment items to console (for
# debugging purposes)
def print_shipment_items(shipment):
    for id_num in shipment["item_id_nums"]:
        print(f"Item ID#: {id_num} | "
              f"Item Quantity: {shipment['items'][id_num]}")


# compare two shipments to check if both represent the same shipment;
# items can vary for same shipments
def compare_shipments(shipment1, shipment2) -> bool:
    return shipment1["deliveree"] == shipment2["deliveree"] \
           and shipment1["address"] == shipment2["address"]


# add the "S-" prefix to be used in the repl.it db to differentiate
# between shipments ("S-") and items ("I-")
def shipment_id_wrapper(id_num):
    return f"S-{id_num}"


# remove the "S-" prefix used in the repl.it db to differentiate between
# shipments ("S-") and items ("I-")
def shipment_id_unwrapper(db_id_num):
    return db_id_num.removeprefix("S-")
