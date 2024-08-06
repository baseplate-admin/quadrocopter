from machine import Pin, I2C
from vendor.bmp180 import BMP180
from vendor.adxl345 import ADXL345
from vendor.l3g4200 import L3G4200
from src.motion_detector import MotionDetector


SCL_PIN = const(21)
SDA_PIN = const(20)
I2C_ID = const(0)

while True:
    bmp180 = BMP180(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)
    adxl345 = ADXL345(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)
    l3g4200d = L3G4200(sda=Pin(SDA_PIN),scl=Pin(SCL_PIN),i2c_id=I2C_ID)

    print(adxl345.xValue, adxl345.yValue, adxl345.zValue)
    print(adxl345.RP_calculate(adxl345.xValue, adxl345.yValue, adxl345.zValue))

    
    # print(bmp180.temperature)
