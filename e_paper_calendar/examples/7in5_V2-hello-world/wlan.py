import machine
def do_connect():
    import network
    # enable station interface and connect to WiFi access point
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    if not nic.isconnected():
        print('connecting to network...')
        wlan=open("wlan.txt").read()[:-1].split(",")
        print(wlan)
        print(wlan[0])
        print(wlan[1])
        nic.connect(wlan[0], wlan[1])
        i=0
        TOO_MANY_RETRIES=20000
        import utime
        while not nic.isconnected() and i < TOO_MANY_RETRIES:
           i+=1
           utime.sleep_ms(1)
        if i < TOO_MANY_RETRIES:
           print("connected")
        else:
            print("connect failed!")
        return wlan
    return None
    # now use sockets as usual

