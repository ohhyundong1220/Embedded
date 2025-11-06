import RPi.GPIO as GPIO
import serial
import threading
import time

SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

PWMA = 18
PWMB = 23
AIN1 = 22
AIN2 = 27
BIN1 = 25
BIN2 = 24

gData = ""

bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

def serial_thread():
	global gData
	while True:
		data = bleSerial.readline()	#1라인씩 읽어오기
		data = data.decode('utf-8', errors='ignore')	#수신시 오류가 발생할때가 있어 오류 무시 추가
		gData = data
		print("수신한 문자열:", gData)
		time.sleep(0.1)

def main():
	global gData

	#pin전포 저장 변수
	gpioPin = [18,23,22,27,25,24]

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	for i in gpioPin:
		GPIO.setup(i,GPIO.OUT)

	L_Moter = GPIO.PWM(gpioPin[0],500)
	L_Moter.start(0)

	R_Moter = GPIO.PWM(gpioPin[1],500)
	R_Moter.start(0)

	try:
		while True:
			if(gData == "go\r\n"):
				print("수행한 명령: GO")
				GPIO.output(gpioPin[2],0)
				GPIO.output(gpioPin[3],1)
				GPIO.output(gpioPin[4],0)
				GPIO.output(gpioPin[5],1)
				L_Moter.ChangeDutyCycle(100)
				R_Moter.ChangeDutyCycle(100)
				gData = ""
			elif(gData == "back\r\n"):
				print("수행한 명령: BACK")
				GPIO.output(gpioPin[2],1)
				GPIO.output(gpioPin[3],0)
				GPIO.output(gpioPin[4],1)
				GPIO.output(gpioPin[5],0)
				L_Moter.ChangeDutyCycle(100)
				R_Moter.ChangeDutyCycle(100)
				gData = ""
			elif(gData == "right\r\n"):
				print("수행한 명령: RIGHT")
				GPIO.output(gpioPin[2],0)
				GPIO.output(gpioPin[3],1)
				GPIO.output(gpioPin[4],0)
				GPIO.output(gpioPin[5],1)
				L_Moter.ChangeDutyCycle(100)
				R_Moter.ChangeDutyCycle(50)
				gData = ""
			elif(gData == "left\r\n"):
				print("수행한 명령: LEFT")
				GPIO.output(gpioPin[2],0)
				GPIO.output(gpioPin[3],1)
				GPIO.output(gpioPin[4],0)
				GPIO.output(gpioPin[5],1)
				L_Moter.ChangeDutyCycle(50)
				R_Moter.ChangeDutyCycle(100)
				gData = ""
			elif(gData == "stop\r\n"):
				print("수행한 명령: STOP")
				GPIO.output(gpioPin[2],0)
				GPIO.output(gpioPin[3],1)
				GPIO.output(gpioPin[4],0)
				GPIO.output(gpioPin[5],1)
				L_Moter.ChangeDutyCycle(0)
				R_Moter.ChangeDutyCycle(0)
				gData = ""
    
	except KeyboardInterrupt:
		L_Moter.stop(0)
		R_Moter.stop(0)
		pass

if __name__ == '__main__':
	#쓰레드 시작
	task1 = threading.Thread(target=serial_thread)
	task1.start()
	main()
	bleSerial.close()
	GPIO.cleanup()
