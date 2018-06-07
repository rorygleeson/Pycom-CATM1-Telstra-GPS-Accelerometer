import pycoproc
import pycom
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
import gc
import time
import machine
import ubinascii




led_red    = 0xf00000
led_green  = 0x0ff000
led_blue   = 0x0f0ff0
led_yellow = 0xf0f000
led_orange = 0xf00f00
led_purple = 0xf000ff
led_white  = 0xf0f0f0


def flashLed(ledColor, numflashes):
    x = 0
    while x < numflashes:
        pycom.rgbled(ledColor)
        time.sleep(0.2)
        pycom.heartbeat(False)
        time.sleep(0.2)
        x += 1



print("Starting boot")
pycom.wifi_on_boot(False)
pycom.heartbeat(False)
time.sleep(2)
py = Pytrack()
li = LIS2HH12()


print("Get Wakeup reason")
reason = py.get_wake_reason()
print("Wakeup reason")
print(reason)

print("Get Mac ID ..")
dev_id = ubinascii.hexlify(machine.unique_id(),':').decode()
print("Mac ID is ..")
print(dev_id)


print("Get Voltage ..")
voltage = py.read_battery_voltage()
print("Voltage is ..")
print(voltage)



if reason == pycoproc.WAKE_REASON_ACCELEROMETER:        # purple
    flashLed(led_purple, 2)
else:                                                   # orange
    flashLed(led_orange, 2)



print("Starting...get GPS")


l76 = L76GNSS(py, timeout=60)
coord = l76.coordinates()


if coord == (None, None):
    flashLed(led_red, 3)
    print("Reset chip in 1 seconds ..")
    time.sleep(1)
    machine.reset()
else:
    lat, lon = coord
    flashLed(led_blue, 3)
    gc.collect()
    print("continue")





print("gps is")
print(lat,lon)




print("Continue, Send TCP message")

