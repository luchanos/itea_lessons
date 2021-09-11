class Chest:
    def __init__(self, material):
        self.material = material

    def __str__(self):
        return f"сундук сделан из: {self.material}\nв адресе памяти: {id(self)}"


# это чертеж
class Key:
    def __init__(self, material):
        self.material = material

    def open_chest(self, chest: Chest):
        print(f"вы только что с помощью {self} открыли {chest}")

    def __str__(self):
        return f"ключ из: {self.material}\nв адресе памяти: {id(self)}"


key_1 = Key("steel")
key_2 = Key("ferrum")
key_3 = Key("cobalt")

chest_1 = Chest("wood")
chest_2 = Chest("gold")

key_1.open_chest(chest_1)
key_2.open_chest(chest_1)
