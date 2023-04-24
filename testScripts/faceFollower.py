# Ejecutar: sudo pip3 install pigpio

import cv2
import dlib
import RPi.GPIO as GPIO
from time import sleep

# Configurar los pines GPIO para el control del motor
ENA = 23
IN1 = 24
IN2 = 25
STEP = 18
DIR = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

# Inicializar el controlador de motor Pololu DRV8825
from stepper_motor import StepperMotor

motor = StepperMotor(step_pin=STEP,
                     dir_pin=DIR,
                     enable_pin=ENA,
                     mode_pins=(0, 0, 0),
                     steps_per_rev=200)

# Inicializar el detector facial de DLib
detector = dlib.get_frontal_face_detector()

# Cargar el modelo predictor facial de DLib
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Inicializar la cámara web
cap = cv2.VideoCapture(0)

# Configurar el tamaño de la ventana de la cámara
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Configurar la velocidad de movimiento del motor
motor_speed = 50  # Velocidad en pasos por segundo

# Bucle principal
while True:
    # Capturar una imagen desde la cámara
    ret, frame = cap.read()

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en la imagen
    faces = detector(gray, 1)

    # Si se detectó una cara, mover el motor para mantenerla centrada
    if len(faces) > 0:
        # Calcular la posición de la cara en la imagen
        x1 = faces[0].left()
        y1 = faces[0].top()
        x2 = faces[0].right()
        y2 = faces[0].bottom()
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        w = x2 - x1
        h = y2 - y1

        # Calcular la diferencia en píxeles entre la posición de la cara y el centro de la imagen
        diff_x = cx - int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)

        # Mover el motor en la dirección adecuada para mantener la cara centrada
        if diff_x > 10:
            motor.rotate(-1, motor_speed)
        elif diff_x < -10:
            motor.rotate(1, motor_speed)

    # Mostrar la imagen en una ventana
    cv2.imshow("Frame", frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

# Detener el motor
motor.stop()
