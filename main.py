from machine import Pin
from vendor.bmp180 import BMP180
from vendor.adxl345 import ADXL345
from vendor.l3g4200 import L3G4200
from functions.calculator import RP_calculate
import time

SCL_PIN = const(21)
SDA_PIN = const(20)
I2C_ID = const(0)

bmp180 = BMP180(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)

adxl345 = ADXL345(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)
# adxl345.calibrate()

l3g4200d = L3G4200(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)


while True:
    print(
        RP_calculate(
            l3g4200d.xyz_values["x"], l3g4200d.xyz_values["y"], l3g4200d.xyz_values["z"]
        )
    )
    time.sleep(1)
    