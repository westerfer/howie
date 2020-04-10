import RPi.GPIO as GPIO
import time
import os


s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10


def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  print("\n")
  




def loop():
  temp = 1
  while(1):  

    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration   
   
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration

    GPIO.output(s2,GPIO.HIGH)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    
      
    if green>red and blue<red and temp==0:
      print("red")
      os.system("mpc play 7")
      temp=0
    elif red<green and blue<green and temp==0:
      print("green")
      os.system("mpc play 4")
      temp=0
    elif green<blue and red<blue and temp==0:
       print("blue")
       os.system("mpc play 2")
       temp=0
    elif red>1000 and green>1000 and blue>1000 and temp==1:
      print("place the object.....")
      temp=0


def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
       loop()

    except KeyboardInterrupt:
       endprogram()
