# importando as bibliotecas
import cv2
import numpy as np

# Especificando intervalos de cores superiores e inferiores para detectar no formato hsv
lower = np.array([15, 150, 20])
upper = np.array([35, 255, 255]) #(Esses intervalos detectarão Amarelo

# Capturando imagens da webcam
webcam_video = cv2.VideoCapture(0)

while True:
    success, video = webcam_video.read() #Lendo imagens da webcam

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Convertendo imagem BGR para o formato HSV

    mask = cv2.inRange(img, lower, upper) #Mascarando a imagem para encontrar nossa cor

    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # prucurando cores na mascara

    # Encontrando a posição de todos os contornos
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3) #desenhando ratangulo

    cv2.imshow("mask image", mask)#Exibindo a imagem da máscara

    cv2.imshow("window", video)#Exibindo a imagem da webcam+

    cv2.waitKey(1)
