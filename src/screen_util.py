import logging
import os
import sys
import time

src_dir = os.path.dirname(os.path.realpath(__file__))
glance_dir = os.path.dirname(src_dir)
lib_dir = os.path.join(glance_dir, 'lib')
if os.path.exists(lib_dir):
    sys.path.append(lib_dir)

has_pi_sugar = False
preview_mode = False

if os.path.exists('glance.conf'):
    with open('glance.conf') as config_file:
        for row in config_file:
            key, value = row.split('=')
            value = value.strip()
            if key == 'has_pi_sugar':
                has_pi_sugar = True if value.lower() == 'true' else False
            if key == 'preview_mode':
                preview_mode = True if value.lower() == 'true' else False

class PreviewDisplay:

    height = 480
    width = 800

    def initialize(self):
        pass
    def clear_screen(self):
        pass
    def sleep(self):
        pass
    def wake(self):
        pass
    def close(self):
        pass
    
    def display(self, Limage):
        Limage.show()
    
    def get_battery(self):
        return "100%"

class ePaperDisplay:
    
    if not preview_mode:
        from waveshare_epd import epd7in5_V2

        epd = epd7in5_V2.EPD()

        height = epd.height
        width = epd.width

        def initialize(self):
            logging.info("Initializing screen")
            self.epd.init()
            self.epd.Clear()

        def clear_screen(self):
            logging.info("Clearing screen...")
            self.epd.init()
            self.epd.Clear()
            self.sleep()

        def sleep(self):
            logging.info("Go to sleep...")
            self.epd.sleep()

        def wake(self):
            logging.info("Wake up...")
            self.epd.init()

        def close(self):
            self.epd7in5_V2.epdconfig.module_exit()

        def display(self, Limage):
            self.epd.display(self.epd.getbuffer(Limage))
            time.sleep(2)

        def get_battery(self):
            battery = os.popen('echo "get battery" | nc -q 0 127.0.0.1 8423')
            battery = battery.read().split(':')[1]
            if battery.find(".") < 0:
                value = battery + "%"
            else:
                value = battery[1:battery.index('.')] + '%'
            return value

display = PreviewDisplay() if preview_mode else ePaperDisplay()