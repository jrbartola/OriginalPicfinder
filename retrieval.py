__author__ = 'Jesse'

import os
import glob
import itertools
import re
from urllib import request
from os.path import basename
from urllib import parse
from bs4 import BeautifulSoup

### ####
# PHOTO_SIZE: Default = 20000 bytes
# DOWNLOAD_PATH: Must be specified
# USERNAME: Must be specified



def get_recent_pictures(username, download_path, pic_size):

    url = 'http://' + username + '.tumblr.com/archive/filter-by/photo'

    try:
        url_content = request.urlopen(url).read()
    # Throw excpetion if url is invalid
    except Exception:
        print(Exception)
        return
    soup = BeautifulSoup(url_content)

    # We want only original, user-posted photos
    original_divs = soup.findAll('div', 'is_original')

    blog_links = []

    # Iterate through all div elements with 'is_original' class
    # and find the link to the picture they reference
    for tag in original_divs:
        post_links = tag.findAll('a')
        for link in post_links:
            blog_links.append(link['href'])

    photo_links = []

    for link in blog_links:
        post_soup = BeautifulSoup(request.urlopen(link).read())
        reg_photo = post_soup.findAll('img')
        # Check for iFrame embedded images
        frame_set = post_soup.findAll('iframe', 'photoset')

        # Iterate through all iFrames in set
        # If none exist, loop does not execute
        for frame in frame_set:
            iframe_url = frame['src']
            frame_soup = BeautifulSoup(request.urlopen(iframe_url).read())
            # Retrieve the link tags for all the photos in the iframe set
            frame_pics = frame_soup.findAll('a', 'photoset_photo')
            for pic in frame_pics:
                # Add the link of each iframe photo to the photolinks array
                photo_links.append(pic['href'])
        # Gets the URL of the main picture on the page, with a class permalink photo
        for reg in reg_photo:
            photo_links.append(reg['src'])

    # Download every image from their urls
    for img_url in photo_links:
        download_image_from_url(img_url, download_path, pic_size=pic_size)
    print
    print

def download_image_from_url(img_url, download_path, pic_size):
    # Download only the proper image files
    if img_url.lower().endswith('.jpeg') or \
        img_url.lower().endswith('.jpg') or \
        img_url.lower().endswith('.gif') or \
        img_url.lower().endswith('.png') or \
        img_url.lower().endswith('.bmp'):
        try:
            img_data = request.urlopen(img_url).read()
            # Download only significant images (min is 20 kb to avoid avatar downloads)
            if len(img_data) >= pic_size:
                file_name = username.upper() + basename(parse.urlsplit(img_url)[2])
                # Filter out avatar pictures if they are bigger than min photo size
                if 'static' not in file_name and 'avatar' not in file_name:
                    if (os.path.isfile(download_path + file_name)):
                        print('File exists. Skipping...')
                        # output = open(os.path.join(download_path, file_name), 'wb')
                        # output.write(imgData)
                        # output.close()
                    else:
                        print("Found    " + img_url)
                        output = open(os.path.join(download_path, file_name), 'wb')
                        output.write(imgData)
                        output.close()
        except Exception:
            print(Exception)
            # pass

