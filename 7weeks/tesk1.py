import RPi.GPIO as GPIO
import time

SW = [5,6,13,19]
SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

click_counts = [0, 0, 0, 0]

last_states = [GPIO.input(pin) for pin in SW]

try:
    while True:
        current_states = [GPIO.input(pin) for pin in SW]

        for i in range(4):
            if last_states[i] == 0 and current_states[i] == 1:
                click_counts =+ 1

                print("SW%d click"%(i+1), click_counts)
        last_states = current_states
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
GPIO.cleanup()