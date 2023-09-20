#!/usr/bin/python
# -*-
import logging
import os
import screen_util as screen
import time
import traceback

from instructables_page import Instructables
from album_page import Album

logging.basicConfig(level=logging.DEBUG)


def check_instructables():
    contests = instructables_app.update_contests()

def main():
    try:
        page = 0
        if os.path.exists('glance.conf'):
            config = open('glance.conf', 'r')
            page = int(config.readline().split('=')[1])
            config.close()

        if page == 0:
            instructables = Instructables()
            instructables.run()
        elif page == 1:
            album = Album()
            album.download_photos()
            album.run()
        else:
            instructables = Instructables()
            instructables.run()

        time.sleep(2)
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        screen.clear_screen()
        exit()

    while True:
        try:
            continue
            #check for new data
        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            screen.clear_screen()
            exit()

if __name__ == '__main__':
    main()