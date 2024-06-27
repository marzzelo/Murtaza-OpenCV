import cv2
import numpy as np

def plot_clicked_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        
# mouse callback function

img = cv2.imread("Resources/cards.jpg")

width,height = 250,350
pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])  # the front card
# pts1 = np.float32([[277,116],[456,127],[260,362],[459,375]])  # the partially hidden card
# pts1 = np.float32([[7,126],[32,109],[44,179],[69,164]])  # the "K" letter

pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])


matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOutput = cv2.warpPerspective(img,matrix,(width,height))

cv2.imshow("Image",img)
cv2.setMouseCallback("Image", plot_clicked_points)  # click on the image to get the x,y coordinates of the 4 corners (use a "Z" shaped path)

cv2.imshow("Output",imgOutput)

cv2.waitKey(0)
