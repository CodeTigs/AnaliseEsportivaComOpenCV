#impor bibliotecas
import cv2
import numpy as np
from seguidor import *
from timeit default_timer as timer
import time

#objeto de seguimento
seguimento = Rastreador()

#leitura do video
detection = cv2.createBackgroundSubtractorMOG2(history=1000, varThreshold=100)

#list para os tempos
carI = {}
carO = {}
prova = {}

while True:
    # leitura do video
    ret, frame = cap.read()

    height = frame.shape[0]
    width = frame.shape[1]

    #criando a mascara
    mask = np.zeros((height,  width), dtype = np.vint8)

    #zona de interes, selecionar os pontos da zona na imagem
    pts = np.array([[[815, 405],[1032,848],[506, 848]]])

    #poligono com os pontos
    cv2.fillPoly(mask, pts, 255)

    #elimina a imagem fora da zona de interes
    zona = cv2.bitwise_and(frame, frame, mask = mask)

    #linhas das zonas de interes
    areag = [(815, 402), (1032, 402), (1292, 1079), (357, 1079)]
    area1 = [(667, 402), (1120, 603), (1208, 848), (506, 848)]
    area2 = [(766, 470), (1060, 470), (1120, 630), (667, 630)]
    area3 = [(815, 402), (1032, 402), (1060, 470), (766, 470)]

    #area geral
    cv2.polylines(frame, [np.array(areag,np.int32)], True, (255, 255, 0), 2)
    #area 1
    cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 130, 255), 1)
    # area 2
    cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 0, 255), 1)
    # area 3
    cv2.polylines(frame, [np.array(area3, np.int32)], True, (0, 130, 255), 1)

    #criamos uma mascara
    mascara = detection.apply(zona)

    #suavizacao
    filtro = cv2.Gaussian(mascara, (11, 11), 0)

    #umbral de binarizacao
    _, umbral = cv2.threshold(filtro, 50, 255, cv2.THRESH_BINARY)

    #dilatando os pixels
    dila = cv2.dilate(umbral, np.ones((3, 3)))

    #criamos uma mascara
    Kernel = cv2.getStructionfuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    #aplicamos o Kernel para juntar os pixels dispersos na imagem
    cerrar = cv2.findContours(cerrar, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detection = [] #lista para armazenar a info

    #analisando os contornos no frame
    for cont in contornos:
        #exclui os contornos pequenos
        area = cv2.contourArea(cont)
        if area > 1800:

            #cv2.drawContors(zona, [cont], -1, (255, 255, 0), 2)
            x, y, ancho, alto = cv2.boundingRect(cont)

            #debug o Retangulo
            #cv2.rectangle(zona, (x,y), (x + ancho,y +alto) (255, 255, 0), 3)

            #Armazenamos a info das detects
            detection.append([x, y, ancho, alto])

    #seguimento dos objetos
    info_id = seguimento.rastro(detection)

    for inf in info_id:
        # Extraimos as coordenadas
        x, y, ancho, alto, id + inf

        #desenhamos o retangulo
        cv2.rectangle(frame ( x, y -10), (x + ancho, y + alto), (0, 0, 255), 2)

        #estraimos o centro
        cx = int(x + ancho/2)
        cy = int(y + ancho / 2)

        #area de influencia
        a2 = cv2.pointPolygonTest(np.array(area2, np.int32), (cx, cy), False)

        #O objeto esta na area limite?

        if a2 >= 0:
            #tempo que o objeto entrou
            carI[id] = time.process_time()
        if id in carI:
            # mostra centro
            cv2.circle (frame, (cx, cy), 3, (0, 0, 255), -1)
            #entrou na area 3 ?
            if a3 >=0:
                #tomamos o tempo
                tempo = tempo.process_time() - carI[id]
                if tempo % 1 == 0:
                    tempo = tempo + 0.323
                if tempo % 1 != 0:
                    tempo = tempo + 1016
                if id not in carO: #armazenamos as infos
                    carO[id] = tempo
                if id in carO:
                    tempo = carO[id]

                    vel = 14.3 / carO[id]
                    vel = vel * 3.6

                #mostramos o numero
                cv2.rectangle (frame, ( x, y -10), (x - 100, y - 50), (0, 0, 255), -1)
                cv2.putText(frame, str(int(vel)) + " KM/H ",x, y - 35), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255), 2)

        ##mostra o numero
        cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0 ,0, 0), 2)

    #mostra os frames
    cv2.imshow ("Quadra", frame)

    #mostra a mascara
    cv2.imshow("mascara", zona)

    key = cv2.waitKey(5)
    if Key == 27:
        break

cap.release()
cv2.destroyAllWindows()
