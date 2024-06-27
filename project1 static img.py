import cv2
import numpy as np
from Modules.stackImg import stackImages


# LOAD AN IMAGE USING 'IMREAD'
img = cv2.imread("Resources/shapes.png")
# get the dimensions of the image
frameWidth = img.shape[1]
frameHeight = img.shape[0]
# DISPLAY
# cv2.imshow("Lena Soderberg",img)


# cap = cv2.VideoCapture(1)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# cap.set(10,150)

# Values of TrackBars FOR YELLOW: (h_min, s_min, v_min, h_max, s_max, v_max)
# 0 255 255 157 255 255

# Values of TrackBars FOR RED: (h_min, s_min, v_min, h_max, s_max, v_max)
# 179 217 233 179 232 255

# Values of TrackBars for GREEN: (h_min, s_min, v_min, h_max, s_max, v_max)
# 73 255 163 79 255 176

# Values of TrackBars for BLUE: (h_min, s_min, v_min, h_max, s_max, v_max)
# 111 141 163 116 146 175

myColors = [
    [0, 255, 255, 157, 255, 255],  ## HSV for YELLOW
    [179, 217, 233, 179, 232, 255],  ## HSV for RED
    [73, 255, 163, 79, 255, 176],  ## HSV for GREEN
    [111, 141, 163, 116, 146, 175],  ## HSV for BLUE
]

myColorValues = [[0, 255, 255], [0, 0, 255], [0, 255, 0], [255, 0, 0]]  ## BGR

myPoints = []  ## [x , y , colorId ]


def findPenTip(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    color_id = 0
    newPoints = []
    components = []
    
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        
        mask = cv2.inRange(imgHSV, lower, upper)
        
        masked = cv2.bitwise_and(img, img, mask=mask)
        # draw a white capture around the masked image
        masked = cv2.rectangle(masked, (0, 0), (frameWidth, frameHeight), (255, 255, 255), 5)
        
        components.append(masked)
        
        x, y = getContours(mask, True)
        cv2.circle(img, (x, y), 15, myColorValues[color_id], cv2.FILLED)
        cv2.circle(img, (x, y), 15, (0, 0, 0), 1)
        if x != 0 and y != 0:
            newPoints.append([x, y, color_id])
        color_id += 1
        
        
    # reshape the components list to a 2 by 2 matrix
    components = [components[i:i + 2] for i in range(0, len(components), 2)]
    cv2.imshow("Components", stackImages(0.4, components))
    return newPoints


def getContours(img, center=False):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    if center:
        return x + w // 2, y + h // 2
    
    return x + w // 2, y


def drawOnCanvas(img, myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(
            img, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED
        )


pen_tips = findPenTip(img, myColors, myColorValues)
drawOnCanvas(img, pen_tips, myColorValues)
cv2.imshow("Result", img)
if cv2.waitKey(0) & 0xFF == ord("q"):
    cv2.destroyAllWindows()


# while True:
#     success, img = cap.read()
#     imgResult = img.copy()
#     newPoints = findPenTip(img, myColors, myColorValues)
#     if len(newPoints) != 0:
#         for newP in newPoints:
#             myPoints.append(newP)
#     if len(myPoints) != 0:
#         drawOnCanvas(myPoints, myColorValues)

#     cv2.imshow("Result", imgResult)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
