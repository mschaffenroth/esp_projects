import urequests as requests
req = requests.get(open("calendar.txt").read().split(";")[0]).text

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

for i, infos in enumerate(get_events(req)):
    for j, info in enumerate(infos):
        #fb.text(info, 250*j, 20*i, framebuf.MONO_HLSB)
        print(info)
        fb.text(info, 250*j, 20*i, black)

e.display_frame(buf)

