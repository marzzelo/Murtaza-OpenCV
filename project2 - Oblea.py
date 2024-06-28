import cv2
import numpy as np

from Modules.stackImg import stackImages


cap = cv2.VideoCapture(0)
cap.set(10, 0)  # brightness

widthImg = 800  # cap.get(3)
heightImg = 600  # cap.get(4)

print(f"widthImg: {widthImg}, heightImg: {heightImg}")

imgWarped = None


def maskColor(img, HSVrange):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0

    lower = np.array(HSVrange[0:3])
    upper = np.array(HSVrange[3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    # x, y = getContours(mask)

    cv2.imshow("Mask", mask)
    return mask


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (9, 9), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    return imgThres


def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    # Approximate to a square

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # draw the vertices of the square in color (0, 255, 0)
            for vertex in approx:
                cv2.circle(
                    imgContour,
                    (vertex[0][0], vertex[0][1]),
                    20,
                    (0, 255, 0),
                    cv2.FILLED,
                )

            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area

    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)

    return biggest


def reorder(myPoints):
    # print(f'Before reshape: {myPoints}, shape={myPoints.shape}')
    myPoints = myPoints.reshape((4, 2))
    # print(f'After reshape: {myPoints}')

    myPointsNew = np.zeros(
        (4, 1, 2), np.int32
    )  # READ AS "4 ROWS BY 1 COLUMN OF 2 ELEMENTS EACH"
    # print(f'myPointsNew: {myPointsNew}')

    add = myPoints.sum(1)
    # print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints",myPointsNew)
    return myPointsNew


def getWarp(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    imgCropped = imgOutput[20 : imgOutput.shape[0] - 20, 20 : imgOutput.shape[1] - 20]
    # imgCropped = cv2.resize(imgCropped, (widthImg, heightImg))

    return imgCropped


while True:
    success, img = cap.read()

    img = cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    mask = maskColor(img, [24, 111, 55, 29, 197, 255])
                    #  [14, 99, 202, 32, 255, 255])

    # mask the image
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    imgThres = preProcessing(masked_img)

    biggest = getContours(imgThres)

    if biggest.size != 0:
        imgWarped = getWarp(img, biggest)
        # imageArray = ([img,imgThres],
        #           [imgContour,imgWarped])
        imageArray = [imgContour, imgWarped]
        # cv2.imshow("ImageWarped", imgWarped)
    else:
        if imgWarped is None:
            imgWarped = np.zeros((widthImg, heightImg, 3), np.uint8)
        # imageArray = ([img, imgThres],
        #               [img, img])
        # add a red frame around imgWarped
        cv2.putText(
            imgWarped,
            "No contour detected",
            (50, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 0, 255),
            2,
        )
        imageArray = [imgContour, masked_img]

    stackedImages = stackImages(0.6, imageArray)
    cv2.imshow("WorkFlow", stackedImages)

    key = cv2.waitKey(1)
    if key == ord("q") or key == 27:
        break
