from machine import Pin, I2C
from vendor.bmp180 import BMP180
from vendor.adxl345 import ADXL345

SCL_PIN = const(15)
SDA_PIN = const(14)
I2C_ID = const(1)

while True:
    print(ADXL345(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID).xValue)
    print(BMP180(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID).temperature)
