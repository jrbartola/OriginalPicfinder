# OriginalPicfinder
A Tumblr web scraper that finds and downloads all [recent] user-posted pictures from a given blog

## What does it do?
This little script makes use of the BeautifulSoup web-scraping module for Python. Tumblr naturally does not provide a way to strictly view user-uploaded posts from a certain blog. This makes it difficult if one wanted to differentiate between posts that are taken from another blog vs posts that have been uploaded by a user. OriginalPicfinder solves this by traversing the archive of a certain blog and downloading all of its original pictures into a folder of one's choosing.

## Usage
Download the contents of the repo and navigate to the contents of the directory in a terminal

*Syntax*
```
python tumblr_finder.py <username> <download_path> <optional:minimum_pic_size>
```

The script requires at least 2 parameters to run, with a third optional parameter.

```
username
```
(String) The username of the blog you want to download photos from
```
download_path
``` 
(String) An absolute directory path pointing to the folder that the pictures will be downloaded to. If the directory specified does not exist, it will be created for you
```
minimum_pic_size
``` 
(Int) This optional parameter describes the minimum size in bytes of any photo that will be downloaded. Smaller values will be more likely to download unwanted pictures such as avatar icons and navbar items. If omitted, the minimum download size will default to 20000 (20kb). 

