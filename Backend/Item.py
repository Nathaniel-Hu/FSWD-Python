# ======================================================================
# Item Class
# ----------------------------------------------------------------------
# This class provides the attributes and methods to manage items in the
# inventory backend. However, it will not be used in the Python Flask
# web application (hosted on repl.it with db being used), as these item
# objects cannot be stored (in repl.it db).
# ======================================================================
class Item:
    def __init__(self, id_num, name, quantity, buy_price, sell_price):
        self.id_num = id_num
        self.name = name
        self.quantity = quantity
        self.buy_price = buy_price
        self.sell_price = sell_price

    def get_id_num(self) -> str:
        return self.id_num

    def get_name(self) -> str:
        return self.name

    def get_quantity(self) -> int:
        return self.quantity

    def get_buy_price(self) -> float:
        return self.buy_price

    def get_sell_price(self) -> float:
        return self.sell_price

    def set_id_num(self, id_num):
        self.id_num = id_num

    def set_name(self, name):
        self.name = name

    def set_quantity(self, quantity):
        self.quantity = quantity

    def increment_quantity(self, quantity):
        self.quantity += quantity

    def decrement_quantity(self, quantity) -> bool:
        if self.quantity >= quantity:
            self.quantity -= quantity
            return True
        else:
            return False

    def set_buy_price(self, buy_price):
        self.buy_price = buy_price

    def set_sell_price(self, sell_price):
        self.sell_price = sell_price

    def __str__(self):
        return f"ID#: {self.id_num} | " \
               f"Name: {self.name} | " \
               f"Available Quantity: {self.quantity} | " \
               f"Buy Price: {self.buy_price:.2f} | " \
               f"Sell Price {self.sell_price:.2f}"

    def __eq__(self, obj):
        return isinstance(obj, Item) and (self.id_num == obj.id_num
                                          and self.name == obj.name
                                          and self.buy_price == obj.buy_price
                                          and self.sell_price == obj.sell_price
                                          )
