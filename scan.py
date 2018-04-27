# coding: utf-8

# import the necessary packages
from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filters import threshold_adaptive

from lcd_module.main_lcd import write_lcd

import cv2
import os
from scipy import ndimage
import time


def start_camera(ind, width=1280, height=720):
    # Try to start the camera
    cap = cv2.VideoCapture(ind)
    print('Starting the camera...')
    write_lcd('Starting the\ncamera...')
    inicio = time.time()
    while not cap.isOpened():
        cap = cv2.VideoCapture(ind)
    print('Segundos para iniciar a câmera: {}'.format(time.time() - inicio))

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return cap


def captura_imagem(cap):
    while True:
        _, frame = cap.read()
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(33)
        # Capture and show the frame
        if key & 0xFF == ord('c'):
            cv2.imshow('Captura', frame)

            # Save the frame
            if cv2.waitKey(0) & 0xFF == ord('s'):
                # salva_imagem(frame)
                cv2.destroyWindow('Captura')
                cap.release()
                return frame
            else:
                cv2.destroyWindow('Captura')
        elif key & 0xFF == 27:
            cv2.destroyAllWindows()
            cap.release()
            # break
            return None


def salva_imagem(frame):
    print('Salvando...')
    filename = 'foto_' + str(time.time()) + '.jpg'
    print(filename)
    # Verify the filename already exists
    if os.path.exists(filename):
        filename = 'foto_' + str(time.time()) + '.jpg'
        cv2.imwrite(filename, frame)
    else:
        cv2.imwrite(filename, frame)


def detecta_bordas(image):
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # show the original image and the edge detected image
    print("STEP 1: Edge Detection")
    # cv2.imshow("Image", image)
    # cv2.imshow("Edged", edged)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            return screenCnt
        else:
            return None


def desenha_contornos(screenCnt):
    # show the contour (outline) of the piece of paper
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    # cv2.imshow("Outline", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def aplica_filtros(img_filtered):
    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # Copia a imagem para aplicar o filtro adptiveThreshold
    img_filtered = warped.copy()

    img_filtered_gray = cv2.cvtColor(img_filtered, cv2.COLOR_BGR2GRAY)
    img_filtered_blur = cv2.GaussianBlur(img_filtered_gray, (3, 3), 0)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_filtered_clahe = clahe.apply(img_filtered_blur)

    # img_filtered_clahe_rotated = ndimage.rotate(img_filtered_clahe, 90)

    # cv2.namedWindow('CLAHE', cv2.WINDOW_GUI_EXPANDED)
    # cv2.imshow('CLAHE',img_filtered_clahe_rotated)

    img_filtered_thresh = cv2.adaptiveThreshold(img_filtered_clahe, 255,
                                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, 11, 3)

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    # warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    # warped = threshold_adaptive(warped, 251, offset=10)
    # warped = warped.astype("uint8") * 255

    # Rotaciona a imagem em 90 graus
    # warped_rotated = ndimage.rotate(warped, 90)
    # img_filtered_rotated = ndimage.rotate(img_filtered_thresh, 90)


if __name__ == '__main__':

    # Start camera
    cap = start_camera(0)
    frame = captura_imagem(cap)

    if frame is not None:
        image = frame.copy()
    else:
        image = cv2.imread('images/recipe.jpg')
    # image = cv2.imread('images/recipe.jpg')

    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    # image = cv2.imread('images/recipe.jpg')

    # show the original and scanned images
    # print("STEP 3: Apply perspective transform")
    # cv2.namedWindow("Original", cv2.WINDOW_GUI_NORMAL)
    # cv2.imshow("Original", orig)
    # cv2.imshow("Scanned", imutils.resize(warped, height = 650))
    # cv2.imshow("Rotacionada", imutils.resize(warped_rotated, height = 650))
    # cv2.namedWindow('Filtro Adaptativo Gaussiano', cv2.WINDOW_GUI_EXPANDED)
    # cv2.imshow("Filtro Adaptativo Gaussiano", imutils.resize(img_filtered_rotated, height = 650))
    cv2.imshow("Filtro Adaptativo Gaussiano", img_filtered_thresh)

    while True:
        key = cv2.waitKey(33)
        if key & 0xFF == 27:
            cv2.destroyAllWindows()
