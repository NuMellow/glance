import album_pictures
import datetime
import os
import random

from page import Page
from PIL import Image, ImageFont

class Album(Page):

    CONFIG_FILE = 'album.conf'
    def __init__(self):
        super().__init__(debug_mode=True)
        self.pic_dir = os.path.join(self.base_dir, "src", "static", "album")
        self.font18 = ImageFont.truetype(os.path.join(self.font_dir, "Font.ttc"), 18)
        self.schedule_download_enabled = False
        self.download_day= ''
        self.should_download=True
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE) as config:
                for row in config:
                    key, value = row.split('=')
                    value = value.strip()
                    if key == 'schedule_download':
                        self.schedule_download_enabled = False if value.lower() == 'false' else True
                    elif key =='download_day':
                        self.download_day = value
                    elif key == 'should_download':
                        self.should_download = False if value.lower() == 'false' else True

    def draw_photo(self, photo_name):
        bmp = Image.open(os.path.join(self.pic_dir, photo_name))
        self.Limage.paste(bmp, (0, 0))
    
    def get_random_photo(self):
        if not os.path.exists(self.pic_dir):
            os.mkdir(self.pic_dir)
            self.download_photos()

        photo_list = os.listdir(self.pic_dir)
        if len(photo_list) > 0:
            index = random.randint(0, len(photo_list) -1)
            photo = photo_list[index]
            self.draw_photo(photo)
        else:
            self.print_error("Album is empty")

    def download_photos(self):
        if self.should_download:
            album_pictures.get_url()
            if self.schedule_download_enabled:
                date = datetime.datetime.now()
                day = date.strftime("%A").lower()
                
                if day == self.download_day.lower():
                    album_pictures.get_images()
            else:
                album_pictures.get_images()

    def draw_battery(self):
        battery = self.get_battery()
        if battery is not None:
            self.draw.rectangle([420, 775, 470, 800], fill=255)
            self.draw.text((429, 780), battery, font=self.font18, fill=0)

    def draw_page(self):
        self.get_random_photo()
        self.draw_battery()
 
    def run(self):
        return super().run()

if __name__ == '__main__':
    album = Album()
    album.run()