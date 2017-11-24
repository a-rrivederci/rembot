import cv2
import numpy as np
import time
import sys
from collections import deque

np.set_printoptions(threshold='nan')
start_time = time.time()

def bgr_to_cmyk(b,g,r, cmyk_scale = 100):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / 255.
    m = 1 - g / 255.
    y = 1 - b / 255.

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

def cmyk_to_bgr(c,m,y,k):
    rgb_scale = 255
    cmyk_scale = 100

    if (c == 1.0*cmyk_scale) and (m == 1.0*cmyk_scale) and (y == 1.0*cmyk_scale) and (k == 1.0*cmyk_scale):
        # black
        return 0, 0, 0

    r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))

    return b,g,r

# acquire image
print ("Acquiring image ...\n")
img = cv2.imread("/home/echo/Repos/machine-vision/images/rembrandt.jpg")
img_rows = img.shape[0]
img_cols = img.shape[1]
img_channels = img.shape[2]

# drawing properties
drawing_sheet_x = 400 # mm
drawing_sheet_y = 400 # mm
nib_diameter = 2        # mm
# Mapping a square of pixels_per_nib area from the image to one dot made by the nib
pixels_per_nib_x = int(img_cols/(drawing_sheet_x/nib_diameter))
pixels_per_nib_y = int(img_rows/(drawing_sheet_y/nib_diameter))

if (pixels_per_nib_x == 0):
    pixels_per_nib_x = 1

if (pixels_per_nib_y == 0):
    pixels_per_nib_y = 1
    
while (img_cols % pixels_per_nib_x != 0):
    pixels_per_nib_x += 1

while (img_rows % pixels_per_nib_y != 0 ):
    pixels_per_nib_y += 1

assert img_channels >= 3

# convert from bgr color space to cmyk color space
print("Converting from bgr color space to cmyk color space ...\n")
cyan = np.zeros((img_rows, img_cols), np.uint8)
magenta = np.zeros((img_rows, img_cols), np.uint8)
yellow = np.zeros((img_rows, img_cols), np.uint8)
black = np.zeros((img_rows, img_cols), np.uint8)
for row in range(img_rows):
    for col in range(img_cols):
        px_bgr = img[row, col]
        px_cmyk = bgr_to_cmyk(px_bgr[0], px_bgr[1], px_bgr[2])
        cyan[row,col] = px_cmyk[0]
        magenta[row, col] = px_cmyk[1]
        yellow[row,col] = px_cmyk[2]
        black[row,col] = px_cmyk[3]

# average the colors to nib size
print ("Averaging the colors to nib size ...\n")
avg_nib_y = int(img_rows/pixels_per_nib_y)
avg_nib_x = int(img_cols/pixels_per_nib_x)
cyan_avg = np.zeros((avg_nib_y, avg_nib_x), np.uint8)
magenta_avg = np.zeros((avg_nib_y, avg_nib_x), np.uint8)
yellow_avg = np.zeros((avg_nib_y, avg_nib_x), np.uint8)
black_avg = np.zeros((avg_nib_y, avg_nib_x), np.uint8)
sum_c = 0
sum_m = 0
sum_y = 0
sum_k = 0
for row_avg in range(avg_nib_y):
    for col_avg in range(avg_nib_x):
        for row in range(int(row_avg*pixels_per_nib_y), int(row_avg*pixels_per_nib_y + pixels_per_nib_y)):
            for col in range(int(col_avg*pixels_per_nib_x), int(col_avg*pixels_per_nib_x + pixels_per_nib_x)):
                px_c = cyan[row,col]
                px_m = magenta[row, col]
                px_y = yellow[row, col]
                px_k = black[row, col]
                sum_c += px_c
                sum_m += px_m
                sum_y += px_y
                sum_k += px_k
        cyan_avg[row_avg, col_avg] = sum_c / (pixels_per_nib_x * pixels_per_nib_y)
        magenta_avg[row_avg, col_avg] = sum_m / (pixels_per_nib_x * pixels_per_nib_y)
        yellow_avg[row_avg, col_avg] = sum_y / (pixels_per_nib_x * pixels_per_nib_y)
        black_avg[row_avg, col_avg] = sum_k / (pixels_per_nib_x * pixels_per_nib_y)
        sum_c = 0
        sum_m = 0
        sum_y = 0
        sum_k = 0

# reducing color resolution to 3 levels
for row_avg in range(avg_nib_y):
    for col_avg in range(avg_nib_x):
        if(cyan_avg[row_avg, col_avg] < 25):
            cyan_avg[row_avg, col_avg] = 0
        elif(cyan_avg[row_avg, col_avg] >= 25 and cyan_avg[row_avg, col_avg] <= 75):
            cyan_avg[row_avg, col_avg] = 50
        elif(cyan_avg[row_avg, col_avg] > 75):
            cyan_avg[row_avg, col_avg] = 100
        if (magenta_avg[row_avg, col_avg] < 25):
            magenta_avg[row_avg, col_avg] = 0
        elif (magenta_avg[row_avg, col_avg] >= 25 and magenta_avg[row_avg, col_avg] <= 75):
            magenta_avg[row_avg, col_avg] = 50
        elif (magenta_avg[row_avg, col_avg] > 75):
            magenta_avg[row_avg, col_avg] = 100
        if (yellow_avg[row_avg, col_avg] < 25):
            yellow_avg[row_avg, col_avg] = 0
        elif (yellow_avg[row_avg, col_avg] >= 25 and yellow_avg[row_avg, col_avg] <= 75):
            yellow_avg[row_avg, col_avg] = 50
        elif (yellow_avg[row_avg, col_avg] > 75):
            yellow_avg[row_avg, col_avg] = 100
        if (black_avg[row_avg, col_avg] < 25):
            black_avg[row_avg, col_avg] = 0
        elif (black_avg[row_avg, col_avg] >= 25 and black_avg[row_avg, col_avg] <= 75):
            black_avg[row_avg, col_avg] = 50
        elif (black_avg[row_avg, col_avg] > 75):
            black_avg[row_avg, col_avg] = 100

# communicating with firmware
# METHOD 1: Elegant and fast but difficult to compute
# Assumptions: a) Firmware takes (x,y) coordinates as input (with resolution of nib diameter)
#              b) Firmware indicates in some way after pen has reached the desired (x,y) coordinates
#              c) Firmware can be instructed to move down n rows and firmware indicates when it's done
# 1. Try to find the longest continuous line, then put the coordinates that describe the line in a 1D array. Remove the
#    points describing the longest line from the matrix of points that need to be drawn.
# 2. Repeat above until no more points left to be drawn.

# METHOD 2: Not as fast but easy to compute
# Assumptions: a) Firmware takes how long line to draw (resolution of nib diameter). Single point line is just a dot.
#              b) Firmware indicates in some way after drawing the line (or dot) is finished.
# 1. Go from top to down, left to right on row 0 and right to left on row 1 and so on.
# 2. Home pen to top-left of sheet
# 3. Draw the lines in first row:
#       3.1 Go to line beginning coordinate
#       3.2 Put pen down
#       3.3 Draw till line end coordinate reached
#       3.4 Lift pen up
# 4. Move one row below
# 5. Repeat step 3 and 4 for all rows, alternating between left-to-right and right-to-left

# Implementation of METHOD 2
# -1, -1 indicates home
# -2, -2 indicates  pen down
# -3, -3 indicates pen up
# -4, -4 indicates move down one row (this also toggles the direction the horizontal motor moves in)
# -5, n indicates go to pen location and pick up pen

#cmds is a 1 dimensional array, each element in the array is 2 dimensional
#   example: cmds[n] should return the nth 2D elemennt (x,y)
# 0 - k 50%
# 1 - k 100%
# 2 - c 50%
# 3 - c 100%
# 4 - m 50%
# 5 - m 100%
# 6 - y 50%
# 7 - y 100%
i=1
numColors = 8
#cmds = np.array(["goto_home"]) # go to home and pen down
#cmds = np.append( np.zeros((avg_nib_y * avg_nib_x), dtype=[('x', 'i4'), ('y', 'i4')]) )
cmds = np.array( [], dtype=[('x', 'i4'), ('y', 'i4')] )
buff = np.array( [(-1, -1)], dtype=[('x', 'i4'), ('y', 'i4')] )

for color in range(numColors):
    for row_painting in range(avg_nib_y):
        for col_painting in range(avg_nib_x):
            if color == 0:
                if black_avg[row_painting, col_painting] == 50:
                    if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                        buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                    buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                else:
                    if buff[-1][0] == -3 :
                        pass
                    else:
                        buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up
            if color == 1:
                if black_avg[row_painting, col_painting] == 100:
                    if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                        buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                    buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                else:
                    if buff[-1][0] == -3 :
                        pass
                    else:
                        buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up    
            if color == 2:
                if cyan_avg[row_painting, col_painting] == 50:
                    if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                        buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                    buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                else:
                    if buff[-1][0] == -3 :
                        pass
                    else:
                        buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up
            if color == 3:
                if cyan_avg[row_painting, col_painting] == 100:
                    if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                        buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                    buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                else:
                    if buff[-1][0] == -3 :
                        pass
                    else:
                        buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up    
            if color == 4:
                if magenta_avg[row_painting, col_painting] == 50:
                    if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                        buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                    buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                else:
                    if buff[-1][0] == -3 :
                        pass
                    else:
                        buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up    
            if color == 5:
                if magenta_avg[row_painting, col_painting] == 100:
                    if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                        buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                    buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                else:
                    if buff[-1][0] == -3 :
                        pass
                    else:
                        buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up
            if color == 6:
                if yellow_avg[row_painting, col_painting] == 50:
                    if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                        buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                    buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                else:
                    if buff[-1][0] == -3 :
                        pass
                    else:
                        buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up    
            if color == 7:
                if yellow_avg[row_painting, col_painting] == 100:
                    if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                        buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                    buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                else:
                    if buff[-1][0] == -3 :
                        pass
                    else:
                        buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up        
        # after each row
        if i%2 == 0:
            #flip row 
            for i in range(len(buff)):
                if buff[i][0] == -2:
                    buff[i] = (-3, -3)
                elif buff[i][0] == -3:
                    buff[i] = (-2, -2)
            # move next row command to top
            buff = deque (buff[::-1])
            buff.rotate(1)
        # append buff to cmds
        cmds = np.append( cmds, buff )
        # reset buff
        buff = np.array( [], dtype=[('x', 'i4'), ('y', 'i4')] )
        # append next row to buff
        buff = np.append( buff, np.array( [(-4, -4)], dtype=[('x', 'i4'), ('y', 'i4')] ) )
        i+=1
    # after each color
    # append change color
    cmds = np.append( cmds, np.array( [(-5, -5)], dtype=[('x', 'i4'), ('y', 'i4')] ) )
    # append home
    cmds = np.append( cmds, np.array( [(-1, -1)], dtype=[('x', 'i4'), ('y', 'i4')] ) )

# print array
f = open('output.txt','w')
for i in range(len(cmds)):
    f.write(str(cmds[i]) + "\n")
f.close()

# # paint using opencv
# painting = np.zeros((avg_nib_y, avg_nib_x, 3), np.uint8)

# # paint the cyan, magenta, yellow, and black points
# print ("Painting the cyan, magenta, yellow, and black points ...\n")
# for row_painting in range(avg_nib_y):
#     for col_painting in range(avg_nib_x):
#         painting[row_painting, col_painting] = cmyk_to_bgr(cyan_avg[row_painting, col_painting],
#                                                            magenta_avg[row_painting, col_painting],
#                                                            yellow_avg[row_painting, col_painting],
#                                                            black_avg[row_painting, col_painting])
# cv2.imwrite("painting.jpg", painting)
print("--- %s seconds ---" % (time.time() - start_time))
sys.exit(0)
