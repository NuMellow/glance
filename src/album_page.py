from flask import Flask, render_template, jsonify
import requests
import threading
import time
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib

URL = ''
pyportal_clip_upper_left = (260, 7)
pyportal_clip_lower_right = (740, 367)
glance_size = (480, 800)

def convert_image_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        image_file = io.BytesIO(r.content)
        im = Image.open(image_file)
        im.thumbnail(glance_size)
        im_reduced = im.convert(mode="L", palette=Image.ADAPTIVE, colors=256)
        im.close()
        return im_reduced
    return None

def get_images():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    image_anc = soup.find_all('a', class_='p137Zd')
    count = 0
    for link in image_anc:
        count +=1
        uri = link['href'][1:]
        uri = uri.replace('%3F', '?').replace('%3D', '=')
        actual_img_page = requests.get('https://photos.google.com' + uri)
        more_soup = BeautifulSoup(actual_img_page.content, 'html.parser')
        img_tag = more_soup.find('img')['src']
        image = convert_image_url(img_tag)
        image_name = urllib.parse.quote('static/album/' + str(count) +'.bmp')
        image.save(image_name, 'BMP')