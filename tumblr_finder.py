__author__ = 'Jesse Bartola'

import os
import sys
import retrieval
import platform

def verify_path(path):
    if os.path.exists(path):
        return True
    # Create the directory if it does not exist
    os.makedirs(path)
    return False

def main(argv):
    if len(argv) < 2:
        print("\nYou must specify a tumblr username and a download path.\n")
        print("Usage: \n\tpython tumblr_finder.py <username> <download_path> <optional:min_image_size>")
        print("\nDefault minimum image download size is 20kb (20000) if not specified")
        if platform.system() == "Windows":
            print("\nExample: python tumblr_finder.py myblog123 C:\\Users\\Jesse\\Downloads 25000")
        else:
            print("\nExample: python tumblr_finder.py myblog123 /Users/Jesse/Downloads 25000")

        return

    username = argv[0]
    pathname = argv[1]
    picsize = 20000

    verify_path(pathname)

    if len(argv) == 3:
        try:
            picsize = int(argv[2])
        except ValueError:
            print("The third argument provided must be a positive integer")
            return

    retrieval.get_recent_pictures(username, pathname, picsize)
    #retrieval.get_oldest_pictures(username, pathname, picsize)

if __name__ == '__main__':
    main(sys.argv[1:])
