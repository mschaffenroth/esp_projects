import machine
from machine import Pin
from machine import ADC
import time
from time import sleep
from HC_SR04 import HCSR04

p2=Pin(34)
moisture = ADC(p2)
moisture.atten(moisture.ATTN_11DB)


while True:
    sensor = HCSR04(trigger_pin=33, echo_pin=26,echo_timeout_us=1000000)
    distance = sensor.distance_cm()
    print("dist: ", distance)
    moisture_value = moisture.read()
    print(moisture_value)
    sleep(3)



