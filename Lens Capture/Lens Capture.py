# Lens Capture
# importing the required packages
from win32api import GetSystemMetrics
from numpy import *

import pyautogui
import time
import cv2
import sys
import os

resolution = (GetSystemMetrics(0), GetSystemMetrics(1)) # System resolution
codec = cv2.VideoWriter_fourcc(*"mp4v") # Specify video codec

os.system('title Lens Capture') # Console title
print("Press Esc key to exit") # A small info, how to close the recorder
Filename = f"Capture-{str(time.time())}.mp4" # Specify name of Output file
Fps = 7 # Specify frames rate

out = cv2.VideoWriter(Filename, codec, Fps, resolution) # Creating a VideoWriter object

while 1:
	time.time() # This will smooth out the recording

	cv2.namedWindow("Lens Capture", cv2.WINDOW_NORMAL) # Create an Empty window
	cv2.resizeWindow("Lens Capture", 900, 500) # Resize this window

	image = pyautogui.screenshot() # Take screenshot using PyAutoGUI

	frame = array(image) # Convert the screenshot to a numpy array
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert it from BGR(Blue, Green, Red) to RGB(Red, Green, Blue)

	out.write(frame) # Write it to the output file
	cv2.imshow('Lens Capture', frame) # Optional: Display the recording screen

	# Stop recording when we press 'Esc' 
	if cv2.waitKey(33) == 27:  break
	if cv2.getWindowProperty('Lens Capture', cv2.WND_PROP_VISIBLE) < 1: break

out.release() # Release the Video writer
cv2.destroyAllWindows() # Destroy all windows
sys.exit()
