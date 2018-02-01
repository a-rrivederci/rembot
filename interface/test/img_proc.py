import sys
from optparse import OptionParser
import cv2 as cv
import numpy as np
from PIL import Image


def line_tone(image, window):
    """
    Converts image into line pattern
    img: (object) png/jpg image
    window: (int) window size
    """
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Get size
    height, width, channel = image.shape

    # Create new Image and a Pixel Map
    haltone_img = np.zeros((height, width), np.uint8)

    window_pixels = np.zeros((window, window, channel), dtype=np.uint8)

    # Transform to line tone
    for i in range(0, int(width/window) * window - window, window):
        for j in range(0, int(height/window)  * window - window, window):
            # get pixels from window
            for row, wrow in enumerate(range(i, i+window)):
                for col, wcol in enumerate(range(j, j+window)):
                    window_pixels[row, col] = image[wrow, wcol]
            
            return window_pixels

    return window_pixels

if __name__ == '__main__':
    PARSER = OptionParser(usage="usage: %prog [filename]")
    _, ARGS = PARSER.parse_args()

    # Handle no-file error
    if len(ARGS) != 1:
        PARSER.print_help()
        sys.exit(1)

    INPUT_IMG = ARGS[0]

    # Convert to Line Halftone
    SRC = cv.imread(INPUT_IMG, cv.IMREAD_COLOR)#cv.IMREAD_GRAYSCALE)
    RES = line_tone(SRC, 100)

    # Create window
    #cv.namedWindow("Original", cv.WINDOW_NORMAL)
    cv.namedWindow("Result", cv.WINDOW_NORMAL)
    #cv.imshow('Original', SRC)
    cv.imshow('Result', RES)

    # Tap 'q' to exit
    KEY = cv.waitKey(0) & 0xFF
    if KEY == ord('q'):
        cv.destroyWindow("image")
