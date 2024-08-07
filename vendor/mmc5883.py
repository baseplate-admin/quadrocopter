from machine import I2C, Pin
import math
import time

MMC_ADDRESS = 0x30  # I2C address of MMC5883MC

COMPASS_CONFIG_REGISTER = 0x08
COMPASS_THRESHOLD_REGISTER = 0x0B
COMPASS_STATUS_REGISTER = 0x07
COMPASS_DATA_REGISTER = 0x00
Product_ID = 0x2F


class MMC5883MA:
    def __init__(
        self,
        scl,
        sda,
        i2c_id,
    ):
        self.i2c = I2C(i2c_id, scl=scl, sda=sda, freq=100000)
        self.ID = 0
        self.reg = 0
        self.xMax = 0
        self.xMin = 0
        self.yMax = 0
        self.yMin = 0
        self.zMax = 0
        self.zMin = 0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.angle = 0.0

    def begin(self):
        self.write_byte(MMC_ADDRESS, COMPASS_CONFIG_REGISTER, COMPASS_CONFIG_REGISTER)
        self.ID = self.read_byte(MMC_ADDRESS, Product_ID)
        print("ID = ", self.ID)

    def calibrate(self):
        count = 0
        print("Please wait until calibration is done!")
        while count < 10000:
            self.write_byte(MMC_ADDRESS, COMPASS_CONFIG_REGISTER, 1)
            while (self.reg & 1) == 0:
                self.reg = self.read_byte(MMC_ADDRESS, COMPASS_STATUS_REGISTER)

            data = self.read_bytes(MMC_ADDRESS, COMPASS_DATA_REGISTER, 6)
            sx, sy, sz = (
                self.combine_bytes(data[0], data[1]),
                self.combine_bytes(data[2], data[3]),
                self.combine_bytes(data[4], data[5]),
            )

            if count == 0:
                self.xMax = self.xMin = sx
                self.yMax = self.yMin = sy
                self.zMax = self.zMin = sz

            self.xMax = max(self.xMax, sx)
            self.xMin = min(self.xMin, sx)
            self.yMax = max(self.yMax, sy)
            self.yMin = min(self.yMin, sy)
            self.zMax = max(self.zMax, sz)
            self.zMin = min(self.zMin, sz)

            if (count % 1000) == 0:
                print(".", end="")
            count += 1
        print(".")

    def update(self):
        self.reg = 0
        self.write_byte(MMC_ADDRESS, COMPASS_CONFIG_REGISTER, 1)
        while (self.reg & 1) == 0:
            self.reg = self.read_byte(MMC_ADDRESS, COMPASS_STATUS_REGISTER)

        data = self.read_bytes(MMC_ADDRESS, COMPASS_DATA_REGISTER, 6)
        self.sx, self.sy, self.sz = (
            self.combine_bytes(data[0], data[1]),
            self.combine_bytes(data[2], data[3]),
            self.combine_bytes(data[4], data[5]),
        )

        if self.xMax != self.xMin:
            self.x = 2.0 * (float(self.sx - self.xMin) / (self.xMax - self.xMin)) - 1.0
        else:
            self.x = 0.0

        if self.yMax != self.yMin:
            self.y = 2.0 * (float(self.sy - self.yMin) / (self.yMax - self.yMin)) - 1.0
        else:
            self.y = 0.0

        if self.zMax != self.zMin:
            self.z = 2.0 * (float(self.sz - self.zMin) / (self.zMax - self.zMin)) - 1.0
        else:
            self.z = 0.0

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getAngle(self):
        if self.x != 0.0:
            if self.x > 0.0:
                self.angle = 57.2958 * math.atan(self.y / self.x)
            elif self.x < 0.0:
                if self.y < 0.0:
                    self.angle = 57.2958 * math.atan(self.y / self.x) - 180.0
                else:
                    self.angle = 57.2958 * math.atan(self.y / self.x) + 180.0
        return self.angle

    def readData(self):
        self.update()
        return f"Mag X:{self.x}\tY:{self.y}\tZ:{self.z}"

    def write_byte(self, addr, reg, data):
        self.i2c.writeto_mem(addr, reg, bytes([data]))

    def read_byte(self, addr, reg):
        return self.i2c.readfrom_mem(addr, reg, 1)[0]

    def read_bytes(self, addr, reg, count):
        return self.i2c.readfrom_mem(addr, reg, count)

    def combine_bytes(self, msb, lsb):
        return (msb << 8) + lsb


# Example usage:
# i2c = I2C(0, scl=Pin(21), sda=Pin(20))
