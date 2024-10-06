import time

from System import config
from System.Battery import Battery
from System.ChargeController import ChargeController
from System.Inverter import Inverter
from System.RemoteMeter import RemoteMeter
from System.SolarPanel import SolarPanel


if __name__ == '__main__':
    panel = SolarPanel()
    battery = Battery()
    remote_meter = RemoteMeter()
    controller = ChargeController(panel, battery, remote_meter)
    inverter = Inverter(battery)

    if config.time_delta == 1:
        print("Hour result:")
    elif config.time_delta == 60:
        print("Minute result:")
    elif config.time_delta == 3600:
        print("Second result:")

    for i in range(1, 20):
        inverter.power()
        controller.process()

        # заживити споживачів inverter.power()
        time.sleep(1)

