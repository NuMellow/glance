#!/usr/bin/python
# -*-
import logging
import os
import screen_util as screen
import traceback

from instructables_page import Instructables
from album_page import Album

logging.basicConfig(level=logging.DEBUG)

def start_page(app):
    page = app()
    page.run()
    return page

def main():
    try:
        page = 0
        if os.path.exists('glance.conf'):
            with open('glance.conf') as config:
                row = config.readline()
                _, value = row.split('=')
                page = int(value)

        if page == 0:
            start_page(Instructables)
        elif page == 1:
            album = start_page(Album)
            album.download_photos()
        else:
            start_page(Instructables)
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        screen.clear_screen()
        exit()

if __name__ == '__main__':
    main()