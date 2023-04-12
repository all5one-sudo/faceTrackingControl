import RPi.GPIO as GPIO
import time

# Se definen los parametros del pwm a utilizar
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
# Se define el pin al que ira conectado el servo
servo = 23

def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

def setup():
    global p
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(servo, GPIO.OUT)  
    GPIO.output(servo, GPIO.LOW) 
    p = GPIO.PWM(servo, 50)     
    p.start(0)                    

def setAngle(angle):      
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)
    
def loop():
    while True:
        for i in range(0, 91, 5):   
            setAngle(i)    
            time.sleep(0.002)
        time.sleep(1)
        for i in range(90, -1, -5): 
            setAngle(i)
            time.sleep(0.001)
        time.sleep(1)
def destroy():
    p.stop()
    GPIO.cleanup()

if __name__ == '__main__':    
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()