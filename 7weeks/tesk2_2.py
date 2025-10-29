import RPi.GPIO as GPIO
import time

BUZZER = 12
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER,GPIO.OUT)
GPIO.setup(SW1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

p = GPIO.PWM(BUZZER,262)

music = [262, 294, 330, 349, 392, 440, 494, 523]

while True:
	if GPIO.input(SW1)==1:
		mu = [7,6,7,3,2,1,0]
		p.start(50)
		for i in mu:
			p.ChangeFrequency(music[i])
			time.sleep(0.3)
		p.stop()

	elif GPIO.input(SW2)==1:
		mu = [2,1,0,1,2,2,2,1,1,1,2,4,4]
		p.start(50)
		for i in mu:
			p.ChangeFrequency(music[i])
			time.sleep(0.5)
		p.stop()
	
	elif GPIO.input(SW3)==1:
		mu = [0,0,4,4,5,5,4,3,3,2,2,1,1,0]
		p.start(50)
		for i in mu[:7]:
			p.ChangeFrequency(music[i])
			time.sleep(0.3)
		time.sleep(0.5)
		for i in mu[7:]:
			p.ChangeFrequency(music[i])
			time.sleep(0.3)
		p.stop()
	
	elif GPIO.input(SW4)==1:
		mu = [3,1,6,2,6,2,3,4,2,1,5,2,3,4,5]
		p.start(50)
		for i in mu:
			p.ChangeFrequency(music[i])
			time.sleep(0.2)
		p.stop()
