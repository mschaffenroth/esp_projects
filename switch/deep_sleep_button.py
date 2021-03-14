import machine, time
from machine import Pin
import time
import esp32
from wlan import do_connect
import hue

global active
active=False
P1=32
P2=33
ds_pin1 = machine.Pin(P1, Pin.OUT, pull=machine.Pin.PULL_HOLD)
ds_pin1.value(1)
ds_pin2 = machine.Pin(P2, Pin.IN)
ds_pin2.value(0)
ds_pin2 = machine.Pin(P2, machine.Pin.IN)

def hue_show():
       h = hue.Bridge()
       h.setLight(2, bri=50, transitiontime=1)
       time.sleep(1)
       h.setLight(2, bri=254, transitiontime=1)
       time.sleep(1)
       h.setLight(2, bri=50, transitiontime=1)
       time.sleep(1)
       h.setLight(2, bri=254, transitiontime=1)

def callback(p):
    global active
    if not active:
       do_connect()

       active=True
       print(active)
       print("Switch activated!")
       time.sleep(1)
       active=False
       
       hue_show()
    else:
        print(active)

#ds_pin2.irq(trigger=Pin.IRQ_FALLING, handler=callback)

#time.sleep(1)

callback(None)

esp32.wake_on_ext0(pin = ds_pin2, level = esp32.WAKEUP_ALL_LOW)

machine.deepsleep()

#while True:
#    pass
    #v=ds_pin1.value() 
    #print("32: ", v)
    #v2=ds_pin2.value() 
#   print("33: ", v2)
