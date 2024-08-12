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


mmc5883.calibrate()


_interval = 1000  # 1ms = 1/.001 = 1000hz
delta_t = 1 / _interval

pitch = 0
roll = 0
yaw = 0

while True:
    mmc5883.update()
    accel_x, accel_y, accel_z = adxl345.x, adxl345.y, adxl345.z
    mag_x_raw, mag_y_raw, mag_z_raw = mmc5883.x, mmc5883.y, mmc5883.z
    gyro_x, gyro_y, gyro_z = (
        l3g4200d.xyz_values["x"],
        l3g4200d.xyz_values["y"],
        l3g4200d.xyz_values["z"],
    )
    
    # Hard iron offsets (determined during calibration)
    hard_iron_offset_x = 30.92
    hard_iron_offset_y = 42.60
    hard_iron_offset_z = -14.61

    # Soft iron correction matrix (determined during calibration)
    soft_iron_matrix = [
        [2.774, -1.258, 0.836],  # Scale x, no cross-coupling
        [-1.258, 1.227, -0.475],  # Scale y, no cross-coupling
        [0.836, -0.475, 0.0815]   # Scale z, no cross-coupling
    ]

    # Time interval (seconds)
    delta_t = 0.01

    # Convert gyroscope data from DPS to radians per second
    omega_x = math.radians(gyro_x)
    omega_y = math.radians(gyro_y)
    omega_z = math.radians(gyro_z)

    # Step 1: Hard Iron Calibration
    m_x_hard = mag_x_raw - hard_iron_offset_x
    m_y_hard = mag_y_raw - hard_iron_offset_y
    m_z_hard = mag_z_raw - hard_iron_offset_z

    # Step 2: Soft Iron Calibration using matrix multiplication
    m_x_soft = (
        soft_iron_matrix[0][0] * m_x_hard +
        soft_iron_matrix[0][1] * m_y_hard +
        soft_iron_matrix[0][2] * m_z_hard
    )

    m_y_soft = (
        soft_iron_matrix[1][0] * m_x_hard +
        soft_iron_matrix[1][1] * m_y_hard +
        soft_iron_matrix[1][2] * m_z_hard
    )

    m_z_soft = (
        soft_iron_matrix[2][0] * m_x_hard +
        soft_iron_matrix[2][1] * m_y_hard +
        soft_iron_matrix[2][2] * m_z_hard
    )

    # Calculate pitch and roll from accelerometer
    pitch = math.atan2(accel_y, math.sqrt(accel_x**2 + accel_z**2))
    roll = math.atan2(-accel_x, accel_z)

    # Adjust magnetometer readings using pitch and roll
    m_x_corr = m_x_soft * math.cos(pitch) + m_z_soft * math.sin(pitch)
    m_y_corr = (
        m_x_soft * math.sin(roll) * math.sin(pitch) +
        m_y_soft * math.cos(roll) -
        m_z_soft * math.sin(roll) * math.cos(pitch)
    )

    # Calculate yaw from corrected magnetometer data
    yaw = math.atan2(-m_y_corr, m_x_corr)

    # Integrate gyroscope data
    pitch_gyro = omega_y * delta_t
    roll_gyro = omega_x * delta_t
    yaw_gyro = omega_z * delta_t

    # Combine initial angles with gyroscope data
    pitch += pitch_gyro
    roll += roll_gyro
    yaw += yaw_gyro

    # Convert to degrees for readability
    pitch_deg = math.degrees(pitch)
    roll_deg = math.degrees(roll)
    yaw_deg = math.degrees(yaw)
    sleep_timer = _interval - int(time.ticks_ms() % _interval)

    print(pitch_deg, roll_deg, yaw_deg)

    led.toggle()
    #time.sleep_ms(sleep_timer)
