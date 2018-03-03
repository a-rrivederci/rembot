#!/usr/bin/python3
from PIL import Image


class Algo:
    
    def rcodeGenerate(data):
        #Paper Offests
        x_offset = 20
        y_offset = 20

        #Commands for Bot!
        reset       = ["R00"]
        penDown     = ["R02 P1"]
        penLift     = ["R02 P0"]
        setPosition = ["M90 X[(x value)] Y[(y value)]"]

        #Movement, can be UP DOWN LEFT RIGHT
        #Dont use speed yet
        Move = ["R01 X[(x value)] Y[(y value)] F[(speed)]"] 

        #-----------------------------------------------------#
        cmd = []
        xLength = 20
        yLength = 1
        for row in data:
            if data.index in row == 0:
                cmd.append("R02 P1\r\n")
                cmd.append("R01 x0 X10 y0 Y0\r\n")
            elif row == row[-1]:
                cmd.append("R02 P0\r\n")
                cmd.append("R01 x0 X0 y0 Y1\r\n")
            else:
                cmd.append("R02 P0\r\n")
                cmd.append("R01 x0 X10 y0 Y0\r\n")

        # Commands are appended in the list in reverse
        cmd.reverse()
        self.cmd
        print(cmd)

    def paperScaleCheck(img):
        # The paper Width and Height are calculated @300dpi for an A4 paper!
        paperWidth = 2480
        paperHeight = 3508
        imgWidth, imgHeight = img.size
        print(imgWidth, imgHeight)

        if imgHeight > paperHeight or imgWidth > paperWidth:
            print('Cant print this image too large')
        else:
            print('Processing ...')
            imageToLists(img)


    def imageToLists(img):
        WIDTH, HEIGHT = img.size

        #convert image data to a list of integers
        data = list(img.getdata())

        # convert that to 2D list (list of lists of integers)
        data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

        # At this point the image's pixels are all in memory and can be accessed
        # individually using data[row][col].

        #for row in data:
            #print(' '.join('{:3}'.format(value) for value in row))
        
        rcodeGenerate(data)    

    def main():
        img = Image.open('photo.png').convert('L')
        paperScaleCheck(img)

    
if __name__ == "__main__":
    main()