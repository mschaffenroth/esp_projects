"""
	Example for 7.5 inch black & white Waveshare E-ink screen, V2
	Run on ESP32
"""

import epaper7in5_V2
from machine import Pin, SPI
from wlan import do_connect
import urequests as requests

# SPIV on ESP32
sck = Pin(18) # CLK
miso = Pin(19) # 
mosi = Pin(23) # DIN 
dc = Pin(32) # DC
cs = Pin(33) # Chip Select
rst = Pin(19) # RST
busy = Pin(35) # BUSY
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)

e = epaper7in5_V2.EPD(spi, cs, dc, rst, busy)
e.init()

w = 800
h = 480
x = 0
y = 0

# --------------------

# use a frame buffer
# 400 * 300 / 8 = 15000 - thats a lot of pixels
import framebuf
buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
black = 0
white = 1
fb.fill(white)

# --------------------

# write hello world with black bg and white text
#from image_dark import hello_world_dark
#from image_light import hello_world_light
#print('Image dark')
#bufImage = hello_world_dark
#fbImage = framebuf.FrameBuffer(bufImage, 128, 296, framebuf.MONO_HLSB)
#fb.blit(fbImage, 20, 2)
#bufImage = hello_world_light
#fbImage = framebuf.FrameBuffer(bufImage, 128, 296, framebuf.MONO_HLSB)
#fb.blit(fbImage, 168, 2)
#e.display_frame(buf)

# --------------------

# write hello world with white bg and black text
print('Image light')
#e.display_frame(hello_world_light)

# --------------------
do_connect()
req = requests.get("https://calendar.google.com/calendar/ical/ekghglkiv8h0rs2nhek2pfmhhc%40group.calendar.google.com/private-7ef134bce7ffb74ad8122a9ae3aa7bbd/basic.ics").text

def get_events(text):
    ical = text.split("\n")
    type_ = ""
    events = []
    cal_entry = []
    for entry in ical:
        if entry.startswith("BEGIN:VEVENT"):
            type_ = "event"
        if entry.startswith("END:VEVENT"):
            type_ = ""
            events.append(cal_entry)
            cal_entry = []

        if type_ == "event" and entry.startswith("DTSTART") or entry.startswith("SUMMARY"):
        #if entry.startswith("DTSTART") or entry.startswith("SUMMARY"):
        #    print(entry)
            cal_entry.append(entry.split(":")[1])
    return events

events = get_events(req)

#for i, infos in enumerate(get_events(req)):
#    for j, info in enumerate(infos):
#        #fb.text(info, 250*j, 20*i, framebuf.MONO_HLSB)
#        print(info)
#        fb.text(info, 250*j, 20*i, black)

#e.display_frame(buf)

#fb_content = requests.get("https://nextcloud.mschaffenroth.de/s/GarQJRJ9Y8qTjbP/download")
#buf = bytearray(w * h // 8)
#buf = fb_content.raw

e.display_frame2("frame_buffer.fb", "frame_buffer2.fb", "frame_buffer3.fb","frame_buffer4.fb", w, h, framebuf.MONO_HLSB)

# -------------------- --------------------
