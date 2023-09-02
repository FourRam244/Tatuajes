import cv2
import numpy as np
from PIL import Image
import sys
import os
cpr=cv2.imread("p9.jpg")#Parte del cuerpo
re = cv2.imread("d2.jpg") #Imagen a convertir dibujo
height, width = re.shape[:2]
image= cv2.resize(re, None, fx=3/4, fy=3/4, interpolation=cv2.INTER_AREA)
grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey)
blur=cv2.GaussianBlur(invert,(21,21),0)
invertedblur= cv2.bitwise_not(blur)
dibujo=cv2.divide(grey,invertedblur, scale=256.0)
cv2.imshow("Imagen",image)
cv2.imshow("Dibujo",dibujo)
#cv2.imwrite("dibujo.png",dibujo)
cv2.waitKey(0)

#segmentar
seg = cpr
seg2 = cv2.resize(seg, None, fx=1 / 2, fy=1 / 2, interpolation=cv2.INTER_AREA)
#Detectar color
hsv= cv2.cvtColor(seg2,cv2.COLOR_RGB2HSV)

lower_verde= np.array([245,255,221])
upper_verde= np.array([90,49,37])


mask=cv2.inRange(hsv,upper_verde, lower_verde)

piel=cv2.bitwise_and(seg2,seg2, mask = mask)
kernel = np.ones((6,6),np.uint8)
apertura=cv2.morphologyEx(piel,cv2.MORPH_CLOSE,kernel)
cv2.imshow("original",seg2)
cv2.waitKey(0)
cv2.imshow("HSV",hsv)
cv2.waitKey(0)
cv2.imshow("Final",mask)

cv2.waitKey(0)
#cv2.imshow("1",apertura)
cv2.imwrite("final.png",apertura)
cv2.waitKey(0)


#recorte
xI, yI, xF, yF = 0 ,0 ,0 ,0
interruptor =False

def dibujar(event ,x ,y ,flags ,param):
    global xI ,yI ,xF ,yF ,interruptor ,imagen
    if event == cv2.EVENT_LBUTTONDOWN:
        xI ,yI = x ,y
        interruptor =False

    if event == cv2.EVENT_LBUTTONUP:
        xF ,yF = x ,y
        interruptor =True
        recorte =imagen[yI:yF ,xI:xF ,:]

        cv2.imwrite("Recorte.png", recorte)

        print("coordenadas" ,"[" ,xI ,yI ,"]" ,"[" ,xF ,yF ,"]")
img1 = cv2.imread("p5.jpg")

cv2.namedWindow("Recortar")

cv2.setMouseCallback("Recortar", dibujar)

while True:
    img2 = cv2.imread("final.png")
    imagen = cv2.resize(img2, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    if interruptor==True:
        cv2.rectangle(imagen ,(xI ,yI) ,(xF ,yF) ,(255 ,0 ,0) ,2)

    cv2.imshow("Recortar", imagen)
    k=cv2.waitKey(1)&0xff
    if k ==27:
        break
cv2.destroyAllWindows()
#-------------------------------------------------------------------------
rt=1
while rt == 1:
    #rotacion de imagen
    print("Desea rotas la imagen?")
    opc = str(input("si o no?: "))
    if opc=="si" or opc=="SI" or opc=="sI" or opc=="Si":
        print("¿Cuantos grados desea rotar la imagen?")
        angulo = int(input())
        (h, w) = dibujo.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D((cX, cY), -angulo, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # calcular las nuevas dimensiones límite de la imagen
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # ajustar la matriz de rotación para tener en cuenta la traducción
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # realizar la rotación real y devolver la imagen
        rotado=cv2.warpAffine(dibujo, M, (nW, nH))
        # cv2.imshow ('imagen', imagen2) # Mostrar imagen
        # cv2.waitKey(0)
        #--------------------------------------------------
        #Quitar Fondo
        image = Image.fromarray(rotado)
        rgba = image.convert("RGBA")
        datas = rgba.getdata()

        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:  # encontrar el color negro por su valor RGB
                #
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        rgba.putdata(newData)
        rgba.save("dibujo2.png", "PNG")

        cv2.imshow("Dibujo rotado",rotado)
        cv2.imwrite('dibujo.png', rotado)


    #--------------------------------------------------------------------------
    #suma Imagenes
    rs = cv2.imread('recorte.png')
    img1 = cv2.imread('dibujo2.png')
    #plt.imshow(img1)
    #plt.show()
    #crop_img = img1[30:630, 150:400]
    #cv2.imwrite("recorte.png",crop_img)
    #print("tamaño",crop_img.shape)
    #r = cv2.imread('')

    invert2 = cv2.bitwise_not(rs)
    w=invert2.shape[1]
    h=invert2.shape[0]
    res = cv2.resize(invert2,(w,h), interpolation=cv2.INTER_CUBIC)
    res2 = cv2.resize(img1,(w,h), interpolation=cv2.INTER_CUBIC)
    resAW = cv2.subtract(res2,res)


    #Muestra final
    cv2.imshow('resAW',resAW)
    print("tamaño dibujo",resAW.shape)
    #Calcular medidas tatuaje
    a1=resAW.shape[1]
    a2=resAW.shape[0]
    ancho=(a1/96)/0.393701
    alto=(a2/96)/0.393701
    ancho=(ancho*2)-3
    alto=(alto*2)-3
    print("---------Tamaño del Tatuaje-----------")
    print("Ancho en px: ",a1,"px Ancho en cm: ",round(ancho,2),"cm")
    print("Alto en px: ",a2,"px Alto en cm: ",round(alto,2),"cm")
    #---------------------------------------------------
    final = cpr
    final2 = cv2.resize(final, None, fx=1/2, fy=1/2, interpolation=cv2.INTER_AREA)
    print("tamaño imagen",final2.shape)
    final2[yI:yF, xI:xF]=resAW
    cv2.imshow('resAW',final2)

    #cv2.imshow('recorte',invert2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Esta conforme con el diseño?")
    print("1)Si , 2)No")
    rt2 = str(input("Digite su respúesta: "))
    if rt2=="2" or rt2=="no" or rt2=="No" :
        rt==1
    if rt2=="1" or rt2=="si" or rt2=="Si":
        break
print("Fin")



