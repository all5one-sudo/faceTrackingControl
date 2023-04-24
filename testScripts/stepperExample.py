#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# Se definen los pines a utilizar
out1 = 17
out2 = 18
out3 = 27
out4 = 22

# Tiempo de espera entre los pasos, hay que tener cuidado con este valor porque si es muy chico
# se puede estar sobrepasando un límite mecánico del motor
stepSleep = 0.01
# Número de pasos a realizar, para una vuelta entera se requieren 200 pasos
stepCount = 2000

# Se setean los diferentes pines (analogo a void setup de arduino)
GPIO.setmode(GPIO.BCM)
GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
GPIO.setup(out3, GPIO.OUT)
GPIO.setup(out4, GPIO.OUT)

# Se inicializan todas las salidas en 0 (low)
GPIO.output(out1, GPIO.LOW)
GPIO.output(out2, GPIO.LOW)
GPIO.output(out3, GPIO.LOW)
GPIO.output(out4, GPIO.LOW)


# Se limpian las salidas
def cleanup():
    GPIO.output(out1, GPIO.LOW)
    GPIO.output(out2, GPIO.LOW)
    GPIO.output(out3, GPIO.LOW)
    GPIO.output(out4, GPIO.LOW)
    GPIO.cleanup()


# Movimiento del stepper
try:
    i = 0
    for i in range(stepCount):
        if i % 4 == 0:
            GPIO.output(out4, GPIO.HIGH)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.LOW)
        elif i % 4 == 1:
            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.HIGH)
            GPIO.output(out1, GPIO.LOW)
        elif i % 4 == 2:
            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.HIGH)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.LOW)
        elif i % 4 == 3:
            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.HIGH)

        time.sleep(stepSleep)

except KeyboardInterrupt:
    cleanup()
    exit(1)

cleanup()
exit(0)
