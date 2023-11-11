import os
import screen_util as screen

from PIL import Image, ImageDraw, ImageFont

class Page:
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.font_dir = os.path.join(self.base_dir, "fonts")
        self.epd = screen.epd
        self.Limage = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.Limage)

    def draw_page(self):
        pass

    def get_battery(self):
        if screen.has_pi_sugar:
            return screen.get_battery()
        else:
            return None

    def run(self):
        screen.initialize()
        self.draw_page()
        screen.display(self.Limage)
        screen.sleep()