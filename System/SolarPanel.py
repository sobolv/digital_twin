from System import config

# Додати кут нахилу панелі
# Запам'ятовувати старі парметри після виходу з програми

class SolarPanel:
    NOMINAL_POWER = 275
    SHORT_CIRCUIT_CURRENT = 9.2 # Якщо акум в нулі
    OPEN_CIRCUIT_POWER = 38.9 # Макс напруга в середині панелі
    # MAX_SYSTEM_VOLTAGE = 1000
    MAX_POINT_CURRENT = 8.7 # Макс для зарядки акуму
    MAX_POINT_VOLTAGE = 31.6
    # MAX_REVERSE_CURRENT = 20
    NOCT = 45
    PMPP = -0.0029

    def generate(self):
        return self.generate_power() / config.time_delta

    def generate_power(self):
        power = self.NOMINAL_POWER * (config.solar_irradiance / 1000) * (1 - config.shadow_coefficient) * (
                    1 + self.PMPP * (config.panel_temperature - 25))
        return power

    def generate_power_from_ui(self, solar_irradiance, shadow_coefficient, panel_temperature):
        power = self.NOMINAL_POWER * (solar_irradiance / 1000) * (1 - shadow_coefficient) * (
                1 + self.PMPP * (panel_temperature - 25))
        return power
