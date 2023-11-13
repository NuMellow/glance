import logging
import os
import screen_util as screen

from PIL import Image, ImageDraw, ImageFont

class Page:
    
    def __init__(self, debug_mode=False):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.font_dir = os.path.join(self.base_dir, "lib", "fonts")
        self.epd = screen.epd
        self.Limage = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.Limage)
        if debug_mode is True:
            logging.basicConfig(level=logging.DEBUG)

    def draw_page(self):
        pass

    def get_battery(self):
        if screen.has_pi_sugar:
            return screen.get_battery()
        else:
            return None
    
    def print_error(self):
        font = os.path.join(self.font_dir, "Font.ttc")
        font_error = ImageFont.truetype(font, 24)
        error_message = "Something went wrong on the page."
        self.draw.rectangle([20, 374, 460, 450], fill=255, outline="black", width=4)
        self.draw.text((50, 400), error_message, font=font_error, fill=0)

    def run(self):
        try:
            screen.initialize()
            self.draw_page()
        except:
            self.print_error()
        finally:
            screen.display(self.Limage)
            screen.sleep()