class Item:
    def __init__(self, id_num, name, quantity, buy_price, sell_price):
        self.id_num = id_num
        self.name = name
        self.quantity = quantity
        self.buy_price = buy_price
        self.sell_price = sell_price

    def get_id_num(self) -> int:
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

    def set_buy_price(self, buy_price):
        self.buy_price = buy_price

    def set_sell_price(self, sell_price):
        self.sell_price = sell_price
