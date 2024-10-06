import numpy as np


time_delta = 1  # За годину
solar_irradiance = 1000
panel_temperature = 25
shadow_coefficient = 0

battery_charge_voltage_x = np.array([12.85, 12.75, 12.50, 12.30, 12.15, 12.05,11.95, 11.81, 11.66, 11.51, 10.50])
battery_charge_percentage_y = np.array([100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0])