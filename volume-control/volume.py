from RPi import GPIO
from time import sleep
import subprocess


clk = 5
dt = 6
btn = 26

# vals from output of amixer cget numid=1
min = 0
max = 255

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

isMuted = False
preVolume = volume = 125 # give it some volume to start with
clkLastState = GPIO.input(clk)
btnLastState = GPIO.input(btn)

subprocess.call(['amixer', '-q', '-c', '0', 'cset', 'numid=1', str(volume)])

try:
    while True:
        btnPushed = GPIO.input(btn)
        if ((not btnLastState) and btnPushed):
            if isMuted:
                volume = preVolume
                isMuted = False
                print ("Howie's Unmuted")
            else:
                preVolume = volume
                volume = 0
                isMuted = True
                print ("Howie's Muted")
            subprocess.call(['amixer', '-q', '-c', '0', 'cset', 'numid=1', str(volume)])
            sleep(0.05)
        else:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if isMuted:
                    isMuted = False
                    volume = 100
                if dtState != clkState:
                    volume += 5
                    if volume > max:
                        volume = max
                else:
                    volume -= 5
                    if volume < min:
                        volume = min
                print ("{:d} ({:.0%})".format(volume, float(volume)/float(max)))
                subprocess.call(['amixer', '-q', '-c', '0', 'cset', 'numid=1', str(volume)])
            clkLastState = clkState
        btnLastState = btnPushed
finally:
    GPIO.cleanup()
