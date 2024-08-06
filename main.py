from machine import Pin
from vendor.bmp180 import BMP180
from vendor.adxl345 import ADXL345
from vendor.l3g4200 import L3G4200

import time

SCL_PIN = const(21)
SDA_PIN = const(20)
I2C_ID = const(0)

bmp180 = BMP180(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)

adxl345 = ADXL345(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)
adxl345.calibrate()

l3g4200d = L3G4200(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)

while True:
    print(
        (
            adxl345.x,
            adxl345.y,
            adxl345.z,
        )
    )
    print(adxl345.mean())
    time.sleep(1)
    # print(bmp180.temperature)
