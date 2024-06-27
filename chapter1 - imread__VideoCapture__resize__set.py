# ------------------ READ IMAGE --------------------------
# import cv2
# # LOAD AN IMAGE USING 'IMREAD'
# img = cv2.imread("Resources/lena.png")
# # DISPLAY
# cv2.imshow("Lena Soderberg",img)
# cv2.waitKey(0)

# ------------------ READ VIDEO --------------------------
# import cv2
#
# frameWidth = 640
# frameHeight = 480
# cap = cv2.VideoCapture("Resources/test_video.mp4")
# while True:
#     success, img = cap.read()
#
#     if not success:
#         break
#
#     img = cv2.resize(img, (frameWidth, frameHeight))
#     cv2.imshow("Result", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# ------------------ READ WEBCAM --------------------------
import cv2

try:
    cap = cv2.VideoCapture(0)
except Exception as e:
    print(e)
    exit(1)

frameWidth = cap.get(3)  # 3 == cv.CAP_PROP_FRAME_WIDTH
frameHeight = cap.get(4)  # 4 == cv.CAP_PROP_FRAME_HEIGHT

print(f'Frame Width: {frameWidth}, Frame Height: {frameHeight}')

cur_brightness = 0

cap.set(10, cur_brightness)  # 10 == cv.CAP_PROP_BRIGHTNESS

while True:
    success, img = cap.read()
    cv2.imshow("Result", img)
    key = cv2.waitKey(1)

    if key == 27 or not success:
        break

    if key == ord('b'):
        cur_brightness += 10
        print(cur_brightness)
        cap.set(10, cur_brightness)
    elif key == ord('d'):
        cur_brightness -= 10
        cap.set(10, cur_brightness)
        print(cur_brightness)


cap.release()
cv2.destroyAllWindows()
