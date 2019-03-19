# Authors: Jake Edwards, Emalee Keesler, and Rubin Orozco
# Date: 3/19/2019
# Class: CSC 435-001
# Project: SFA-Cast

import numpy as np
import cv2
from PIL import ImageGrab

#Continuously grab frames until the 'esc' key is pressed
while True:
    img = ImageGrab.grab(bbox=(0,0,1920,1080)) #Pillow img
    img_np = np.array(img) #Convert pillow image to numpy array

    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB) #Convert to proper color space

    cv2.imshow("Screen", frame)

    if cv2.waitKey(1) ==27:
        break
    
cv2.destroyAllWindows()