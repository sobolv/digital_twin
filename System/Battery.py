import math

from System.charging_interpolation import spline_interpolation
from System import config


class Battery:
    NOMINAL_VOLTAGE = 12
    CAPACITY = 40  # Ah
    MIN_OPERATING_TEMPERATURE = -20
    MAX_OPERATING_TEMPERATURE = 60
    POWER = NOMINAL_VOLTAGE * CAPACITY
    voltage = 0
    current_charge = 0  # Ah які є в акумуляторі
    charge_in_percent = 0
    degradation_percentage_per_cycle = 0.00025
    charge_cycles = 0
    charge_summary = 0

    def charge(self, power: int):
        self.update_actual_capacity()
        self.add_charge_summary(power)
        if self.charge_in_percent <= 50:
            print("Higher battery degradation below 50% charge")
        if self.charge_in_percent < 100:
            if (self.current_charge + power / self.NOMINAL_VOLTAGE) >= self.CAPACITY:
                self.current_charge = self.CAPACITY
            else:
                self.current_charge += power / self.NOMINAL_VOLTAGE
            self.charge_in_percent = (self.current_charge / self.CAPACITY) * 100
            self.voltage = spline_interpolation(config.battery_charge_voltage_x, config.battery_charge_percentage_y,
                                                self.charge_in_percent)
        return self.charge_in_percent, self.voltage

    def add_charge_summary(self, power):
        self.charge_summary += math.modf(power / self.NOMINAL_VOLTAGE)

    def discharge(self, power: int):
        self.update_actual_capacity()
        self.add_charge_summary(power)
        if self.charge_in_percent <= 50:
            print("Higher battery degradation below 50% charge")
        if self.charge_in_percent > 0:
            if (self.current_charge - power / self.NOMINAL_VOLTAGE) <= 0:
                self.current_charge = 0
            else:
                self.current_charge -= power / self.NOMINAL_VOLTAGE
            self.charge_in_percent = (self.current_charge / self.CAPACITY) * 100
            self.voltage = spline_interpolation(config.battery_charge_voltage_x, config.battery_charge_percentage_y,
                                                self.charge_in_percent)
        return self.charge_in_percent, self.voltage

    def update_actual_capacity(self):
        if self.charge_summary >= self.CAPACITY:
            if self.charge_in_percent <= 50:
                self.charge_cycles += 1.5
            else:
                self.charge_cycles += 1
            self.charge_summary = 0
        self.CAPACITY *= (1 - (self.charge_cycles * self.degradation_percentage_per_cycle))

