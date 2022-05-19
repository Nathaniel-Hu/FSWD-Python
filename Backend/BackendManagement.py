# ------------------------------------------------------------------------------------------------------------
# Item Management Functions
# ------------------------------------------------------------------------------------------------------------
# return item dictionary; item id_num used as key to access this dictionary inside replit db
def create_item(name, quantity, buy_price, sell_price) -> dict:
    return {"name": name, "quantity": quantity, "buy_price": buy_price, "sell_price": sell_price}


# return string representation of item
def string_item(id_num, item) -> str:
    return f"ID#: {id_num} | Name: {item['name']} | Available Quantity: {item['quantity']} | " \
           f"Buy Price: {item['buy_price']:.2f} | Sell Price {item['sell_price']:.2f}"


# print string representation of item to console (for debugging purposes)
def print_item(id_num, item):
    print(f"ID#: {id_num} | Name: {item['name']} | Available Quantity: {item['quantity']} | "
          f"Buy Price: {item['buy_price']:.2f} | Sell Price {item['sell_price']:.2f}")


# compare two items to check if both represent the same item; quantities can vary for same items
def compare_items(item1, item2) -> bool:
    return item1["name"] == item2["name"] and item1["buy_price"] == item2["buy_price"] and \
           item1["sell_price"] == item2["sell_price"]


# ------------------------------------------------------------------------------------------------------------
# Shipment Management Functions
# ------------------------------------------------------------------------------------------------------------
# return shipment dictionary; shipment id_num used as key to access this dictionary inside replit db
def create_shipment(deliveree, address, items_info=None) -> dict:
    if items_info is None:
        items = {}
    else:
        # item_info = (item_id_num, item_quantity)
        items = {item_info[0]: item_info[1] for item_info in items_info}
    return {"deliveree": deliveree, "address": address, "items": items}


# return address dictionary; "address" used as key to access this dictionary inside shipment dictionary
def create_address(street_address, town_city, province_state, country, postal_zip_code) -> dict:
    return {"street_address": street_address, "town_city": town_city, "province_state": province_state,
            "country": country, "postal_zip_code": postal_zip_code}


# return string representation of shipment info
def string_shipment_info(id_num, shipment) -> str:
    return f"Shipment ID#: {id_num}\nDeliveree: {shipment['deliveree']}\n" \
           f"Address:\n{shipment['address']['street_address']}\n{shipment['address']['town_city']}, " \
           f"{shipment['address']['province_state']}, {shipment['address']['country']}\n" \
           f"{shipment['address']['postal_zip_code']}\n"


# return list of string representations of shipment items
def string_shipment_items(shipment) -> [str]:
    return [f"Item ID#: {item_id_num} | Item Quantity: {shipment['item_id_nums'][item_id_num]}" for item_id_num in
            shipment["item_id_nums"]]


# print string representation of shipment info to console (for debugging purposes)
def print_shipment_info(id_num, shipment):
    print(f"Shipment ID#: {id_num}\nDeliveree: {shipment['deliveree']}\n"
          f"Address:\n{shipment['address']['street_address']}\n{shipment['address']['town_city']}, "
          f"{shipment['address']['province_state']}, {shipment['address']['country']}\n"
          f"{shipment['address']['postal_zip_code']}\n")


# print list of string representations of shipment items to console (for debugging purposes)
def print_shipment_items(shipment):
    for item_id_num in shipment["item_id_nums"]:
        print(f"Item ID#: {item_id_num} | Item Quantity: {shipment['item_id_nums'][item_id_num]}")


# compare two shipments to check if both represent the same shipment; items can vary for same shipments
def compare_shipments(shipment1, shipment2) -> bool:
    return shipment1["deliveree"] == shipment2["deliveree"] and shipment1["address"] == shipment2["address"]
