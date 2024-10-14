import random

from System import config
from System.Battery import Battery
from System.Device import Device

# Врахувати втрати при перетворенні
# Додати вентилятор при споживанні > 200Вт
# Додати кпд на інвертор, чим нижча напруга на акум ти нижч кпд
# 2000 - споживана потужність, 1600 - вхідна
# перевірка на перевантаження інвертора по А (10А)
# додати темп до інвертора

class Inverter:
    NOMINAL_POWER = 2000
    ALLOWABLE_PEAK_POWER = 4000
    NOMINAL_INPUT_VOLTAGE = 12
    MIN_NOMINAL_OUTPUT_VOLTAGE = 220
    MAX_NOMINAL_OUTPUT_VOLTAGE = 240
    devices = []
    total_power = 0

    def __init__(self, battery: Battery):
        self.battery = battery

    def power(self):
        power = self.total_power / config.time_delta
        charge_in_percent, voltage = self.battery.discharge(power)
        # print("Total power: " + str(power) + " Battery: " + str(charge_in_percent) + " Voltage: " + str(voltage))

    def power_with_load(self, current_load):
        power = current_load
        charge_in_percent, voltage = self.battery.discharge(power)
        return power, charge_in_percent, voltage

    def power_with_load_amps(self, current_amp_draw, time_delta):
        power = current_amp_draw * self.MIN_NOMINAL_OUTPUT_VOLTAGE / time_delta
        charge_in_percent, voltage = self.battery.discharge(power)
        return power, charge_in_percent, voltage

    def add_device(self, device: Device):
        self.devices.append(device)
        self.count_total_power()

    def delete_device(self, device: Device):
        if device in self.devices:
            self.devices.remove(device)
        else:
            print("Прилад не знайдено")
        self.count_total_power()

    def count_total_power(self):
        if len(self.devices) > 0:
            power = 0
            for i in range(0, len(self.devices)):
                if self.devices[i].has_charger:
                    power += self.devices[i].power  # врахувати коефіцієнт перетворення
                else:
                    power += self.devices[i].power
            self.total_power = power
        else:
            self.total_power = 0




# у інвертора буде список під'єднаних приладів. просумувати їх споживання
# battery.discharge(сумарне споживання під'єднаних приладів)

