from zipfile import ZipFile
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib

URL = ''
glance_size = (480, 800)

def get_url():
    global URL
    f = open('album.conf', 'r')
    url = f.readline().split('=')[1]
    URL = url
    f.close()

def crop_image(image):
    width = image.width
    height = image.height
    new_width = (3*height) / 5

    left_crop = (width / 2) - (new_width / 2) 
    right_crop = (width / 2) + (new_width / 2)
    image = image.crop((left_crop, 0, right_crop, height))

    return image

def resize_image(image_file):
    im = Image.open(image_file)
    im = crop_image(im)
    im = im.resize(glance_size)
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
        with ZipFile(zip_name, 'r') as zip:
            image_names = zip.namelist()
            print('Grabbing the photos...')
            for image in image_names:
                bmp_name = image.split('.')[0] + '.bmp'
                img = zip.open(image)
                ima = resize_image(img)
                ima.save('static/album/' + bmp_name, 'BMP')

if __name__ == '__main__':
    get_url()
    get_images()