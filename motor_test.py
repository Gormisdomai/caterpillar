import RPi.GPIO as IO
import time
IO.setmode(IO.BCM)


pwm_pin = 17
ain_1_pin = 22
ain_2_pin = 27

slow_speed_frequency = 100
fast_speed_frequency = 200

IO.setup(pwm_pin, IO.OUT)
IO.setup(ain_1_pin, IO.OUT)
IO.setup(ain_2_pin, IO.OUT)


slow_speed_frequency = 100
fast_speed_frequency = 300

pulse = IO.PWM(pwm_pin, fast_speed_frequency) 

IO.output(ain_1_pin, IO.HIGH)
IO.output(ain_2_pin, IO.LOW)

pulse.start(50)
time.sleep(5)
pulse.stop()

IO.cleanup()
