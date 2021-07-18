from PIL import Image
import pyautogui
import numpy as np
import sys
import cv2

beatThreshold = 0.05
prevBrightness =0
score =0

def take_screenshot():
   """
   Takes screenshot around the beat and saves it
   """
   px,py = pyautogui.size()
   x,y = pyautogui.position()
   left = x-px/60
   top = py-py/15
   width = px/30
   height = py/15
   img = pyautogui.screenshot("screenshit.png",region=(left, top, width, height))
   img.save("screenshit.png")

def cal_brightness():
   """
   Calculates the image brightness and compare with previous
   """
   greyscale_image = Image.open("screenshit.png").convert('L')
   histogram = greyscale_image.histogram()
   pixels = sum(histogram)
   brightness = scale = len(histogram)

   for index in range(0, scale):
      ratio = histogram[index] / pixels
      brightness += ratio * (-scale + index)
   global prevBrightness
   dBrightness = round(brightness/scale - prevBrightness,3)
   prevBrightness = round(brightness/scale,3)
   return dBrightness


def main():
   while True:
      cap = cv2.VideoCapture("Haku_Wank_Slow.mp4")
      while True:
         take_screenshot()
         ret, frame = cap.read()
         if ret == False:
            cap = cv2.VideoCapture("Haku_Wank_Slow.mp4")
            ret, frame = cap.read()
         cv2.imshow('frame',frame)
         
         if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit()
            
         if cal_brightness() > beatThreshold:
            cap.release()
            cap = cv2.VideoCapture("Haku_Wank_Fast.mp4")
      cap.release()
      cv2.destroyAllWindows()




if __name__ == "__main__":
    main()

