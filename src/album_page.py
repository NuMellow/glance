import album_pictures
import os
import random
import screen_util as screen
import sys

from PIL import Image, ImageDraw, ImageFont

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'src', 'static', 'album')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

epd = screen.epd
Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Limage)
font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)

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

    def draw_battery(self):
        if screen.has_pi_sugar:
            battery = screen.get_battery()
            draw.rectangle([420, 775, 470, 800], fill=255)
            draw.text((429, 780), battery, font=font18, fill=0)
 
    def run(self):
        self.initialize()
        self.get_random_photo()
        self.draw_battery()
        screen.display(Limage)
        screen.sleep()

if __name__ == '__main__':
    album = Album()
    album.run()