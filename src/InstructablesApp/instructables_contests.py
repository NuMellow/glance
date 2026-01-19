"""
Instructables Contest Scraper and Web Server
by James Matlock
Feb 2021

This project implements a simple web server that provides a REST API to
peripheral devices like the Adafruit MagTag, PyPortal, or Matrix Portal.
The REST API provides information about the latest Instructables contests.

Basically there are three links served up by this web server:
- http://127.0.0.1:5000/ - This page just shows the information collected.
- http://127.0.0.1:5000/api/v1/contests - JSON data about the contests
- http://127.0.0.1:5000/api/v1/meta - JSON data about the server itself

By default, the server responds on all IP addresses at port 5000 on the
host computer.

Webscraper updated by NuMellow Jan 2026
"""
import requests
import threading
import time
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image
import io
from dataclasses import dataclass
import asyncio
import urllib
import os

from playwright.async_api import async_playwright

URL = "https://www.instructables.com/contest/"
UPDATE_EVERY = 120  # Number of minutes between updates from Instructables

crop_upper_left = (260, 0)
crop_lower_right = (520, 200)
pyportal_size = (320, 240)
glance_size = (100, 75)


@dataclass
class Contest:
    name: str
    date: str
    days_until: int
    contest_uri: str
    contest_graphic_uri: str
    entry_count: str


@dataclass
class Contests:
    contests: list


contests = Contests([])


@dataclass
class Meta:
    current_time: str
    last_update: str
    last_update_dt: datetime
    next_update_minutes: int
    contest_count: int


meta = Meta('', '', datetime.now(), UPDATE_EVERY, 0)


def convert_image_url_to_small(url):
    r = requests.get(url)
    if r.status_code == 200:
        image_file = io.BytesIO(r.content)
        im = Image.open(image_file)
        im_reduced = im.crop((*crop_upper_left, *crop_lower_right)) \
            .resize(glance_size)
        im_reduced = im_reduced.convert(mode="L", palette=Image.ADAPTIVE, colors=256)
        im.close()
        return im_reduced
    return None

async def update_contests():
    CONTEST_CARD_CLASS = "._contestCard_1ezpy_1"
    CONTEST_DETAILS_CLASS = "._artifakt_element_6jn54_2"
    INSTRUCTABLES_SITE = "https://www.instructables.com"
    IMG_DIRECTORY = "InstructablesApp/res/contestImg/"
    TIMEOUT = 120000 # 2 minutes

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True) # set headless=False to see the UI
        page = await browser.new_page()
        page.set_default_timeout(TIMEOUT)
        await page.goto("https://www.instructables.com/contest/")
        contest_cards = page.locator(CONTEST_CARD_CLASS)
        contests = []
        contest_card_list = []
        while len(contest_card_list) == 0:
            contest_card_list = await contest_cards.all()

        if not os.path.exists(IMG_DIRECTORY):
            os.mkdir(IMG_DIRECTORY)

        for contest_card in contest_card_list:
            link_elements = contest_card.get_by_role("link")
            link_elements_list =  await link_elements.all()
            contest_href = await link_elements_list[0].get_attribute("href")

            contest_img = contest_card.get_by_role("img")
            contest_name = await contest_img.get_attribute("alt")

            contest_graphic_uri = await contest_img.get_attribute("src")
            image = convert_image_url_to_small(contest_graphic_uri)
            image_fname =  urllib.parse.quote(IMG_DIRECTORY
                                            + contest_name.strip()
                                            .replace("#", "")
                                            .replace("&", "")
                                            + '.bmp')
            image.save(image_fname, 'BMP')

            contest_details_element = contest_card.locator(CONTEST_DETAILS_CLASS).last
            contest_details_text = await contest_details_element.inner_text()
            contest_details_list = contest_details_text.split("|")

            contest_deadline = contest_details_list[0].strip("Closes ")
            days_until = -1  # Contest no longer show year so cannot easily determine days left
                             # But actually, the actual contest page has the date in full so its
                             # possible to bring it back. Out of scope for this ticket though

            contest_uri = urllib.parse.quote(INSTRUCTABLES_SITE + contest_href, safe='/:')
            
            entry_count = contest_details_list[1].split(",")[1]

            contest_entry = Contest(contest_name, contest_deadline,
                                    days_until, contest_uri,
                                    image_fname, entry_count)
            contests.append(contest_entry)

        await browser.close()
        return contests

async def setup_server(meta_data, contests_data):
    async def contest_update(meta_data, contests_data):
        print('Updating contest data')
        contests_data.contests = await update_contests()
        meta_data.last_update_dt = datetime.now()
        meta_data.last_update = str(meta_data.last_update_dt.strftime('%Y-%m-%d %H:%M'))
        print(f'Contest data loaded: {meta_data.last_update}')
        meta_data.contest_count = len(contests_data.contests)

    await contest_update(meta_data, contests_data)

async def download_contests():
    await setup_server(meta, contests)

if __name__ == '__main__':
    asyncio.run(setup_server(meta, contests))
