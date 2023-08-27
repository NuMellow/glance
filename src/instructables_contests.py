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
"""
from flask import Flask, render_template, jsonify
import requests
import threading
import time
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image, ImageDraw
import io
from dataclasses import dataclass
import urllib

URL = "https://www.instructables.com/contest/"
UPDATE_EVERY = 120  # Number of minutes between updates from Instructables
# UPDATE_EVERY = 15  # TEST VALUE REMOVE

app = Flask(__name__)
pyportal_clip_upper_left = (260, 7)
pyportal_clip_lower_right = (740, 367)
pyportal_size = (320, 240)


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
        im_reduced = im.crop((*pyportal_clip_upper_left, *pyportal_clip_lower_right)) \
            .resize(pyportal_size)
        draw = ImageDraw.Draw(im_reduced)
        draw.rectangle([(20, 195), (300, 235)], fill=(0, 0, 0), outline=(255, 255, 255))
        im_reduced = im_reduced.convert(mode="P", palette=Image.ADAPTIVE, colors=256)
        im.close()
        return im_reduced
    return None


def update_contests():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='cur-contests')
    contest_banners = results.find_all('div', class_='contest-banner')

    contests = []
    for contest in contest_banners:
        contest_name = contest.find('img')['alt']
        contest_deadline = contest.find('span', class_='contest-meta-deadline')['data-deadline']
        deadline = datetime.fromisoformat(contest_deadline)
        if deadline < datetime.now():
            continue
        deadline_formatted = deadline.strftime('%B %d')
        delta = deadline - datetime.now()
        days_until = delta.days
        contest_uri = urllib.parse.quote('https://www.instructables.com' + contest.find('a')['href'], safe='/:')
        contest_graphic_uri = contest.find('img')['src']
        image = convert_image_url_to_small(contest_graphic_uri)
        image_fname = urllib.parse.quote('static/contestImg/'
                                         + contest_name.replace(" ", "")
                                         .replace("#", "")
                                         .replace("&", "")
                                         + '.bmp')
        image.save(image_fname, 'BMP')
        entry_count = contest.find_all('span', class_='contest-meta-count')[1].text
        contest_entry = Contest(contest_name, deadline_formatted,
                                days_until, contest_uri,
                                image_fname, entry_count)
        contests.append(contest_entry)
    return contests


def setup_server(meta_data, contests_data):
    def contest_update(meta_data, contests_data):
        print('Updating contest data')
        contests_data.contests = update_contests()
        meta_data.last_update_dt = datetime.now()
        meta_data.last_update = str(meta_data.last_update_dt.strftime('%Y-%m-%d %H:%M'))
        print(f'Contest data loaded: {meta_data.last_update}')
        meta_data.contest_count = len(contests_data.contests)

    def contest_update_job(meta_data, contests_data):
        while True:
            print(f'Waiting {UPDATE_EVERY} minutes for next contest update')
            time.sleep(UPDATE_EVERY * 60)  # sleep for two hours
            contest_update(meta_data, contests_data)

    contest_update(meta_data, contests_data)
    thread = threading.Thread(target=contest_update_job, args=(meta_data, contests_data,), daemon=True)
    thread.start()


@app.route('/')
def index():
    return render_template('index.html', contests=contests.contests)


@app.route('/api/v1/contests', methods=['GET'])
def get_contests():
    return jsonify(contests.contests)


@app.route('/api/v1/meta', methods=['GET'])
def get_meta():
    meta.current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    meta.next_update_minutes = UPDATE_EVERY - ((datetime.now() - meta.last_update_dt).seconds // 60)
    return jsonify(meta)


setup_server(meta, contests)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
