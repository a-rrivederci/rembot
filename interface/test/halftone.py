import sys
from optparse import OptionParser
import cv2 as cv
import numpy as np
from PIL import Image
from math import floor


def line_tone(image, window):
    """
    Converts image into line pattern
    img: (object) png/jpg image
    window: (int) window size
    """
    tone = np.zeros((window, window), dtype=np.uint8)
    # Set all values to white
    # tone[tone == 0] = 255
    # Set horizontal avg as white
    tone[int(tone.shape[0]/2)] = 255

    # Convert image to grayscale
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Get size of source image
    height, width = gray_image.shape

    # Create new image
    haltone_img = np.zeros((height, width), np.uint8)

    window_pixels = np.zeros((window, window), dtype=np.uint8)

    # Transform to line tone
    for i in range(0, height-window, window):
        for j in range(0, width-window, window):
            # Get pixels from window
            for row, wrow in enumerate(range(i, i+window)):
                for col, wcol in enumerate(range(j, j+window)):
                    try:
                        window_pixels[row, col] = gray_image[wrow, wcol]
                    except IndexError:
                        print(i, j,row, col, wrow, wcol)
                        sys.exit(1)

    
            # Get window average
            saturation = np.sum(window_pixels) / (window*window)

            if saturation > 127:
                haltone_img[i:i+window, j:j+window] = tone
            elif saturation < 127:
                pass
        
    return haltone_img

if __name__ == '__main__':
    PARSER = OptionParser(usage="usage: %prog [filename] window")
    _, ARGS = PARSER.parse_args()

    # Handle in complete args error
    if len(ARGS) != 2:
        PARSER.print_help()
        sys.exit(1)

    # Read source image
    SRC = cv.imread(ARGS[0], cv.IMREAD_COLOR)
    # Convert to Line Halftone
    RES = line_tone(SRC, int(ARGS[1]))

    # Create window
    #cv.namedWindow("Original", cv.WINDOW_NORMAL)
    cv.namedWindow("Result", cv.WINDOW_NORMAL)
    #cv.imshow('Original', SRC)
    cv.imshow("Result", RES)
    cv.imwrite("interface\images\k7.png", RES)

    # Tap 'q' to exit
    KEY = cv.waitKey(0) & 0xFF
    if KEY == ord('q'):
        cv.destroyWindow("image")
