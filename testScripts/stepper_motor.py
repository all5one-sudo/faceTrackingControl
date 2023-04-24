import RPi.GPIO as GPIO
from time import sleep

class StepperMotor:
    def __init__(self, step_pin, dir_pin, enable_pin, mode_pins, steps_per_rev):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.mode_pins = mode_pins
        self.steps_per_rev = steps_per_rev
        
        # Configurar los pines GPIO para el control del motor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.mode_pins, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)
        GPIO.output(self.mode_pins, GPIO.LOW)

    def set_mode(self, mode):
        # Configurar el modo de paso del motor
        GPIO.output(self.mode_pins, mode)

    def rotate(self, direction, speed):
        # Rotar el motor en la dirección y velocidad especificadas
        if direction == 1:
            GPIO.output(self.dir_pin, GPIO.HIGH)
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)

        delay = 1 / (2 * self.steps_per_rev * speed)
        for i in range(200):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)

    def stop(self):
        # Detener el motor
        GPIO.output(self.enable_pin, GPIO.HIGH)
        GPIO.cleanup()
