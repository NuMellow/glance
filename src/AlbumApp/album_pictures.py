from zipfile import ZipFile
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps
import urllib
import os

URL = ''
glance_size = (480, 800)

def get_url():
    global URL
    f = open('album.conf', 'r')
    url = f.readline().split('=')[1]
    URL = format_url(url)
    f.close()

def format_url(url):
    if url[-1] == "\n":
        url = url[:-1]
    return url

def resize_image(image_file):
    im = Image.open(image_file)
    im = ImageOps.fit(im, glance_size)
    im_reduced = im.convert(mode="L", palette=Image.ADAPTIVE, colors=256)
    im.close()
    return im_reduced

def get_images():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    print('Got soup...')
    all_scripts = soup.find_all('script')
    download_link = ''
    print('Reading the script...')
    for script in all_scripts:
        items = str(script).split(',')
        for i in items:
            if 'https://video-downloads' in i:
                download_link = i.replace('"', '')
                print('YES! ' + i)
                break

    if len(download_link) > 0:
        zip_name = 'images.zip'
        print('Download the zip...')
        urllib.request.urlretrieve(download_link, zip_name)
        
        if not os.path.exists('res/album'):
            os.mkdir('res/album')
        
        with ZipFile(zip_name, 'r') as zip:
            image_names = zip.namelist()
            print('Grabbing the photos...')
            for image in image_names:
                bmp_name = image.split('.')[0] + '.bmp'
                img = zip.open(image)
                ima = resize_image(img)
                ima.save('res/album/' + bmp_name, 'BMP')

if __name__ == '__main__':
    get_url()
    get_images()