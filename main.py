from machine import Pin
from vendor.bmp180 import BMP180
from vendor.adxl345 import ADXL345
from vendor.l3g4200 import L3G4200
from vendor.mmc5883 import MMC5883MA
import time
import math
from machine import Pin
from micropython import const

led = Pin(25, Pin.OUT)

SCL_PIN = const(21)
SDA_PIN = const(20)
I2C_ID = const(0)

bmp180 = BMP180(
    sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID
)  #  Pressure/Temperature/Altitude Sensor
adxl345 = ADXL345(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)  # accelerometer
mmc5883 = MMC5883MA(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)  # magnetometer
l3g4200d = L3G4200(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), i2c_id=I2C_ID)  # gyro


_interval = 1000  # 1ms = 1/.001 = 1000hz
delta_t = 1 / _interval

pitch = 0
roll = 0
yaw = 0

while True:
    # mmc5883.update()
    # accel_x, accel_y, accel_z = adxl345.x, adxl345.y, adxl345.z
    mag_x, mag_y, mag_z = mmc5883.read_magnetic_field()
    # gyro_x, gyro_y, gyro_z = (
    #     l3g4200d.xyz_values["x"],
    #     l3g4200d.xyz_values["y"],
    #     l3g4200d.xyz_values["z"],
    # )

    # omega_x = math.radians(gyro_x)
    # omega_y = math.radians(gyro_y)
    # omega_z = math.radians(gyro_z)

    # pitch_acc = math.atan2(accel_y, math.sqrt(accel_x**2 + accel_z**2))
    # roll_acc = math.atan2(-accel_x, accel_z)

    # m_x_corr = mag_x * math.cos(pitch_acc) + mag_z * math.sin(pitch_acc)
    # m_y_corr = (
    #     mag_x * math.sin(roll_acc) * math.sin(pitch_acc)
    #     + mag_y * math.cos(roll_acc)
    #     - mag_z * math.sin(roll_acc) * math.cos(pitch_acc)
    # )

    # yaw_mag = math.atan2(-m_y_corr, m_x_corr)

    # pitch_gyro = omega_y * delta_t
    # roll_gyro = omega_x * delta_t
    # yaw_gyro = omega_z * delta_t

    # pitch = pitch_acc
    # roll = roll_acc
    # yaw = yaw_mag

    # # Combine gyroscope data for relative changes
    # pitch += pitch_gyro
    # roll += roll_gyro
    # yaw += yaw_gyro

    # # Convert to degrees for readability
    # pitch_deg = math.degrees(pitch)
    # roll_deg = math.degrees(roll)
    # yaw_deg = math.degrees(yaw)

    # sleep_timer = _interval - int(time.ticks_ms() % _interval)

    print(mag_x, mag_y, mag_z)

    led.toggle()
    # time.sleep_ms(sleep_timer)
