import cv2
import numpy as np

from Modules.stackImg import stackImages
from Modules.trackbars import TrackBars

tbars = TrackBars()
tbars.createTrackBars()

try:
    cap = cv2.VideoCapture(0)
except Exception as e:
    print(e)
    exit(1)

cur_brightness = -0

cap.set(10, cur_brightness)  # 10 == cv.CAP_PROP_BRIGHTNESS

while True:
    success, img = cap.read()

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgH = imgHSV[:, :, 0]  # hue
    imgS = imgHSV[:, :, 1]  # saturation
    imgV = imgHSV[:, :, 2]  # value

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
print(f'{h_min}, {s_min}, {v_min}, {h_max}, {s_max}, {v_max}')
