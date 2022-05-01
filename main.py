from rpi_ws281x import *
import time
import datetime
import RPi.GPIO as GPIO
import smbus
GPIO.setmode(GPIO.BCM)
TRIGGER_PIN = 21
ECHO_PIN = 20
HIGH_TIME = 0.1
LOW_TIME = 1 - HIGH_TIME
GPIO.setup(TRIGGER_PIN,GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
SPEED_OF_SOUND = 330/float(1000000)

address = 0x48
A3 = 0x43
bus = smbus.SMBus(1)

GPIO.setup(18,GPIO.OUT)
p = GPIO.PWM

p.start(50)

LED_COUNT = 16
LED_PIN = 12
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

r=0
g=0
b=0
max = 0

def getDistance(td):
  distance=SPEED_OF_SOUND*td/float(2)
  return distance
  
try:
  col = int(input("Enter color of choice: 1: blue 2: green 3: purple: "))
  
  if(col == 1):
    r=0
    g=0
    b=255
    
  elif(col == 2):
    r=0
    g=255
    b=0
    
  if(col == 3):
    r=76
    g=0
    b=153
    
  else:
    r=0
    g=255
    b=0
    
  while True:
    bus.write_byte(address,A3)
    val1 = bus.read_byte(address)
    val2 = (val1*3.3/255)
    
    print(val2)
    p.ChangeDutyCycle(val2)
    
    GPIO.output(TRIGGER_PIN,GPIO.HIGH)
    time.sleep(HIGH_TIME)
    GPIO.output(TRIGGER_PIN,GPIO.LOW)
    while GPIO.input(ECHO_PIN)==False:
      pass
    starttime = datetime.datetime.now().microsecond
    while GPIO.input(ECHO_PIN)==True:
      pass
    endtime = datetime.datetime.now().microsecond
    tavel_time = endtime - starttime
    
    strip = Adafruit_NeoPixel(LED_COUNT,LED_PIN,LED_FREQ_HZ,LED_DMA,LED_BRIGHTNESS,LED_INVERT,LED_CHANNEL)
    strip.begin()
    val = getDistance(travel_time)
    if(val < 0.04):
      if(val2<=5):
        strip.setPixelColor(0,Color(r,g,b))
        strip.setPixelColor(1,Color(r,g,b))
        strip.setPixelColor(2,Color(r,g,b))
        strip.setPixelColor(3,Color(r,g,b))
        strip.setPixelColor(4,Color(r,g,b))
        strip.setPixelColor(15,Color(0,0,0))
        strip.setPixelColor(14,Color(0,0,0))
        strip.setPixelColor(13,Color(0,0,0))
        strip.setPixelColor(12,Color(0,0,0))
      elif(val2>=6):
        strip.setPixelColor(0,Color(r,g,b))
        strip.setPixelColor(15,Color(r,g,b))
        strip.setPixelColor(14,Color(r,g,b))
        strip.setPixelColor(13,Color(r,g,b))
        strip.setPixelColor(12,Color(r,g,b))
        strip.setPixelColor(1,Color(0,0,0))
        strip.setPixelColor(2,Color(0,0,0))
        strip.setPixelColor(3,Color(0,0,0))
        strip.setPixelColor(4,Color(0,0,0))
      else:
        strip.setPixelColor(0,Color(r,g,b))
        strip.setPixelColor(1,Color(0,0,0))
        strip.setPixelColor(2,Color(0,0,0))
        strip.setPixelColor(3,Color(0,0,0))
        strip.setPixelColor(4,Color(0,0,0))
        strip.setPixelColor(15,Color(0,0,0))
        strip.setPixelColor(14,Color(0,0,0))
        strip.setPixelColor(13,Color(0,0,0))
        strip.setPixelColor(12,Color(0,0,0))
    else:
      for x in range(0,LED_COUNT):
        strip.setPixelColor(x,Color(255,0,0))
    strip.show()
    time.sleep(LOW_TIME)
except KeyboardInterrupt:
  pass
for x in range(0,LED_COUNT):
  strip.setPixelColor(x,Color(0,0,0))
p.stop()
GPIO.cleanup()
