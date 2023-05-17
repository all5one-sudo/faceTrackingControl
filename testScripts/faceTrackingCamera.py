import cv2
import dlib

# Inicializo el cascade classifier de imagenes para OpenCV
faceCascade = cv2.CascadeClassifier(
    '/Users/federicovillar/miniforge3/pkgs/libopencv-4.6.0-py310h5ab14b7_6/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
)

# Dimensiones de la imagen de salida
OUTPUT_SIZE_WIDTH = 1280
OUTPUT_SIZE_HEIGHT = 720


def detectFace():
    # Se inicializa la webcam de la posición 0, es decir, la que está por defecto
    sampleVideo = cv2.VideoCapture(0)
    # Se crea una ventana llamada "Reconocimiento" que mostrará la imagen con la cara remarcada
    cv2.namedWindow("Reconocimiento", cv2.WINDOW_AUTOSIZE)
    # Este es el faceTracker del paquete dlib
    tracker = dlib.correlation_tracker()
    # Se inicializa la variable a trackear en 0, posición inicial
    trackingFace = 0
    trackerColor = (0, 165, 255)
    xValueString = ''
    # Inicia el proceso de reconocimiento propiamente dicho
    try:
        '''Bucle infinito para que la imagen sea un stream, la excepción se lanza en el momento en
        que se aprieta Ctrl+C en terminal, y con eso salgo del bucle'''
        while True:
            # Se lee el último frame del video
            rc, fullImage = sampleVideo.read()
            # Para procesar de la mejor manera y optimizar recursos, se reescala la imagen
            originalImage = cv2.resize(fullImage, (480, 320))
            # Si se presiona Q se cierran todas las ventanas que estén abiertas
            # No logré que funcione sin esto, me parece que está demás
            pressedKey = cv2.waitKey(2)
            if pressedKey == ord('Q'):
                cv2.destroyAllWindows()
                exit(0)
            # Se crea una copia del último frame para dibujarle el rectángulo
            auxImage = originalImage.copy()
            # Si no se está trackeando ninguna cara, entonces se trata de buscar alguna
            if (not trackingFace):
                # Se pasa la imagen a escala de grises para el análisis
                grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
                # Se usa haarcascade para reconocer los rostros
                faces = faceCascade.detectMultiScale(grayImage, 1.3, 5)
                # Se inicializan las variables necesarias en 0
                maxArea = 0
                x = 0
                y = 0
                w = 0
                h = 0
                # Se calculan las áreas de las caras
                for (_x, _y, _w, _h) in faces:
                    if _w * _h > maxArea:
                        x = int(_x)
                        y = int(_y)
                        w = int(_w)
                        h = int(_h)
                        maxArea = w * h
                # Se elige a la cara de mayor área, ver tema de minimo reconocible
                if maxArea > 0:
                    # Se inicializa el tracker
                    tracker.start_track(
                        originalImage,
                        dlib.rectangle((x - 10), (y - 20), (x + w + 10),
                                       (y + h + 20)))
                    # Se pone el tracker en True, para saber que se está trackeando una cara
                    trackingFace = 1
            # Se obtiene la posición de la cara
            Value = ((x + (w / 2)) - 640) * (1280 / 480)
            '''xValueString = 'X: ' + str(xValue)'''
            # Se comprueba si realmente se está trackeando una cara
            if trackingFace:
                # Se actualiza el tracker
                trackingQuality = tracker.update(originalImage)
                # Si la calidad del tracker es suficiente se obtienen las posiciones
                if trackingQuality >= 8.75:
                    tracked_position = tracker.get_position()
                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())
                    # Obtenidas las posiciones, se puede imprimir la posición en el eje x
                    xValue = ((t_x + t_w / 2) * (1280 / 420) - 725
                              )  # convertir a radianes!
                    xValueString = 'X: ' + str(xValue.__round__(2))
                    cv2.rectangle(auxImage, (t_x, t_y), (t_x + t_w, t_y + t_h),
                                  trackerColor, 2)
            else:
                # Si la calidad no es suficiente, se vuelve a leer la imagen e intentar trackear
                trackingFace = 0
            # Se reescala la imagen nuevamente
            largeResult = cv2.resize(auxImage,
                                     (OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))
            printImage = cv2.putText(largeResult, xValueString, (200, 200),
                                     cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255))
            # Se abre una ventana para mostrar la imagen con el rectángulo
            cv2.imshow("Reconocimiento", printImage)

        # El comando Ctrl+C termina el proceso
    except KeyboardInterrupt as e:
        cv2.destroyAllWindows()
        exit(0)


# Programa principal
if __name__ == '__main__':
    detectFace()