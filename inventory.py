import json

class ItemList():
    def __init__(
        self
    ):

        self.items = json.load(open("items/items.json"))
        self.item_list_pages = {}

        for i, item in enumerate(self.items["items"]):
            if int((i + 1) / 11 + 1) not in self.item_list_pages:
                self.item_list_pages[int((i + 1) / 11 + 1)] = []
            self.item_list_pages[int((i + 1) / 11 + 1)].append(self.items["items"][item])

    def get_item_pages(self):
        return self.item_list_pages