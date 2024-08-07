from machine import Pin, I2C
from micropython import const

I2C_ADDR = const(0x53)

regAddress = const(0x32)
TO_READ = 6
buff = bytearray(6)


class ADXL345:
    def __init__(self, scl, sda, i2c_id, addr=I2C_ADDR):
        self.addr = addr
        self.i2c = I2C(i2c_id, scl=Pin(scl), sda=Pin(sda), freq=100000)
        b = bytearray(1)
        b[0] = 0
        self.i2c.writeto_mem(self.addr, 0x2D, b)
        b[0] = 16
        self.i2c.writeto_mem(self.addr, 0x2D, b)
        b[0] = 8
        self.i2c.writeto_mem(self.addr, 0x2D, b)

        self.calibrated_values = {"x": 0, "y": 0, "z": 0}

    @property
    def x(self):
        buff = self.i2c.readfrom_mem(self.addr, regAddress, TO_READ)
        x = (int(buff[1]) << 8) | buff[0]
        if x > 32767:
            x -= 65536
        return x

    @property
    def y(self):
        buff = self.i2c.readfrom_mem(self.addr, regAddress, TO_READ)
        y = (int(buff[3]) << 8) | buff[2]
        if y > 32767:
            y -= 65536
        return y

    @property
    def z(self):
        buff = self.i2c.readfrom_mem(self.addr, regAddress, TO_READ)
        z = (int(buff[5]) << 8) | buff[4]
        if z > 32767:
            z -= 65536
        return z

    def calibrate(self):
        print("Calibrating accelerometer sensor")
        __x = 0
        __y = 0
        __z = 0
        for i in range(0, 10000):
            __x += self.x
            __y += self.y
            __z += self.z
            if i % 1000 == 0:
                print(".", end="")

        self.calibrated_values = {"x": __x / 10000, "y": __y / 10000, "z": __z / 10000}

    def mean(self):
        __x = self.x - self.calibrated_values["x"]
        __y = self.y - self.calibrated_values["y"]
        __z = self.z - self.calibrated_values["z"]

        if __x > 360:
            __x -= 360
        elif __x < -360:
            __x += 360

        if __y > 360:
            __y -= 360
        elif __y < -360:
            __y += 360

        if __z > 360:
            __z -= 360
        elif __z < -360:
            __z += 360
        return {
            "x": __x,
            "y": __y,
            "z": __z,
        }
