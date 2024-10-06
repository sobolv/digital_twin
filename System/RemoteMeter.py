from System import config


class RemoteMeter:
    SYSTEM_VOLTAGE = 12
    # не включно
    MAX_CONSUMPTION_WITH_BACKLIGHT_AND_SIREN_ON = 65
    MAX_CONSUMPTION_WITH_BACKLIGHT_ON = 23
    MAX_CONSUMPTION_WITH_BACKLIGHT_OFF = 15

    MIN_OPERATING_TEMPERATURE = -20
    MAX_OPERATING_TEMPERATURE = 70

    def display(self, battery_voltage: float, battery_percent: int, panel_power: float):
        print("Generated power: %.2fW" % panel_power)
        print("Battery condition:")
        print("Charge in percent: %d%%     Voltage: %.2fV" % (battery_percent, battery_voltage))
        print("Cycles: %d     Voltage: %.2fV" % (battery_percent, battery_voltage))
        print()






