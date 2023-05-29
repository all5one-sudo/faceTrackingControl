import cv2
import dlib
import RPi.GPIO as GPIO # Librería para manejar los pines de la Raspberry Pi 4
from time import sleep

# Configurar los pines GPIO para el control del motor
ENA = 23 # ENA del A4988
STEP = 18 # Pin STEP, por cada pulso que le mando hace un paso
DIR = 4 # Este pin hace que gire en un sentido u otro

GPIO.setmode(GPIO.BCM) # Se usan los pines en formado Broadcom
# Setear los pines declarados como salidas
GPIO.setup(DIR, GPIO.OUT) 
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
# Se imprime un cero en ENA, esto es porque es activo por bajo
GPIO.output(ENA,GPIO.LOW)

# Delay entre pasos
delay = 0.002
# Error en pixeles
pixelError = 50

# Inicializo el cascade classifier de imagenes para OpenCV
faceCascade = cv2.CascadeClassifier('/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_default.xml')

# Dimensiones de la imagen de salida
OUTPUT_SIZE_WIDTH = 1280
OUTPUT_SIZE_HEIGHT = 720

# Función que se encarga de detectar la cara y trackearla
def trackFace():
    # Se inicializa la webcam de la posición 0, es decir, la que está por defecto
    sampleVideo = cv2.VideoCapture(0)
    # Se crea una ventana llamada "Reconocimiento" que mostrará la imagen con la cara remarcada
    cv2.namedWindow("Reconocimiento", cv2.WINDOW_AUTOSIZE)
    # Este es el faceTracker del paquete dlib
    tracker = dlib.correlation_tracker()
    # Se inicializa la variable a trackear en 0, posición inicial
    trackingFace = 0
    trackerColor = (0,165,255)
    xValueString = ''
    # Inicia el proceso de reconocimiento propiamente dicho
    try:
        '''Bucle infinito para que la imagen sea un stream, la excepción se lanza en el momento en
        que se aprieta Ctrl+C en terminal, y con eso salgo del bucle'''
        while True:
            # Se lee el último frame del video
            rc,fullImage = sampleVideo.read()
            # Se rota la imagen 180 grados para que se pueda montar la cámara al revés en el hardware prototipo
            fullImage = cv2.rotate(fullImage, cv2.ROTATE_180)
            # Para procesar de la mejor manera y optimizar recursos, se reescala la imagen
            originalImage = cv2.resize(fullImage,(480,320))
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
                for (_x,_y,_w,_h) in faces:
                    if  _w*_h > maxArea:
                        x = int(_x)
                        y = int(_y)
                        w = int(_w)
                        h = int(_h)
                        maxArea = w*h
                # Se elige a la cara de mayor área, ver tema de minimo reconocible
                if maxArea > 0 :
                    # Se inicializa el tracker
                    tracker.start_track(originalImage,dlib.rectangle((x-10),(y-20),(x+w+10),(y+h+20)))
                    # Se pone el tracker en True, para saber que se está trackeando una cara
                    trackingFace = 1
            # Se obtiene la posición de la cara
            '''xValue = ((x+(w/2))-640)*(1280/480)
            xValueString = 'X: ' + str(xValue)'''
            # Se comprueba si realmente se está trackeando una cara
            if trackingFace:
                # Se actualiza el tracker
                trackingQuality = tracker.update(originalImage)
                # Si la calidad del tracker es suficiente se obtienen las posiciones
                if trackingQuality >= 4:
                    tracked_position =  tracker.get_position()
                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())
                    # Obtenidas las posiciones, se puede imprimir la posición en el eje x
                    xValue = ((t_x+t_w/2)*(1280/480)-640) # convertir a radianes!
                    xValueString = 'X: ' + str(xValue.__round__(2))
                    cv2.rectangle(auxImage,(t_x, t_y),(t_x + t_w , t_y + t_h),trackerColor,2)
                else:
                    # Si la calidad no es suficiente, se vuelve a leer la imagen e intentar trackear
                    trackingFace = 0
                # El límite del pixelError es seteado en 200 a propósito en la etapa de pruebas para eliminar ruido
                # Si se detecta que la cara está a la derecha se mueve el motor en esa dirección
                '''if xValue < -pixelError:
                    GPIO.output(DIR,GPIO.HIGH)
                    GPIO.output(STEP, GPIO.HIGH)
                    sleep(delay)
                    GPIO.output(STEP, GPIO.LOW)
                    sleep(delay)
                # Si se detecta que la cara está a la izquierda se mueve el motor en la otra dirección
                elif xValue > pixelError:
                    GPIO.output(DIR,GPIO.LOW )
                    GPIO.output(STEP, GPIO.HIGH)
                    sleep(delay)
                    GPIO.output(STEP, GPIO.LOW)
                    sleep(delay)'''
                # Se llama a la funcion para rotar el motor
                rotateStepper(xValue)
            # Se reescala la imagen nuevamente
            largeResult = cv2.resize(auxImage,(OUTPUT_SIZE_WIDTH,OUTPUT_SIZE_HEIGHT))
            printImage = cv2.putText(largeResult, xValueString, (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255))
            # Se abre una ventana para mostrar la imagen con el rectángulo
            cv2.imshow("Reconocimiento", printImage)

    # El comando Ctrl+C termina el proceso
    except KeyboardInterrupt as e:
        cv2.destroyAllWindows()
        exit(0)

# Funcion que rota el paso a paso dependiendo del error medido por la camara
def rotateStepper(error):
    print('Rotando motor')
    # Se calculan cuantos pasos hay que ejecutar
    steps = round(18*abs(error)/240)
    # Dos casos, por si se tiene que girar en un sentido u otro
    if(error < 0):
        GPIO.output(DIR,GPIO.HIGH)
        i = 0
        while(i < steps):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
            i = i+1
    else:
        GPIO.output(DIR,GPIO.LOW)
        i = 0
        while(i < steps):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
            i = i+1

# Programa principal
if __name__ == '__main__':
    trackFace()
