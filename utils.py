import RPi.GPIO as IO
import time
import subprocess

IO.setmode(IO.BCM)


touch_pin = 25
pwm_pin = 17
ain_1_pin = 22
ain_2_pin = 27

slow_speed_frequency = 100
fast_speed_frequency = 300

def setup():
   slow_speed_frequency = 100
   fast_speed_frequency = 200

   IO.setup(pwm_pin, IO.OUT)
   IO.setup(ain_1_pin, IO.OUT)
   IO.setup(ain_2_pin, IO.OUT)
   IO.setup(touch_pin, IO.IN)

def spin_test():

   pulse = IO.PWM(pwm_pin, fast_speed_frequency) 
   IO.output(ain_1_pin, IO.HIGH)
   IO.output(ain_2_pin, IO.LOW)

   pulse.start(50)
   time.sleep(5)
   pulse.stop()


def spin_til_push():

   pulse = IO.PWM(pwm_pin, fast_speed_frequency) 
   pulse.start(45)
   time.sleep(1.5)
   while IO.input(touch_pin) == 0:
      continue
   pulse.stop()

def cleanup():
   IO.cleanup()

def take_photo():
   subprocess.check_call(["fswebcam", "/tmp/test.jpg"])

def display_photo():
   subprocess.check_call(["fbi", "/tmp/test.jpg"]) 

def focus_helper():
   while 1:
      take_photo()
      display_photo()

def roll_die():
   spin_til_push()
   take_photo()
   display_photo()

if __name__ == "__main__":
   setup()
   roll_die()
   cleanup()

