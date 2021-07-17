from PIL import Image, ImageGrab
from numpy.linalg import norm
from win32api import GetSystemMetrics
import win32gui
import requests
import numpy as np
import time
import sys

connection = False

accelThreshold = 2000
brightnessThreshold = 50
prevBrightness =0

px = GetSystemMetrics(0)   #Monitor width
py = GetSystemMetrics(1)   #Monitor height

def take_screenshot():
   """
   Takes screenshot around the beat and saves it
   """
   x,y = win32gui.GetCursorPos()
   left = x-px/60
   top = py-py/15
   right = x+px/60
   bottom = py
   img = ImageGrab.grab(bbox = (left,top,right,bottom))
   return img

def cal_brightness(img):
   """
   Calculate the brightness of img and compare with previous value
   """
   brightness =np.average(img)
   global prevBrightness
   dBrightness = round(brightness - prevBrightness,3)
   prevBrightness = brightness
   return dBrightness

def get_accel():
   """
   Parameters: Try to request for the acceleration from ESP server
   Returns: the acceleration value if communication succeeds
   and exits if communication fails.
   """
   global connection
   try:
      r = requests.get("http://192.168.0.19/acceleration", timeout = 5)
      if r.status_code == 200:
         if connection == False:
            print("Connected")
            connection = True
         return int(r.text)
      
   except requests.ConnectionError:
      print("Connection lost")
      sys.exit()
   except requests.exceptions.Timeout:
      print("Timeout error")
      sys.exit()
   except requests.exceptions.RequestException as e:
      print("Unknown Error")
      sys.exit()

def main():
   justOnce =1
   accelTimer = time.time()
   beatTimer = time.time()
   while True:
      timer = time.time()
      if cal_brightness(take_screenshot()) > brightnessThreshold:
         beatTimer = time.time()
         if (beatTimer - accelTimer) < 0.25:
            if justOnce == 0:
               print("BGreat")
               justOnce = 1

      if get_accel() > accelThreshold:
         accelTimer = time.time()
         if (accelTimer - beatTimer) < 0.25:
            if justOnce == 0:
               print("AGreat")
               justOnce = 1

      if abs(beatTimer - accelTimer) > 0.5:
         if justOnce == 0:
            beatTimer = 0
            accelTimer =0 
         else:
            justOnce =0
      print(f"Execution speed is {time.time()-timer} sec")
         
         
         


if __name__ == "__main__":
    main()


