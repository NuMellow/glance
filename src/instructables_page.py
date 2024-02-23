import instructables_contests as ins_contests
import os

from page import Page
from PIL import Image, ImageFont

class Instructables(Page):

    FIRST_ITEM_VPOS = 60
    ITEM_LEFT_MARGIN = 30
    ITEM_HEIGHT = 75
    ITEM_TOP_MARGIN = 30
    TITLE_HPOS = 150

    def __init__(self):
        super().__init__()
        self.pic_dir = os.path.join(self.base_dir, "pic")
        font = os.path.join(self.font_dir, "Font.ttc")
        self.font_heading = ImageFont.truetype(font, 24)
        self.font_normal = ImageFont.truetype(font, 18)
        self.font_small = ImageFont.truetype(font, 12)
        ins_contests.download_contests()

    def truncate_long_name(name, truncate_length=32):
        truncated_name = name

        if len(name) > truncate_length:
            truncated_name = name[:truncate_length] + "..."
        
        return truncated_name

    def draw_speech_bubble(self):
        self.draw.line((15, 20, 15, 620), fill=0, width=2)
        self.draw.line((465, 20, 465, 620), fill=0, width=2)
        self.draw.arc((15, 15, 25, 25), 180, 270, fill=0, width=2)
        self.draw.arc((15, 615, 25, 625), 90, 180, fill=0, width=2)
        self.draw.line((20, 15, 460, 15), fill=0, width=2)
        self.draw.line((20, 625, 180, 625), fill=0, width=2)
        self.draw.line((200, 625, 460, 625), fill=0, width=2)
        self.draw.arc((455, 15, 465, 25), 270, 360, fill=0, width=2)
        self.draw.arc((455, 615, 465, 625), 0, 90, fill=0, width=2)
        self.draw.line((180, 625, 180, 645),fill=0, width=2)
        self.draw.line((180, 645, 200, 625), fill=0, width=2)

    def draw_battery(self):
        battery = self.get_battery()
        if battery is not None:
            self.draw.text((429, 780), battery, font=self.font_normal, fill=0)

    def draw_layout(self):
        print("Drawing instrucatables layout...")
        bmp = Image.open(os.path.join(self.pic_dir, 'Megan.bmp'))
        self.Limage.paste(bmp, (15, 650))
        self.draw.text((150, 15), 'Instructables', font=self.font_heading, fill=0)
        self.draw_speech_bubble()
        self.draw_battery()

    def draw_contests(self):
        arrange = self.FIRST_ITEM_VPOS
        for item in ins_contests.contests.contests:
            if arrange <= 545:
                name = self.truncate_long_name(item.name)
                days_until_text = "Days left: " + str(item.days_until)
                entries = "Entries: " + str(item.entry_count)
                pic = Image.open(item.contest_graphic_uri)
                self.Limage.paste(pic, (self.ITEM_LEFT_MARGIN, arrange))
                self.draw.text((self.TITLE_HPOS, arrange), name, font=self.font_normal, fill=0)
                self.draw.text((self.TITLE_HPOS, arrange + 40), days_until_text, font=self.font_small, fill=0)
                self.draw.text((300, arrange + 40), entries, font=self.font_small, fill=0)
                arrange += self.ITEM_HEIGHT + self.ITEM_TOP_MARGIN
            else:
                break

    def draw_page(self):
        self.draw_layout()
        self.draw_contests()

    def run(self):
        return super().run()

if __name__ == "__main__":
    instructables_app  = Instructables()
    instructables_app.run()