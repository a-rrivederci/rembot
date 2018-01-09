#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image ability provides Rembot with the ability to process images
License is available in LICENSE
@author eeshiken
@since 2017-DEC-28
"""

import cv2
import numpy as np


class Image:
    def __init__(self):
        np.set_printoptions(threshold='nan')
        self.start_time = time.time()

    def img_process(self, imgpath):
        # acquire image
        print("Acquiring image ...")
        img = cv2.imread(imgpath)
        print("Done!\n")
        img_rows = img.shape[0]
        img_cols = img.shape[1]
        img_channels = img.shape[2]

        # drawing properties
        drawing_sheet_x = 400 # mm
        drawing_sheet_y = 400 # mm
        nib_diameter = 2        # mm

        # Mapping a square of pixels_per_nib area from the image to one dot made by the nib
        pixels_per_nib_x = 1
        pixels_per_nib_y = 1

        assert img_channels >= 3

        # convert from bgr color space to cmyk color space
        print("Converting from bgr color space to cmyk color space ...")
        cyan = np.zeros((img_rows, img_cols), np.uint8)
        magenta = np.zeros((img_rows, img_cols), np.uint8)
        yellow = np.zeros((img_rows, img_cols), np.uint8)
        black = np.zeros((img_rows, img_cols), np.uint8)

        blue = img[:, :, 0]
        green = img[:, :, 1]
        red = img[:, :, 2]

        blue[blue == 0] = 1 # to avoid r=g=b=0 that leads to nan cmyk

        cyan = (1 - red/255)
        magenta = (1 - green/255)
        yellow = (1 - blue/255)
        black = np.minimum(cyan, magenta)
        black = np.minimum(black, yellow)
        cyan = (cyan - black)/(1 - black)
        magenta = (magenta - black)/(1 - black)
        yellow = (yellow - black)/(1 - black)

        cyan = cyan * 100
        magenta = magenta * 100
        yellow = yellow * 100
        black = black * 100
        print("Done!\n")

        # average the colors to nib size
        print("Averaging the colors to nib size ...")
        self.avg_nib_y = int(img_rows/pixels_per_nib_y)
        self.avg_nib_x = int(img_cols/pixels_per_nib_x)
        self.cyan_avg = np.zeros((self.avg_nib_y, self.avg_nib_x), np.uint8)
        self.magenta_avg = np.zeros((self.avg_nib_y, self.avg_nib_x), np.uint8)
        self.yellow_avg = np.zeros((self.avg_nib_y, self.avg_nib_x), np.uint8)
        self.black_avg = np.zeros((self.avg_nib_y, self.avg_nib_x), np.uint8)

        sum_c = 0
        sum_m = 0
        sum_y = 0
        sum_k = 0
        for row_avg in range(self.avg_nib_y):
            for col_avg in range(self.avg_nib_x):
                for row in range(int(row_avg*pixels_per_nib_y), int(row_avg*pixels_per_nib_y + pixels_per_nib_y)):
                    for col in range(int(col_avg*pixels_per_nib_x), int(col_avg*pixels_per_nib_x + pixels_per_nib_x)):
                        px_c = cyan[row, col]
                        px_m = magenta[row, col]
                        px_y = yellow[row, col]
                        px_k = black[row, col]
                        sum_c += px_c
                        sum_m += px_m
                        sum_y += px_y
                        sum_k += px_k
                self.cyan_avg[row_avg, col_avg] = sum_c / (pixels_per_nib_x * pixels_per_nib_y)
                self.magenta_avg[row_avg, col_avg] = sum_m / (pixels_per_nib_x * pixels_per_nib_y)
                self.yellow_avg[row_avg, col_avg] = sum_y / (pixels_per_nib_x * pixels_per_nib_y)
                self.black_avg[row_avg, col_avg] = sum_k / (pixels_per_nib_x * pixels_per_nib_y)
                sum_c = 0
                sum_m = 0
                sum_y = 0
                sum_k = 0

        # reducing color resolution to 3 levels
        self.cyan_avg[self.cyan_avg < 25] = 0
        self.magenta_avg[self.magenta_avg < 25] = 0
        self.yellow_avg[self.yellow_avg < 25] = 0
        self.black_avg[self.black_avg < 25] = 0

        self.cyan_avg[np.logical_and(self.cyan_avg >= 25, self.cyan_avg <= 75)] = 50
        self.magenta_avg[np.logical_and(self.magenta_avg >= 25, self.magenta_avg <= 75)] = 50
        self.yellow_avg[np.logical_and(self.yellow_avg >= 25, self.yellow_avg <= 75)] = 50
        self.black_avg[np.logical_and(self.black_avg >= 25, self.black_avg <= 75)] = 50

        self.cyan_avg[self.cyan_avg > 75] = 100
        self.magenta_avg[self.magenta_avg > 75] = 100
        self.yellow_avg[self.yellow_avg > 75] = 100
        self.black_avg[self.black_avg > 75] = 100
        print("Done!\n")

        # # paint the target image shown on gui using opencv
        painting = np.zeros((self.avg_nib_y, self.avg_nib_x, 3), np.uint8)
        r = np.zeros((self.avg_nib_y, self.avg_nib_x, 3), np.uint8)
        g = np.zeros((self.avg_nib_y, self.avg_nib_x, 3), np.uint8)
        b = np.zeros((self.avg_nib_y, self.avg_nib_x, 3), np.uint8)

        r = 255 * (1.0 - self.cyan_avg / float(100)) * (1.0 - self.black_avg / float(100))
        g = 255 * (1.0 - self.magenta_avg / float(100)) * (1.0 - self.black_avg / float(100))
        b = 255 * (1.0 - self.yellow_avg / float(100)) * (1.0 - self.black_avg / float(100))

        r[np.logical_and(np.logical_and(np.logical_and(self.cyan_avg == 100.0, self.magenta_avg == 100.0), self.yellow_avg == 100.0), self.black_avg == 100.0)] = 0
        g[np.logical_and(np.logical_and(np.logical_and(self.cyan_avg == 100.0, self.magenta_avg == 100.0), self.yellow_avg == 100.0), self.black_avg == 100.0)] = 0
        b[np.logical_and(np.logical_and(np.logical_and(self.cyan_avg == 100.0, self.magenta_avg == 100.0), self.yellow_avg == 100.0), self.black_avg == 100.0)] = 0

        print ("Painting the cyan, magenta, yellow, and black points ...")
        for row in range(self.avg_nib_y):
            for col in range(self.avg_nib_x):
                painting[row, col] = b[row, col], g[row, col], r[row, col]
        cv2.imwrite("images/target_image.png", painting)
        print("Done!\n")
        return

        '''
            communicating with firmware
            METHOD 1: Elegant and fast but difficult to compute
            Assumptions: a) Firmware takes (x,y) coordinates as input (with resolution of nib diameter)
                        b) Firmware indicates in some way after pen has reached the desired (x,y) coordinates
                        c) Firmware can be instructed to move down n rows and firmware indicates when it's done
            1. Try to find the longest continuous line, then put the coordinates that describe the line in a 1D array. Remove the
            points describing the longest line from the matrix of points that need to be drawn.
            2. Repeat above until no more points left to be drawn.

            METHOD 2: Not as fast but easy to compute
            Assumptions: a) Firmware takes how long line to draw (resolution of nib diameter). Single point line is just a dot.
                        b) Firmware indicates in some way after drawing the line (or dot) is finished.
            1. Go from top to down, left to right on row 0 and right to left on row 1 and so on.
            2. Home pen to top-left of sheet
            3. Draw the lines in first row:
                3.1 Go to line beginning coordinate
                3.2 Put pen down
                3.3 Draw till line end coordinate reached
                3.4 Lift pen up
            4. Move one row below
            5. Repeat step 3 and 4 for all rows, alternating between left-to-right and right-to-left

            Implementation of METHOD 2
            -1, -1 indicates home
            -2, -2 indicates  pen down
            -3, -3 indicates pen up
            -4, -4 indicates move down one row (this also toggles the direction the horizontal motor moves in)
            -5, n indicates go to pen location and pick up pen

            self.cmds is a 1 dimensional array, each element in the array is 2 dimensional
            example: self.cmds[n] should return the nth 2D elemennt (x,y)
            0 - k 50%
            1 - k 100%
            2 - c 50%
            3 - c 100%
            4 - m 50%
            5 - m 100%
            6 - y 50%
            7 - y 100%
        '''

    def generate_cmds(self):
        # generate gcode
        print("Generating GCode ...")
        i = 1
        numColors = 8
        self.cmds = np.array([], dtype=[('x', 'i4'), ('y', 'i4')])
        buff = np.array([(-1, -1)], dtype=[('x', 'i4'), ('y', 'i4')])

        for color in range(numColors):
            for row_painting in range(self.avg_nib_y):
                for col_painting in range(self.avg_nib_x):
                    if color == 0:
                        if self.black_avg[row_painting, col_painting] == 50:
                            if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                                buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                            buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                        else:
                            if buff[-1][0] == -3 :
                                pass
                            else:
                                buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up
                    if color == 1:
                        if self.black_avg[row_painting, col_painting] == 100:
                            if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                                buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                            buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                        else:
                            if buff[-1][0] == -3 :
                                pass
                            else:
                                buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up    
                    if color == 2:
                        if self.cyan_avg[row_painting, col_painting] == 50:
                            if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                                buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                            buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                        else:
                            if buff[-1][0] == -3 :
                                pass
                            else:
                                buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up
                    if color == 3:
                        if self.cyan_avg[row_painting, col_painting] == 100:
                            if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                                buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                            buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                        else:
                            if buff[-1][0] == -3 :
                                pass
                            else:
                                buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up    
                    if color == 4:
                        if self.magenta_avg[row_painting, col_painting] == 50:
                            if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                                buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                            buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                        else:
                            if buff[-1][0] == -3 :
                                pass
                            else:
                                buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up    
                    if color == 5:
                        if self.magenta_avg[row_painting, col_painting] == 100:
                            if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                                buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                            buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                        else:
                            if buff[-1][0] == -3 :
                                pass
                            else:
                                buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up
                    if color == 6:
                        if self.yellow_avg[row_painting, col_painting] == 50:
                            if buff[-1][0] == -1 or buff[-1][0] == -3 or buff[-1][0] == -4: # home or pen up
                                buff = np.append( buff, np.array( [(-2, -2)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen down
                            buff = np.append( buff, np.array( [(row_painting, col_painting)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # black coord
                        else:
                            if buff[-1][0] == -3 :
                                pass
                            else:
                                buff = np.append( buff, np.array( [(-3, -3)], dtype=[('x', 'i4'), ('y', 'i4')] ) ) # pen up    
                    if color == 7:
                        if self.yellow_avg[row_painting, col_painting] == 100:
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
                # append buff to self.cmds
                self.cmds = np.append( self.cmds, buff )
                # reset buff
                buff = np.array( [], dtype=[('x', 'i4'), ('y', 'i4')] )
                # append next row to buff
                buff = np.append( buff, np.array( [(-4, -4)], dtype=[('x', 'i4'), ('y', 'i4')] ) )
                i+=1
            # after each color
            # append change color
            self.cmds = np.append( self.cmds, np.array( [(-5, -5)], dtype=[('x', 'i4'), ('y', 'i4')] ) )
            # append home
            self.cmds = np.append( self.cmds, np.array( [(-1, -1)], dtype=[('x', 'i4'), ('y', 'i4')] ) )
        print("Done!\n")

        # debug print array
        # print("Outputing preprocessing ...")
        # f = open('debug/output_preprocess.txt','w')
        # for i in range(len(self.cmds)):
        #     f.write(str(self.cmds[i]) + "\n")
        # f.close()
        # print("Done!\n")

        # process commands
        print("Processing ...")
        self.s_cmds = np.array( [], dtype=[('x', 'i4'), ('y', 'i4')] )

        for i in range(len(self.cmds)):
            if self.cmds[i][0] == -1:
                self.s_cmds = np.append( self.s_cmds, self.cmds[i] )
            elif self.cmds[i][0] == -2:
                self.s_cmds = np.append( self.s_cmds, self.cmds[i] )
                if self.cmds[i+2][0] != -3:
                    self.s_cmds = np.append( self.s_cmds, self.cmds[i+1] )
            elif self.cmds[i][0] == -3: 
                self.s_cmds = np.append( self.s_cmds, self.cmds[i-1])
                self.s_cmds = np.append( self.s_cmds, self.cmds[i])
            elif self.cmds[i][0] == -4:
                if self.cmds[i+1][0] != -4:
                    self.s_cmds = np.append( self.s_cmds, self.cmds[i])
            elif self.cmds[i][0] == -5:
                self.s_cmds = np.append( self.s_cmds, self.cmds[i])
        print("Done!\n")

        # # debug print array
        # print("Outputing postprocessing ...")
        # f = open('debug/output_postprocess.txt','w')
        # for i in range(len(self.s_cmds)):
        #     f.write(str(self.s_cmds[i]) + "\n")
        # f.close()
        # print("Done!\n")

        return 
