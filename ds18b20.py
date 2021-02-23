# Complete project details at https://RandomNerdTutorials.com

import machine, onewire, ds18x20, time

def get_temperature(pin):
    ds_pin = machine.Pin(pin, machine.Pin.PULL_UP)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    
    roms = ds_sensor.scan()
    print('Found DS devices: ', roms)
    
    while True:
      ds_sensor.convert_temp()
      time.sleep_ms(750)
      for rom in roms:
        print(rom)
        print(ds_sensor.read_temp(rom))
        break
      break
      time.sleep(5)

get_temperature(25)

