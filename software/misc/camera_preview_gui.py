import sys
import pygame
import picamera
import picamera.array

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode([display_width,display_height])
pygame.display.set_caption('Remnants of Rembrandt')

white = (255,255,255)

running = True
    
def displayImage(image,x,y):
    convertedImage = pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"RGB")
    gameDisplay.blit(convertedImage, (x,y))

x = (display_width - 320)
y = (display_height * 0)

with picamera.PiCamera() as camera:
     with picamera.array.PiRGBArray(camera) as stream:
         camera.resolution = (320, 240)
         
         while running:
             camera.capture(stream, 'rgb', use_video_port=True)
             # stream.array now contains the image data in BGR order
             for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     running = False
             gameDisplay.fill(white)
             displayImage(stream.array,x,y)
             pygame.display.update()
             stream.seek(0)
             stream.truncate()

pygame.display.quit()
pygame.quit()
sys.exit()