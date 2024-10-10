import math

from System import config
from System.charging_interpolation import spline_interpolation


# Перегрів батареї
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

    def set_charge_cycles(self, charge_cycles):
        self.charge_cycles = charge_cycles

    def get_charge_cycles(self):
        return self.charge_cycles

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
            self.voltage = spline_interpolation(config.battery_charge_percentage_x, config.battery_charge_voltage_y,
                                                self.charge_in_percent)
        self.check_battery_values()
        return self.charge_in_percent, self.voltage, self.charge_cycles

    def check_battery_values(self):
        if self.charge_in_percent >= 100:
            self.charge_in_percent = 100
        if self.charge_in_percent <= 0:
            self.charge_in_percent = 0
        if self.voltage >= 12.85:
            self.voltage = 12.85
        if self.voltage <= 10.5:
            self.voltage = 10.5

    def add_charge_summary(self, power):
        if self.charge_in_percent >= 100:
            power = 0.5
        self.charge_summary += math.fabs(power / self.NOMINAL_VOLTAGE)

    def discharge(self, power: int):
        print(f"Discharge for {power}")
        self.update_actual_capacity()
        if self.charge_in_percent <= 50:
            print("Higher battery degradation below 50% charge")
        if self.charge_in_percent > 0:
            if (self.current_charge - power / self.NOMINAL_VOLTAGE) <= 0:
                self.current_charge = 0
            else:
                self.current_charge -= power / self.NOMINAL_VOLTAGE
            self.charge_in_percent = (self.current_charge / self.CAPACITY) * 100
            self.voltage = spline_interpolation(config.battery_charge_percentage_x, config.battery_charge_voltage_y,
                                                self.charge_in_percent)
        self.check_battery_values()
        return self.charge_in_percent, self.voltage

    def update_actual_capacity(self):
        if self.charge_summary >= self.CAPACITY:
            if self.charge_in_percent <= 50:
                self.charge_cycles += 1.2
            else:
                self.charge_cycles += 1
            self.charge_summary = 0
            self.CAPACITY *= (1 - (self.charge_cycles * self.degradation_percentage_per_cycle))
