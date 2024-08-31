from machine import Pin,PWM
import utime

MID = 1500000
MIN = 1000000
MAX = 2000000

led = Pin(25,Pin.OUT)
pwm = PWM(Pin(0))

pwm.freq(50)
pwm.duty_ns(MID)

while True:

    pwm.duty_ns(MAX)
    utime.sleep(10)