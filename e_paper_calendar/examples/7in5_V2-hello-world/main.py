"""
	Example for 7.5 inch black & white Waveshare E-ink screen, V2
	Run on ESP32
"""

import epaper7in5_V2
from machine import Pin, SPI
from wlan import do_connect
import urequests as requests
import machine

def encode_basic_auth(username, password):
    import ubinascii
    formated = b"{}:{}".format(username, password)
    formated = ubinascii.b2a_base64(formated)[:-1].decode("ascii")
    return {'Authorization' : 'Basic {}'.format(formated)}

def draw_white(pin):
    clear_screen = True
    print("clear_screen: ", clear_screen)
    import gc
    import framebuf
    gc.collect()
    fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
    black = 0
    white = 1
    fb.fill(white)
    e.display_frame(buf)

sleep_time_ms = 60000

try:
    boot_button= Pin(0) # boot
    
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
    buf = bytearray(w * h // 8)
    clear_screen = False
    
    boot_button.irq(trigger=Pin.IRQ_FALLING, handler=draw_white)
    
    
    print("connect wifi")
    # --------------------
    do_connect()
    # --------------------
    
    print("clear_screen: ", clear_screen)
    if clear_screen:
        machine.deepsleep(sleep_time_ms)
    
    import gc
    gc.collect()
    
    print("create frame buffer")
    # use a frame buffer
    # 400 * 300 / 8 = 15000 - thats a lot of pixels
    
    import framebuf
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
    #print('Image light')
    #e.display_frame(hello_world_light)
    
    
    #buf = fb_content.raw
    
    #e.display_frame2(buf, open("framebuffer0.fb"))
    
    print("download image")
    config=open("calendar.txt").read().split(";")[1]
    user=open("calendar.txt").read().split(";")[2]
    pw=open("calendar.txt").read().split(";")[3]
    request=requests.get(config, headers=encode_basic_auth(user, pw))
    fb_content = request.raw
    
    print("draw image")
    if not clear_screen:
        e.display_frame2(fb_content)
    print("done")
    
    import gc
    gc.collect()
except OSError:
    pass    
machine.deepsleep(sleep_time_ms)
    # -------------------- --------------------
