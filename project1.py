import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 0)

# myColors = [[76, 207, 35, 88, 255, 75],  # green
#             [0, 155, 79, 11, 204, 187],  # red
#             [27, 111, 137, 34, 169, 188], ]  # yellow
myColors = [[73, 255, 64, 91, 255, 242],  # green
            [0, 83, 190, 20, 207, 255],  # red
            [27, 0, 248, 44, 76, 255], ]  # yellow

myColorValues = [[0, 180, 0],  # BGR
                 [0, 0, 200],
                 [0, 255, 255], ]
# [3, 132, 252]]

myPoints = []  # [x , y , colorId ]

mouse_dn = False


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 15, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]),mask)
    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


def mouse_callback(event, x, y, flags, param):
    global mouse_dn, myPoints
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_dn = True
        print("Mouse Down")
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_dn = False
        print("Mouse Up")
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("Clear")
        myPoints.clear()


cv2.namedWindow("Result")
cv2.setMouseCallback("Result", mouse_callback)

while True:

    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    if mouse_dn:
        if len(newPoints) != 0:
            for newP in newPoints:
                myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) == 27:
        break
