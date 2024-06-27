import cv2
import numpy as np
from Modules.stackImg import stackImages
from Modules.getContours import getContours


# def getContours(img):
# """
# Function to get the contours of the shapes in the image
# """
# contours, hierarchy = cv2.findContours(
#     img,
#     cv2.RETR_EXTERNAL,  # retrieves the outermost contours only
#     cv2.CHAIN_APPROX_NONE  # retrieves all the points of the contours
# )

# # the following loop will draw the contours and the bounding boxes around the shapes
# # and will also write the type of the shape in the middle of the bounding box
# for anum, cnt in enumerate(contours):
#     print(f'Contour # {anum}: {cnt}')
#     area = cv2.contourArea(cnt)  # calculates the area of the contour (in pixels)
#     print(f"Area # {anum}: {area}")
#     if area > 500:
#         cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
#         peri = cv2.arcLength(cnt, True)
#         print(f'Perimeter # {anum}: {peri}')
#         approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # approximates the contours to a polygon. (**)
#         objCor = len(approx)
#         print(f'Number of corners # {anum}: {objCor}')

#         x, y, w, h = cv2.boundingRect(approx)
#         if objCor == 3:
#             objectType = "Tri"
#         elif objCor == 4:
#             aspRatio = w / float(h)
#             if aspRatio > 0.98 and aspRatio < 1.03:
#                 objectType = "Square"
#             else:
#                 objectType = "Rectangle"
#         elif objCor > 4:
#             objectType = "Circle"
#         else:
#             objectType = "Unknown"

#         cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.putText(
#             imgContour,
#             objectType,
#             (x + (w // 2) - 10, y + (h // 2) - 10),
#             cv2.FONT_HERSHEY_COMPLEX,
#             0.7,  # font scale
#             (0, 0, 0),
#             2,  # thickness
#         )


path = "Resources/shapes.png"
img0 = cv2.imread(path)

# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
# imgCanny = cv2.Canny(imgBlur, 50, 50)
# getContours(imgCanny)

(img, imgGray, imgBlur, imgCanny, imgContour) = getContours(
    img0,
    process=True,
    area_threshold=500,
    color=(255, 0, 0),
    thickness=3,
    fontScale=0.7,
    fontThickness=2,
    verbose=True,
)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.6, ([img0, imgGray], [imgCanny, imgContour]))

cv2.imshow("Stack", imgStack)

cv2.waitKey(0)

"""
(**) La función cv2.approxPolyDP se utiliza para aproximar una forma a otra forma con menos número de vértices dependiendo 
de la precisión que especifiquemos. Esta función toma tres argumentos:

-cnt: Es el contorno que queremos aproximar.

-epsilon: Es el parámetro de precisión. Es la máxima distancia entre la curva original y su aproximación. 
Una forma común de elegir el valor de epsilon es basándolo en un porcentaje del perímetro del contorno (cv2.arcLength). 
En este caso, se está utilizando el 2% del perímetro del contorno.

-closed=True: Indica que la curva aproximada debe ser cerrada.

Por lo tanto, el perímetro se utiliza para fijar el parámetro epsilon en la instrucción 
approx = cv2.approxPolyDP(cnt, 0.02 * peri, True) 
para determinar el nivel de precisión de la aproximación. 

Un valor de epsilon más grande dará una aproximación más simple (menos vértices), mientras que un valor de epsilon 
más pequeño dará una aproximación más precisa (más vértices).

"""
