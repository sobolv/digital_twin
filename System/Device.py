class Device:
    # Додати конструктор на створення чисто по потужності(при умові, що воно під'єднано без зарядки), також додати
    # поле-маркер чи є зарядка в пристрої, при підключенні через зарядку врахувати коефіцієнт перетворення
    def __init__(self, name: str, current: int, voltage: int, has_charger):
        self.name = name
        self.current = current
        self.voltage = voltage
        self.power = current * voltage
        self.has_charger = has_charger

    def __init__(self, name: str, power: int, has_charger):
        self.name = name
        self.power = power
        self.voltage = 220
        self.current = power/220
        self.has_charger = has_charger
