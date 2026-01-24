import logging
import os
import screen_util as screen

from PIL import Image, ImageDraw, ImageFont

class Page:
    
    def __init__(self, debug_mode=False):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.font_dir = os.path.join(self.base_dir, "lib", "fonts")
        self.screen = screen.display
        self.Limage = Image.new('1', (self.screen.height, self.screen.width), 255)
        self.draw = ImageDraw.Draw(self.Limage)
        if debug_mode is True:
            logging.basicConfig(level=logging.DEBUG)

    def draw_page(self):
        pass

    def get_battery(self):
        if screen.has_pi_sugar:
            return self.screen.get_battery()
        else:
            return None
    
    def split_message(self, message):
        NEW_LINE_BREAK = 180

        words = message.split(" ")
        formatted_message = ""
        line = ""
        for word in words:
            if self.draw.textlength(line + ' ' + word) > NEW_LINE_BREAK:
                formatted_message = formatted_message + line + '\n'
                line = ""
            line = line + ' ' + word

        formatted_message = formatted_message + line
        return formatted_message

    def print_error(self, err_msg="something went wrong on the page."):
        font = os.path.join(self.font_dir, "Font.ttc")
        font_error = ImageFont.truetype(font, 24)
        error_message = self.split_message(err_msg)
        
        BOX_PADDING = 10
        box = self.draw.textbbox((50, 400), error_message, font=font_error)
        box = (box[0] - BOX_PADDING,
               box[1] - BOX_PADDING,
               box[2] + BOX_PADDING,
               box[3] + BOX_PADDING)
        
        self.draw.rectangle(box, fill=255, outline="black", width=4)
        self.draw.text((50, 400), error_message, font=font_error, fill=0)

    def run(self):
        try:
            self.screen.initialize()
            self.draw_page()
        except:
            self.print_error()
            raise
        finally:
            self.screen.display(self.Limage)
            self.screen.sleep()