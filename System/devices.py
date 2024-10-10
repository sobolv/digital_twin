import random

from System import config

class HairDryer:
    POWER = 2100

    def power_on(self, temperature: int, speed: int):
        power_map = {
            (1, 1): 700,
            (2, 1): 1000,
            (3, 1): 1500,
            (1, 2): 900,
            (2, 2): 1500,
            (3, 2): self.POWER,
        }
        return power_map.get((temperature, speed))/config.time_delta



class Fridge:
    MODEL = "Snaige FR24SM-PRDLOE"
    NOMINAL_POWER = 476
    MIN_START_POWER = 500
    MAX_START_POWER = 1000
    MIN_START_TIME = 1 #seconds
    MAX_START_TIME = 2 #seconds

    def __init__(self):
        self.current_time = 0

    def power_on(self):
        if self.current_time <= self.MAX_START_TIME:
            power = random.randint(self.MIN_START_POWER, self.MAX_START_POWER) / config.time_delta
        else:
            power = self.NOMINAL_POWER / config.time_delta

        if config.time_delta == 60:
            self.current_time += 60
        elif config.time_delta == 3600:
            self.current_time += 1
        else:
            self.current_time += 3600
        return power


class Lamp:
    MODEL = "IKEA ARSTID + LED lamp"
    NOMINAL_POWER = 8

    def power_on(self):
        return self.NOMINAL_POWER/config.time_delta


class Microwave:
    MODEL = "Samsung MW3000AM MS20A3010AL"
    MODE = {120, 250, 380, 500, 700}

    def power_on(self, mode: int):
        return mode/config.time_delta


class TV:
    MODEL = "Samsung UE60DU7100UXUA"
    MAX_POWER = 140
    NOMINAL_POWER = 108
    STAND_BY_MODE_POWER = 0.5

    def power_on(self):
        return random.randint(self.NOMINAL_POWER, self.MAX_POWER)/config.time_delta


class Kettle:
    MODEL = "Philips Daily Collection HD9350/90"
    NOMINAL_POWER = 2200
    STAND_BY_MODE_POWER = 0.5
    start_temperature = 20

    def __init__(self, amount_of_water: int, start_temperature: int):
        self.time = (4.186 * amount_of_water * (100 - start_temperature))/self.NOMINAL_POWER
        self.current_time = 0

    def power_on(self):
        if self.current_time < self.time:
            if config.time_delta == 60:
                self.current_time += 60
            elif config.time_delta == 3600:
                self.current_time += 1
            elif config.time_delta == 1:
                self.current_time += 3600
            return self.NOMINAL_POWER/config.time_delta
        return 0


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