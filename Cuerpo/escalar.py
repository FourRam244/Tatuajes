# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 18:18:58 2022

@author: aleja
"""

import cv2
import numpy as np
import math

imagen = cv2.imread("barca.png",0)
cv2.imshow("Imagen", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()

#trasladar
ty = 10
tx = 10
trasladar = np.zeros((imagen.shape[0], imagen.shape[1]), dtype = np.uint8)

for i in range(imagen.shape[0]):
    for j in range(imagen.shape[1]):
        if i + ty < imagen.shape[0] and j + tx <imagen.shape[1]:
            trasladar[i+ty,j+tx] = imagen[i,j]
cv2.imshow("trasladar", trasladar)
cv2.waitKey(0)
cv2.destroyAllWindows()

#escalar

sx = 0.5
sy = 0.5
escalar = np.zeros((imagen.shape[0], imagen.shape[1]), dtype = np.uint8)
for i in range(imagen.shape[0]):
    for j in range(imagen.shape[1]):
        escalar[int(i*sy),int(j*sx)] = imagen[i,j]

NOT =cv2.bitwise_not(escalar)
cv2.imshow("escalar", NOT)
cv2.imwrite("escalado.png",NOT)
cv2.waitKey(0)
cv2.destroyAllWindows()

#rotar
rotar = np.zeros((imagen.shape[0], imagen.shape[1]), dtype = np.uint8)
angulo = 30

for i in range(imagen.shape[0]):
    for j in range(imagen.shape[1]):
        xr = abs(int(j*math.cos(math.pi/angulo) - i* math.sin(math.pi/angulo)))
        yr = abs(int(i*math.cos(math.pi/angulo) + j*math.sin(math.pi/angulo)))
        if xr > 0 and yr>0 and xr<imagen.shape[1] and yr<imagen.shape[0]:
            rotar[xr,yr] = imagen[i,j]
            
cv2.imshow("rotar", rotar)
cv2.waitKey(0)
cv2.destroyAllWindows()

