import logging
import os
import sys
import time

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()

def initialize():
    logging.info("Initializing screen")
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

def clear_screen():
    logging.info("Clearing screen...")
    epd.init()
    epd.Clear()

    sleep()

def sleep():
    logging.info("Go to sleep...")
    epd.sleep()

def wake():
    Logging.info("Wake up...")
    epd.init()

def close():
    epd7in5_V2.epdconfig.module_exit()

def display(Limage):
    epd.display(epd.getbuffer(Limage))
    time.sleep(2)
    epd.sleep()

def get_battery():
    battery = os.popen('echo "get battery" | nc -q 0 127.0.0.1 8423')
    battery = battery.read()
    value = battery[8:battery.index('.')] + '%'
    return value

