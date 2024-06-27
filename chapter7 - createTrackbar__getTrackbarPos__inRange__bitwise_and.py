import cv2
import numpy as np
from Modules.stackImg import stackImages
from Modules.trackbars import TrackBars


path = "Resources/shapes.png"

tbars = TrackBars()
tbars.createTrackBars()

img = cv2.imread(path)

while True:
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgH = imgHSV[:,:,0]  # hue
    imgS = imgHSV[:,:,1]  # saturation
    imgV = imgHSV[:,:,2]  # value

    h_min, h_max, s_min, s_max, v_min, v_max = tbars.getTrackBarsValues()
    

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    
    mask = cv2.inRange(imgHSV, lower, upper)

    imgResult = cv2.bitwise_and(img, img, mask=mask)

    imgStack = stackImages(0.6, [[img, imgHSV], [mask, imgResult]])
    hsvComponents = stackImages(0.4, [[imgH, imgS, imgV]])
    cv2.imshow("Stacked Images", imgStack)
    cv2.imshow("HSV Components", hsvComponents)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break

print("\n\nValues of TrackBars: (h_min, s_min, v_min, h_max, s_max, v_max)")
print(h_min, s_min, v_min, h_max, s_max, v_max)
