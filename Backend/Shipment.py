class Shipment:
    def __init__(self, id_num, deliveree, address, items_info=None):
        self.id_num = id_num
        self.deliveree = deliveree
        self.address = address
        self.items = {}

        if items_info:
            self.add_items(items_info)

    def add_item(self, item_id_num, item_quantity):
        if item_id_num in self.items:
            self.items[item_id_num] += item_quantity
        else:
            self.items[item_id_num] = item_quantity

    def add_items(self, items_info):
        for item_info in items_info:
            # item_info = (item_id_num, item_quantity)
            self.add_item(item_info[0], item_info[1])

    def del_item(self, item_id_num):
        del self.items[item_id_num]

    def del_items(self, item_id_nums):
        for item_id_num in item_id_nums:
            self.del_item(item_id_num)

    def get_id_num(self) -> str:
        return self.id_num

    def get_deliveree(self) -> str:
        return self.deliveree

    def get_address(self) -> str:
        return self.address

    def get_item_id_nums(self) -> [str]:
        return self.items.keys()

    def get_items(self) -> {str: int}:
        return self.items

    def get_items_display(self):
        return [f"Item ID#: {item_id_num} | Item Quantity: {self.items[item_id_num]}" for item_id_num in self.items]

    def get_item_quantity(self, item_id_num) -> int:
        return self.items[item_id_num]

    def set_id_num(self, id_num):
        self.id_num = id_num

    def set_deliveree(self, deliveree):
        self.deliveree = deliveree

    def set_address(self, address):
        self.address = address

    def set_item_quantity(self, item_id_num, item_quantity):
        self.items[item_id_num] = item_quantity

    def __str__(self):
        return f"Shipment ID#: {self.id_num}\nDeliveree: {self.deliveree}\n" \
               f"Address:\n{self.address['street_address']}\n{self.address['town_city']}, " \
               f"{self.address['province_state']}, {self.address['country']}\n{self.address['postal_zip_code']}\n"

    def __eq__(self, obj):
        return isinstance(obj, Shipment) and (self.id_num == obj.id_num and self.deliveree == obj.deliveree and
                                              self.address == obj.address)
