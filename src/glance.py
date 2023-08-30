#!/usr/bin/python
# -*-
import logging
import screen_util as screen
import time
import traceback

from instructables_page import Instructables

logging.basicConfig(level=logging.DEBUG)


def check_instructables():
    contests = instructables_app.update_contests()

def main():
    try:
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