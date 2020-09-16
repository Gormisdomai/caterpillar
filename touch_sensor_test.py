import RPi.GPIO as IO
import time
IO.setmode(IO.BCM)


touch_pin = 25 


IO.setup(touch_pin, IO.IN)


while 1:
   time.sleep(0.2)
   print(IO.input(touch_pin))

