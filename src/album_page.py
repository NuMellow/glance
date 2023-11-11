import album_pictures
import os
import random

from page import Page
from PIL import Image, ImageFont

class Album(Page):

    def __init__(self):
        super().__init__()
        self.pic_dir = os.path.join(self.base_dir, "src", "static", "album")
        self.font18 = ImageFont.truetype(os.path.join(self.font_dir, "Font.ttc"), 18)

    def draw_photo(self, photo_name):
        bmp = Image.open(os.path.join(self.pic_dir, photo_name))
        self.Limage.paste(bmp, (0, 0))
    
    def get_random_photo(self):
        photo_list = os.listdir(self.pic_dir)
        index = random.randint(0, len(photo_list) -1)
        photo = photo_list[index]
        self.draw_photo(photo)

    def download_photos(self):
        album_pictures.get_url()
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