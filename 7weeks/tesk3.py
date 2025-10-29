import RPi.GPIO as GPIO
import time

gpioPin = [18,23,22,27,25,24]

swPin = [5,6,13,19]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for i in swPin:
	GPIO.setup(i,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
for i in gpioPin:
	GPIO.setup(i,GPIO.OUT)

L_Moter = GPIO.PWM(gpioPin[0],500)
L_Moter.start(0)

R_Moter = GPIO.PWM(gpioPin[1],500)
R_Moter.start(0)

try:
	for i in range(2):
		GPIO.output(gpioPin[2],0)
		GPIO.output(gpioPin[3],1)
		GPIO.output(gpioPin[4],0)
		GPIO.output(gpioPin[5],1)
		L_Moter.ChangeDutyCycle(50)
		R_Moter.ChangeDutyCycle(50)
		time.sleep(1)
		L_Moter.ChangeDutyCycle(0)
		R_Moter.ChangeDutyCycle(0)
		time.sleep(1)
	
	while True:
		if GPIO.input(swPin[0]) == 1:
			print("click SW1")
			GPIO.output(gpioPin[2],0)
			GPIO.output(gpioPin[3],1)
			GPIO.output(gpioPin[4],0)
			GPIO.output(gpioPin[5],1)
			L_Moter.ChangeDutyCycle(100)
			R_Moter.ChangeDutyCycle(100)
			time.sleep(2)
		elif GPIO.input(swPin[1]) == 1:
			print("click SW2")
			GPIO.output(gpioPin[2],0)
			GPIO.output(gpioPin[3],1)
			GPIO.output(gpioPin[4],0)
			GPIO.output(gpioPin[5],1)
			L_Moter.ChangeDutyCycle(100)
			R_Moter.ChangeDutyCycle(50)
			time.sleep(2)
		elif GPIO.input(swPin[2]) == 1:
			print("click SW3")
			GPIO.output(gpioPin[2],0)
			GPIO.output(gpioPin[3],1)
			GPIO.output(gpioPin[4],0)
			GPIO.output(gpioPin[5],1)
			L_Moter.ChangeDutyCycle(50)
			R_Moter.ChangeDutyCycle(100)
			time.sleep(2)			
		elif GPIO.input(swPin[3]) == 1:
			print("click SW4")
			GPIO.output(gpioPin[2],1)
			GPIO.output(gpioPin[3],0)
			GPIO.output(gpioPin[4],1)
			GPIO.output(gpioPin[5],0)
			L_Moter.ChangeDutyCycle(100)
			R_Moter.ChangeDutyCycle(100)
			time.sleep(2)
		else:
			L_Moter.ChangeDutyCycle(0)
			R_Moter.ChangeDutyCycle(0)

except KeyboardInterrupt:
	pass
GPIO.cleanup()