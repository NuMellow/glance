import album_pictures
import os
import random
import screen_util as screen
import sys

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'src', 'static', 'album')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

epd = epd7in5_V2.EPD()
Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Limage)

class Album:

    def initialize(self):
        screen.initialize()

    def draw_photo(self, photo_name):
        bmp = Image.open(os.path.join(picdir, photo_name))
        Limage.paste(bmp, (0, 0))
    
    def get_random_photo(self):
        photo_list = os.listdir(picdir)
        index = random.randint(0, len(photo_list) -1)
        photo = photo_list[index]
        self.draw_photo(photo)

    def download_photos(self):
        album_pictures.get_url()
        album_pictures.get_images()
 
    def run(self):
        self.initialize()
        self.get_random_photo()
        screen.display(Limage)
        screen.sleep()

if __name__ == '__main__':
    album = Album()
    album.run()