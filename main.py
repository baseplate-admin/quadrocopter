from machine import Pin
from vendor.bmp180 import BMP180
from vendor.adxl345 import ADXL345
from vendor.l3g4200 import L3G4200
from vendor.mmc5883 import MMC5883MA
from functions.calculator import RP_calculate
import time
from machine import Pin
led = Pin(25, Pin.OUT)

SCL_PIN = const(21)
SDA_PIN = const(20)
I2C_ID = const(0)

bmp180 = BMP180(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)

adxl345 = ADXL345(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)
# adxl345.calibrate()
m = MMC5883MA(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)
l3g4200d = L3G4200(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)


m.begin()
m.calibrate()
while True:
    led.toggle()

    print(m.readData())
    time.sleep(1)

# while True:
#     print(m.measure())
#     # time.sleep(1)
