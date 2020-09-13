import RPi.GPIO as IO
import time
import subprocess

IO.setmode(IO.BCM)


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


def spin():

   pulse = IO.PWM(pwm_pin, fast_speed_frequency) 
   IO.output(ain_1_pin, IO.HIGH)
   IO.output(ain_2_pin, IO.LOW)

   pulse.start(50)
   time.sleep(5)
   pulse.stop()

def cleanup():
   IO.cleanup()

def take_photo():
   subprocess.check_call(["fswebcam", "/tmp/test.jpg"])

def display_photo():
   subprocess.check_call(["fbi", "/tmp/test.jpg"]) 


if __name__ == "__main__":
   setup()
   spin()
   take_photo()
   display_photo()
   cleanup()

