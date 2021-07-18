from PIL import Image, ImageGrab, ImageOps,ImageStat
from numpy.linalg import norm
from win32api import GetSystemMetrics

import tkinter as tk
import win32gui
import numpy as np
import time
import sys

px = GetSystemMetrics(0)
py = GetSystemMetrics(1)   #Monitor height
prevBrightness =0

def take_screenshot():
   """
   Takes screenshot around the beat and saves it
   """
   x,y = win32gui.GetCursorPos()
   left = x-px/60
   top = py-py/15
   right = x+px/60
   bottom = py
   img = ImageGrab.grab(bbox = (left,top,right,bottom)).convert("L")
   return img

def cal_brightness(img):
   stat = ImageStat.Stat(img)
   brightness = stat.mean[0]
   global prevBrightness
   dbrightness = round(brightness - prevBrightness,3)
   prevBrightness = round(brightness,3)
   return dbrightness



def main():
   excecution_time = 0
   count = 0
   while count < 100:
      timer = time.time()
      cal_brightness(take_screenshot())
      excecution_time += time.time()-timer
      count +=1
   print(f"Average time: {excecution_time/count} sec")
   print(f"Trial num: {count}")
      
      
if __name__ == "__main__":
    main()

