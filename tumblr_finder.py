__author__ = 'Jesse'

import sys
import retrieval

def main(argv):
    if len(argv) < 2:
        print("\nYou must specify a tumblr username and a download path.\n")
        print("Use: \n\tpython tumblr_finder.py <username> <download_path> <optional:min_image_size>")
        print("\nDefault minimum image download size is 20kb (20000) if not specified")
        print("\nExample: python tumblr_finder.py myblog123 C:\\Users\\Jesse\\Downloads\\ 25000")
        return
    retrieval.get_recent_pictures(argv[0], argv[1], argv[2])

if __name__ == '__main__':
    main(sys.argv[1:])
