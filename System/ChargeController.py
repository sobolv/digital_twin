from System.Battery import Battery
from System.RemoteMeter import RemoteMeter
from System.SolarPanel import SolarPanel


class ChargeController:
    BATTERY_VOLTAGE = 12
    NOMINAL_CURRENT = 20
    MAXIMUM_VOLTAGE = 50
    SELF_CONSUMPTION = 8.4
    MIN_OPERATING_TEMPERATURE = -35
    MAX_OPERATING_TEMPERATURE = 55

    def __init__(self, solar_panel: SolarPanel, battery: Battery, remote_meter: RemoteMeter):
        self.solar_panel = solar_panel
        self.battery = battery
        self.remote_meter = remote_meter

    def process(self):
        power = self.solar_panel.generate()
        charge_in_percent, voltage = self.battery.charge(power)
        self.remote_meter.display(voltage, charge_in_percent, power)
        # оновити стан батареї(зарядити її battery.charge(power))
        # вивести інформацію на дісплей
        # (опційно) оппрацювати налаштування контролера
        # print("Generated power: " + str(power) + " Battery: " + str(charge_in_percent) + " Voltage: " + str(voltage))
