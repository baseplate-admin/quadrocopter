from machine import Pin, I2C
from vendor.bmp180 import BMP180
from vendor.adxl345 import ADXL345
from vendor.l3g4200 import L3G4200
from src.motion_detector import MotionDetector


SCL_PIN = const(15)
SDA_PIN = const(14)
I2C_ID = const(1)

while True:
    bmp180 = BMP180(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)
    adxl345 = ADXL345(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)
    l3g4200d = L3G4200(sda=Pin(SDA_PIN),scl=Pin(SCL_PIN),i2c_id=I2C_ID)
    print(l3g4200d.xyz_values())
    print(adxl345.xValue, adxl345.yValue, adxl345.zValue)
    print(MotionDetector(adxl345.xValue, adxl345.yValue, adxl345.zValue).direction)
    
    # print(bmp180.temperature)
