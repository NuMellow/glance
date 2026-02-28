import datetime
import os
import random

from page import Page
from AlbumApp import album_pictures
from PIL import Image, ImageFont

class Album(Page):

    CONFIG_FILE = 'AlbumApp/album.conf'
    def __init__(self):
        super().__init__(debug_mode=True)
        self.pic_dir = os.path.join(self.base_dir, "src", "AlbumApp", "res", "album")
        self.font18 = ImageFont.truetype(os.path.join(self.font_dir, "Font.ttc"), 18)
        self.schedule_download_enabled = False
        self.download_day= ''
        self.should_download=True
        self.pre_downloaded = False
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
        bmp = album_pictures.resize_image(os.path.join(self.pic_dir, photo_name))
        self.Limage.paste(bmp, (0, 0))
    
    def get_random_photo(self):
        photo_list = os.listdir(self.pic_dir)
        if len(photo_list) > 0:
            index = random.randint(0, len(photo_list) -1)
            photo = photo_list[index]
            self.draw_photo(photo)
        else:
            self.print_error("Album is empty. If download is enabled, check that scheduled download is off or the same day as today. Turn glance off and on to retry.")

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

    def download_if_empty(self):
        album_does_not_exist =  not os.path.exists(self.pic_dir)
        album_exists_but_is_empty = os.path.exists(self.pic_dir) and not len(os.listdir(self.pic_dir)) > 0

        if album_does_not_exist:
            os.mkdir(self.pic_dir)
           
        if album_does_not_exist or album_exists_but_is_empty:   
            self.download_photos()
            self.pre_downloaded = True

    def draw_page(self):
        self.download_if_empty()
        self.get_random_photo()
        self.draw_battery()
 
    def run(self):
        return super().run()

if __name__ == '__main__':
    album = Album()
    album.run()