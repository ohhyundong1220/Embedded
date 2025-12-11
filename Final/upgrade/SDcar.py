import time
import RPi.GPIO as GPIO

#SW1 = 5 SW2 = 6 SW3 = 13 SW4 = 19 PWMA = 18 PWMB = 23 AIN1 = 22 AIN2 = 27 BIN1 = 25 BIN2 = 24
rLed = 16
lLed = 26
state = False

class Drive:
    def __init__(self):
        self.pins = [5,6,13,19,18,23,22,27,25,24]    
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12,GPIO.OUT) #부저 GPIO셋업
        GPIO.setup((rLed,lLed,21,20),GPIO.OUT) #LED GPIO셋업
        GPIO.setup(self.pins[0:4],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins[4:],GPIO.OUT)
        self.L_Motor = GPIO.PWM(self.pins[4],500)
        self.L_Motor.start(0)
        self.R_Motor = GPIO.PWM(self.pins[5],500)
        self.R_Motor.start(0)
        GPIO.output((rLed,lLed,21,20),0)

    def config_GPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins["SW1"],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins["SW2"],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins["SW3"],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins["SW4"],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins["PWMA"],GPIO.OUT)
        GPIO.setup(self.pins["AIN1"],GPIO.OUT)
        GPIO.setup(self.pins["AIN2"],GPIO.OUT)
        GPIO.setup(self.pins["PWMB"],GPIO.OUT)
        GPIO.setup(self.pins["BIN1"],GPIO.OUT)
        GPIO.setup(self.pins["BIN2"],GPIO.OUT)

    def clean_GPIO(self):
        GPIO.cleanup()
    
    def motor_go(self, speed):
        GPIO.output(self.pins[6],0)
        GPIO.output(self.pins[7],1)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.pins[8],0)
        GPIO.output(self.pins[9],1)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_back(self, speed):
        GPIO.output(self.pins[6],1)
        GPIO.output(self.pins[7],0)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.pins[8],1)
        GPIO.output(self.pins[9],0)
        self.R_Motor.ChangeDutyCycle(speed)
        
    def motor_left(self, speed):
        GPIO.output(self.pins[6],1)
        GPIO.output(self.pins[7],0)
        self.L_Motor.ChangeDutyCycle(speed-10)
        GPIO.output(self.pins[8],0)
        GPIO.output(self.pins[9],1)
        self.R_Motor.ChangeDutyCycle(speed)
    
    def motor_left_s(self, speed):
        GPIO.output(self.pins[6],0)
        GPIO.output(self.pins[7],1)
        self.L_Motor.ChangeDutyCycle(speed-15)
        GPIO.output(self.pins[8],0)
        GPIO.output(self.pins[9],1)
        self.R_Motor.ChangeDutyCycle(speed+15)
        
    def motor_right(self, speed):
        GPIO.output(self.pins[6],0)
        GPIO.output(self.pins[7],1)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.pins[8],1)
        GPIO.output(self.pins[9],0)
        self.R_Motor.ChangeDutyCycle(speed-10)
        
    def motor_right_s(self, speed):
        GPIO.output(self.pins[6],0)
        GPIO.output(self.pins[7],1)
        self.L_Motor.ChangeDutyCycle(speed+15)
        GPIO.output(self.pins[8],0)
        GPIO.output(self.pins[9],1)
        self.R_Motor.ChangeDutyCycle(speed-15)

    def motor_stop(self):
        GPIO.output(self.pins[6],0)
        GPIO.output(self.pins[7],1)
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.pins[8],0)
        GPIO.output(self.pins[9],1)
        self.R_Motor.ChangeDutyCycle(0)

    def stopsignal(self):
        global state
        p = GPIO.PWM(12,235)
        state = not state
        if state :
            GPIO.output((rLed,lLed,21,20),1)
            p.start(10)
            time.sleep(0.5)
        else :
            GPIO.output((rLed,lLed,21,20),0)
            p.stop()

    def stopsignalOFF(self):
        p = GPIO.PWM(12,235)
        GPIO.output((rLed,lLed,21,20),0)
        p.stop()

if __name__ == '__main__':

    drive = Drive()
    drive.motor_go(100)
    time.sleep(2)
    drive.motor_left(100)
    time.sleep(2)
    drive.motor_right(100)
    time.sleep(2)
    drive.motor_back(100)          
    time.sleep(2)
    drive.clean_GPIO()