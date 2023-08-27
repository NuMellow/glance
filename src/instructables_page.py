import instructables_contests as ins_contests
import logging
import os
import sys
import screen_util as screen
import traceback

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)
epd = epd7in5_V2.EPD()
Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Limage)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

FIRST_ITEM_VPOS = 60
ITEM_LEFT_MARGIN = 30
ITEM_HEIGHT = 75
ITEM_TOP_MARGIN = 30
TITLE_HPOS = 150

class Instructables:

    def initialize(self):
        screen.initialize()

    def draw_speech_bubble(self):
        draw.line((15, 20, 15, 620), fill=0, width=2)
        draw.line((465, 20, 465, 620), fill=0, width=2)
        draw.arc((15, 15, 25, 25), 180, 270, fill=0, width=2)
        draw.arc((15, 615, 25, 625), 90, 180, fill=0, width=2)
        draw.line((20, 15, 460, 15), fill=0, width=2)
        draw.line((20, 625, 460, 625), fill=0, width=2)
        draw.arc((455, 15, 465, 25), 270, 360, fill=0, width=2)
        draw.arc((455, 615, 465, 625), 0, 90, fill=0, width=2)

    def draw_battery(self):
        battery = screen.get_battery()
        draw.text((429, 780), battery, font=font18, fill=0)

    def draw_layout(self):
        print("Drawing instrucatables layout...")
        bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
        Limage.paste(bmp, (15, 700))
        draw.text((150, 15), 'Instructables', font=font24, fill=0)
        self.draw_speech_bubble()
        self.draw_battery()
        screen.display(Limage)

    def place_contest_items(self):
        arrange = FIRST_ITEM_VPOS
        for item in ins_contests.contests.contests:
            if arrange <= 545:
                days_until_text = "Days left: " + str(item.days_until)
                pic = Image.open(item.contest_graphic_uri)
                Limage.paste(pic, (ITEM_LEFT_MARGIN, arrange))
                draw.text((TITLE_HPOS, arrange), item.name, font=font18, fill=0)
                draw.text((TITLE_HPOS, arrange + 40), days_until_text, font=font18, fill=0)
                arrange += ITEM_HEIGHT + ITEM_TOP_MARGIN
            else:
                break

    def draw_contests(self):
        self.place_contest_items()
        screen.initialize()
        screen.display(Limage)

    def run(self):
        self.initialize()
        self.draw_layout()
        self.draw_contests()
