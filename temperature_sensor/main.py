from bme280_float import BME280
import machine
from wlan import do_connect
SLEEP_SECONDS=600
SENDING_BATCH=1


import urequests as requests
def _send_to_prometheus(urls, job_name, metric_name, metric_value, dimensions, time):
    dim = ''
    headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
    #for key, value in dimensions.items():
    #    dim += '/%s/%s' % (key, value)
    for url in urls:
        url__ = 'http://%s/metrics/job/%s%s' % (url, job_name, dim)
        print("url: " + url__)
        #data = '%s %s\n' % (metric_name, metric_value)
        import ujson
        data = '%s %s\n' % (metric_name, metric_value)
        print("data: " + data)
        requests.post(url__,
                      data=data, headers=headers)

def setup_i2c():
        #
        # this script assumes the default connection of the I2C bus
        # On pycom devices that is P9 = SDA, P10 = scl
        #
        
        scl_pin_id = 23
        sda_pin_id = 22
        scl = machine.Pin(scl_pin_id)
        sda = machine.Pin(sda_pin_id)
        i2c = machine.SoftI2C(scl=scl,
                            sda = sda, freq=10000)
        return i2c

def measure_battery_level():
    from machine import ADC
    
    p1 = machine.Pin(25, machine.Pin.OUT)
    p1.value(1)
    adc = ADC(machine.Pin(34))          # create ADC object on ADC pin
    v=adc.read()                  # read value, 0-4095 across voltage range 0.0v - 1.0v
    print("measure: ", v)
    return v

def send_batch(value, volt):
    # send sensor values if batch completed
 
    wlan = do_connect()
    #wlan=open("wlan.txt").read()[:-1].split(",")
    #print(wlan)
    rtc = machine.RTC();
    if wlan:
                        # send them to prometheus
        _send_to_prometheus([wlan[2]], "weather", "temperature", value[0], dimensions={}, time=rtc.datetime())
        _send_to_prometheus([wlan[2]], "weather", "air_pressure", value[1], time=rtc.datetime(), dimensions={})
        _send_to_prometheus([wlan[2]], "weather", "humidity", value[2], dimensions={}, time=rtc.datetime())
        _send_to_prometheus([wlan[2]], "weather", "volt", volt, dimensions={}, time=rtc.datetime())

def decode_memory():
   rtc = machine.RTC();
   mem = rtc.memory()

   if mem:
       arr = mem.decode().split("\n")
       values = [arr_elem.split(";") for arr_elem in arr if not arr_elem is None]
   else:
       values = []
   return values

def encode_memory(values):
   # save values to clock memory to survive deep sleep
   values_string = ""
   if values is not None:
     values_string = ";".join(values)
   rtc = machine.RTC()
   rtc.memory(values_string.encode())

def calc_mean(values):
     # calc mean of the sensor values
     if len(values) > 1:
         value = tuple(float(x) + float(y) for x,y in zip(*values))
         value = list(map(lambda y: y/3, value))
         value = list(map(str, value))
     if len(values) == 1:
         value = values[0]
     return value

while True:
    try:
        volt=measure_battery_level()
        # After leaving deepsleep it may be necessary to un-hold the pin explicitly (e.g. if it is an output pin) 
        # See https://docs.micropython.org/en/latest/esp32/quickref.html#deep-sleep-mode
        p1 = machine.Pin(4, machine.Pin.OUT, None)
        
        # enable power for temperatuer sensor
        p2 = machine.Pin(19, machine.Pin.OUT)
        p2.value(1)
        
        values = decode_memory()

        i2c = setup_i2c() 
       
        bme = BME280(i2c=i2c)
        print(bme.values)
        
        # disable power for temperatuer sensor
        #p2.value(0)

        cleaned_values = (bme.values[0].replace("C", ""), bme.values[1].replace("hPa", ""), bme.values[2].replace("%", ""))
        values.append(cleaned_values)
        print("calc mean")
        value = calc_mean(values)
        print(len(values))
        if len(values) == SENDING_BATCH:
           print("send batch")
           send_batch(value, volt)
           value = None
    
        encode_memory(value)
        # free some memory and collect information how much we use
        import gc
        gc.collect()
        print(gc.mem_free())
    except OSError as e:
        print("Error", str(e))


    try:
        p1 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_HOLD)
        machine.deepsleep(SLEEP_SECONDS*1000)
    except OSError as e:
        print("Error", str(e))
