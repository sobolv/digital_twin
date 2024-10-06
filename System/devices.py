class HairDryer:
    POWER = 2100

    def power_on(self, temperature: int, speed: int):
        if temperature == 1 and speed == 1:
            return 700
        elif temperature == 2 and speed == 1:
            return 1000
        elif temperature == 3 and speed == 1:
            return 1500
        elif temperature == 1 and speed == 2:
            return 900
        elif temperature == 2 and speed == 2:
            return 1500
        elif temperature == 3 and speed == 2:
            return 2100



class Fridge:
    MODEL = "Snaige FR24SM-PRDLOE"
    NOMINAL_POWER = 476
    MIN_START_POWER = 500
    MAX_START_POWER = 1000
    MIN_START_TIME = 0.00028
    MAX_START_TIME = 0.00056


class Lamp:
    MODEL = "IKEA ARSTID + LED lamp"
    NOMINAL_POWER = 8


class Microwave:
    MODEL = "Samsung MW3000AM MS20A3010AL"
    MODE = {120, 250, 380, 500, 700}


class TV:
    MODEL = "Samsung UE60DU7100UXUA"
    MAX_POWER = 140
    NOMINAL_POWER = 108
    STAND_BY_MODE_POWER = 0.5


class Kettle:
    MODEL = "Philips Daily Collection HD9350/90"
    NOMINAL_POWER = 2200
    start_temperature = 20

    def power_on(self, start_temperature: int, amount_of_water: int):
        time = 4,186 * amount_of_water * (100 - start_temperature)/self.NOMINAL_POWER
        return time


class Phone:
    MODEL = "iPhone 15"
    POWER = 15.18
    MIN_STAND_BY_MODE_POWER = 0.1
    MAX_STAND_BY_MODE_POWER = 0.5
    CHARGER_POWER = 20
    TIME_TO_50 = 0.5
    MIN_TIME_FROM_50_TO_100 = 1
    MAX_TIME_FROM_50_TO_100 = 1.167


class Laptop:
    MODEL = "HP Probook 440 g6"
    POWER = 52.94
    MIN_STAND_BY_MODE_POWER = 0.5
    MAX_STAND_BY_MODE_POWER = 2
    CHARGER_POWER = 45
    MIN_TIME_TO_80 = 1
    MAX_TIME_TO_80 = 1.42
    MIN_TIME_FROM_80_TO_100 = 0.5
    MAX_TIME_FROM_80_TO_100 = 0.67


class PowerBank:
    MODEL = "Xiaomi PB1022ZM"
    MIN_POWER = 45
    MAX_POWER = 50
    CHARGER_POWER = 18
    STAND_BY_MODE_POWER = 0.5
    TIME_TO_80 = 2.5
    MIN_TIME_FROM_80_TO_100 = 0.5
    MAX_TIME_FROM_80_TO_100 = 1