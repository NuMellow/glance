import os
import screen_util as screen
import sys

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

epd = epd7in5_V2.EPD()
Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Limage)

class Frame:

    def initialize(self):
        screen.initialize()

    def draw_photo(self):
        bmp = Image.open(os.path.join(picdir, 'MeganPicFrame.bmp'))
        Limage.paste(bmp, (0, 129))

    def run(self):
        self.initialize()
        self.draw_photo()
        screen.display(Limage)
        screen.sleep()