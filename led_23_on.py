import machine, time
from machine import Pin

ds_pin = machine.Pin(23, Pin.OUT)
ds_pin.value(1)
time.sleep(2)
ds_pin.value(0)
