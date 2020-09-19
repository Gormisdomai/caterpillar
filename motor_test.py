import RPi.GPIO as IO
import time

IO.setmode(IO.BCM)


pwm_pin = 17
ain_1_pin = 22
ain_2_pin = 27

touch_pin = 25

slow_speed_frequency = 100
fast_speed_frequency = 200

IO.setup(pwm_pin, IO.OUT)
IO.setup(ain_1_pin, IO.OUT)
IO.setup(ain_2_pin, IO.OUT)
IO.setup(touch_pin, IO.IN)

slow_speed_frequency = 100
fast_speed_frequency = 41


pulse = IO.PWM(pwm_pin, fast_speed_frequency)

IO.output(ain_1_pin, IO.HIGH)
IO.output(ain_2_pin, IO.LOW)

while 1:
    pulse.start(50)
    time.sleep(1.5)
    while IO.input(touch_pin) == 0:
        continue
    pulse.stop()
    time.sleep(6)

IO.cleanup()
