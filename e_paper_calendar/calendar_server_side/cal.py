import os
import sys

import datetime
import os

import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import requests
import numpy as np

def put_framebuffer(filename):
    from webdav3.client import Client
    options = {
     'webdav_hostname': WEBDAV_HOSTNAME,
     'webdav_login':    WEBDAV_LOGIN,
     'webdav_password': WEBDAV_PASSWORD 
    }
    print(options)
    client = Client(options)
    client.verify = False # To not check SSL certificates (Default = True)
    client.upload_sync(remote_path="/Documents/esp_frame/framebuffer0.fb", local_path=filename)
 
def put_file(filename_local, filename_remote):
    from webdav3.client import Client
    options = {
     'webdav_hostname': WEBDAV_HOSTNAME,
     'webdav_login':    WEBDAV_LOGIN,
     'webdav_password': WEBDAV_PASSWORD 
    }
    print(options)
    client = Client(options)
    client.verify = False # To not check SSL certificates (Default = True)
    client.upload_sync(remote_path="/Documents/esp_frame/%s" % filename_remote, local_path=filename_local)
    
def get_events(calendar_url):
    ical = requests.get(calendar_url).text.split("\n")
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
            if entry.startswith("DTSTART"):
                e=entry.split(":")[1].strip()
                if len(e) == 15:
                    cal_entry.append(datetime.datetime.strptime(e, '%Y%m%dT%H%M%S'))
                if len(e) == 16:
                    cal_entry.append(datetime.datetime.strptime(e, '%Y%m%dT%H%M%SZ'))
                if len(e) == 8:
                    cal_entry.append(datetime.datetime.strptime(e, '%Y%m%d'))
            else:
                cal_entry.append(entry.split(":")[1].strip())
        while len(cal_entry) >= 3:
            cal_entry.pop()
    events = sorted(events, key=lambda x: x[0])
    events = filter(lambda x: x[0] > datetime.datetime.now(), events)
    events = ([(x[0].strftime("%a %d.%m.%y %H:%M") if x[0] else x[0], x[1]) for x in events])
    for e in events:
        if len(e) == 1:
            events[events.index(e)] =  [''] + e
    return events

def save_framebuffer(Himage, filename):
    FILE_SPLITS=1
    b=np.asarray(Himage)
    b=np.packbits(b, axis=-1)
    open(filename,"wb").write(b)

def save_image(Himage, filename):
    Himage.save(filename)


CAL_URL=open("config.txt").read().split(";")[0]
WEBDAV_HOSTNAME=open("config.txt").read().split(";")[1].strip()
WEBDAV_LOGIN=open("config.txt").read().split(";")[2].strip()
WEBDAV_PASSWORD=open("config.txt").read().split(";")[3].strip()
picdir = ''

logging.basicConfig(level=logging.DEBUG)

logging.info("init and Clear")

font34 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 34)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
# Drawing on the Horizontal image
logging.info("1.Drawing on the Horizontal image...")
Himage = Image.new('1', (800, 480), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Himage)
MAX_ROWS=12
events = get_events(CAL_URL)[:MAX_ROWS]
events = [("Termine", "")] + events
TOP_MARGIN=20
LEFT_MARGIN=10
ROW_WIDTH=200
BOX_WIDTH=470
BOX_HEIGHT=30
ROW_HEIGHT=30
for i, infos in enumerate(events):
    #print(infos)
    for j, info in enumerate(infos):
        if len(info) > 25:
            info = info[:25] + "..."
        draw.text((LEFT_MARGIN+25+ROW_WIDTH*j, TOP_MARGIN+ROW_HEIGHT*i), info, font = font18, fill = 0)
        draw.rectangle([(LEFT_MARGIN, TOP_MARGIN), (10+j*BOX_WIDTH, TOP_MARGIN+25+i*BOX_HEIGHT)])

TITLE="Michelles Kalender"
import requests
corona=requests.get("https://www.lgl.bayern.de/gesundheit/infektionsschutz/infektionskrankheiten_a_z/coronavirus/karte_coronavirus/csv.htm?tabelle=tabelle4").text
sevenday="7 Tages Inzidenz: " + [x.split(";")[4] for x in corona.split("\n") if x.startswith("Amberg-Sulzbach")][0]
draw.text((500, 10), TITLE, font = font34, fill = 0)
draw.text((500, 50), str(datetime.datetime.now().strftime("%a %d.%m.%y  %H:%M")), font = font24, fill = 0)
draw.text((500, 80), sevenday, font = font18, fill = 0)

bmp = Image.open(os.path.join(picdir, 'may.jpg'))
Himage.paste(bmp, (500,120))

HOUR = datetime.datetime.now().time().hour
GREETING = ""
if HOUR >= 0 and HOUR <= 6:
    GREETING = "Gute Nacht"
if HOUR > 6 and HOUR <= 10:
    GREETING = "Guten Morgen"
if HOUR > 10 and HOUR <= 11:
    GREETING = "Guten Tag"
if HOUR > 11 and HOUR <= 13:
    GREETING = "Guten Mittag"
if HOUR > 13 and HOUR <= 17:
    GREETING = "Guten Nachmittag"
if HOUR > 17 and HOUR <= 20:
    GREETING = "Guten Abend"
if HOUR > 20 and HOUR <= 23:
    GREETING = "Gute Nacht"
draw.text((240, 410), GREETING, font = font34, fill = 0)

save_framebuffer(Himage, "files/framebuffer0.fb")
save_image(Himage, "files/calendar.jpg")
#put_file("calendar.jpg", "calendar.jpg")
#put_framebuffer("framebuffer0.fb")
