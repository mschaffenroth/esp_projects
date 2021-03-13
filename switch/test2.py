from wlan import do_connect
import hue

do_connect()
h = hue.Bridge()

h.getLights()

