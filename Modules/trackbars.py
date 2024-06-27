import cv2

def empty(a: int):
    return None


class TrackBars:
    def __init__(self):
        self.h_min = 0
        self.h_max = 179
        self.s_min = 0
        self.s_max = 255
        self.v_min = 0
        self.v_max = 255

    def createTrackBars(self):
        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TrackBars", 640, 240)
        cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
        cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
        cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
        cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
        cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
        cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

    def getTrackBars(self):
        self.h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        self.h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        self.s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        self.s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        self.v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        self.v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    def getTrackBarsValues(self):
        self.getTrackBars()
        return self.h_min, self.h_max, self.s_min, self.s_max, self.v_min, self.v_max
