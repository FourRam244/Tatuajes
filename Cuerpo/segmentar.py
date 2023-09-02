import cv2
import numpy as np
image = cv2.imread("p3.jpg")
image2 = cv2.resize(image, (650, 700), interpolation=cv2.INTER_CUBIC)
#Detectar color
hsv= cv2.cvtColor(image2,cv2.COLOR_RGB2HSV)

lower_verde= np.array([245,255,221])
upper_verde= np.array([90,49,37])


mask=cv2.inRange(hsv,upper_verde, lower_verde)

piel=cv2.bitwise_and(image2,image2, mask = mask)
kernel = np.ones((6,6),np.uint8)
apertura=cv2.morphologyEx(piel,cv2.MORPH_CLOSE,kernel)
cv2.imshow("original",image2)
cv2.waitKey(0)
cv2.imshow("HSV",hsv)
cv2.waitKey(0)
cv2.imshow("Final",mask)

cv2.waitKey(0)
cv2.imshow("1",apertura)
cv2.imwrite("final.png",apertura)
cv2.waitKey(0)
