__author__ = 'Jesse Bartola'

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

def get_oldest_pictures(username, download_path, pic_size):
    next_time = 0
    while next_time is not False and next_time is not None:
        next_time = get_recent_pictures(username, download_path, pic_size, next_time)


def get_recent_pictures(username, download_path, pic_size, before_time=0):

    if before_time != 0:
        url = 'http://' + username + '.tumblr.com/archive/filter-by/photo?before_time=' + str(before_time)
    else:
        url = 'http://' + username + '.tumblr.com/archive/filter-by/photo'

    try:
        url_content = request.urlopen(url).read()
    # Throw excpetion if url is invalid
    except Exception as e:
        print("Could not open page due to " + str(e) + ". Skipping..")
        return False
    soup = BeautifulSoup(url_content)

    # We want only original, user-posted photos
    original_divs = soup.findAll('div', 'is_original')

    # Retrieve link to next archive page (if retrieving oldest pics)
    next_time = soup.find('a', {'id':'next_page_link'})

    # If we reached the last page, terminate
    if next_time is None:
        print("Reached the end of " + username + "'s archive. Finishing...")
        return None

    next_time = int(next_time['href'][37:])
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
        download_image_from_url(username, img_url, download_path, pic_size=pic_size)
    print
    print
    return next_time

def download_image_from_url(username, img_url, download_path, pic_size):
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
                        print("Downloading    " + img_url + "...")
                        output = open(os.path.join(download_path, file_name), 'wb')
                        output.write(img_data)
                        output.close()
        except Exception as e:
            #print(Exception)
            print("Could not download picture due to " + str(e) + ". Skipping...")
            # pass

