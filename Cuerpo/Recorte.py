

import cv2
import numpy as np

xI, yI, xF, yF = 0,0,0,0
interruptor=False

def dibujar(event,x,y,flags,param):
    global xI,yI,xF,yF,interruptor,imagen
    if event == cv2.EVENT_LBUTTONDOWN:
       xI,yI = x,y
       interruptor=False
    
    if event == cv2.EVENT_LBUTTONUP:
        xF,yF = x,y
        interruptor=True
        recorte=imagen[yI:yF,xI:xF,:]

        cv2.imwrite("Recorte.png", recorte)

        print("coordenadas","[",xI,yI,"]","[",xF,yF,"]")
img1 = cv2.imread("p5.jpg")

cv2.namedWindow("display")

cv2.setMouseCallback("display", dibujar)

while True:
    img2 = cv2.imread("p5.jpg")
    imagen = cv2.resize(img2, None, fx=1 / 2, fy=1 / 2, interpolation=cv2.INTER_AREA)
    if interruptor==True:
        cv2.rectangle(imagen,(xI,yI),(xF,yF),(255,0,0),2)

    cv2.imshow("display", imagen)
    k=cv2.waitKey(1)&0xff
    if k ==27:
        break
cv2.destroyAllWindows()
        