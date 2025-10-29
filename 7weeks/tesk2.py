import RPi.GPIO as GPIO
import time

BUZZER = 12
SW1 = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER,GPIO.OUT)
GPIO.setup(SW1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

p = GPIO.PWM(BUZZER,262)
p.start(50)
tone = [262,294,330,349,392,440,494,523]

for i in tone:
	print(i)
	p.ChangeFrequency(i)
	time.sleep(1)

p.stop()

while True :
	if GPIO.input(SW1) == 1 :
		p.start(50)
		for x in range(3):
			for i in tone[::-4]:
				print(i)
				p.ChangeFrequency(i)
				time.sleep(0.5)
		p.stop()


p.stop()
GPIO.cleanup()
