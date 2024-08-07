from machine import I2C
import math
from micropython import const

MMC_ADDRESS = const(0x30)  # I2C address of MMC5883MC

COMPASS_CONFIG_REGISTER = const(0x08)
COMPASS_THRESHOLD_REGISTER = const(0x0B)
COMPASS_STATUS_REGISTER = const(0x07)
COMPASS_DATA_REGISTER = const(0x00)
Product_ID = const(0x2F)


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
        self.__xMax = 0
        self.__xMin = 0
        self.__yMax = 0
        self.__yMin = 0
        self.__zMax = 0
        self.__zMin = 0
        self.__x = 0.0
        self.__y = 0.0
        self.__z = 0.0
        self.angle = 0.0

        self.begin()

    def begin(self):
        self.write_byte(MMC_ADDRESS, COMPASS_CONFIG_REGISTER, COMPASS_CONFIG_REGISTER)
        self.ID = self.read_byte(MMC_ADDRESS, Product_ID)
        # print("ID = ", self.ID)

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
                self.__xMax = self.__xMin = sx
                self.__yMax = self.__yMin = sy
                self.__zMax = self.__zMin = sz

            self.__xMax = max(self.__xMax, sx)
            self.__xMin = min(self.__xMin, sx)
            self.__yMax = max(self.__yMax, sy)
            self.__yMin = min(self.__yMin, sy)
            self.__zMax = max(self.__zMax, sz)
            self.__zMin = min(self.__zMin, sz)

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
        self.__x = (
            2.0 * (float(self.sx - self.__xMin) / (self.__xMax - self.__xMin)) - 1.0
        )
        self.__y = (
            2.0 * (float(self.sy - self.__yMin) / (self.__yMax - self.__yMin)) - 1.0
        )
        self.__z = (
            2.0 * (float(self.sz - self.__zMin) / (self.__zMax - self.__zMin)) - 1.0
        )

    @property
    def x(self):
        self.update()
        return self.__x

    @property
    def y(self):
        self.update()
        return self.__y

    @property
    def z(self):
        self.update()
        return self.__z

    def getAngle(self):
        if self.__x != 0.0:
            if self.__x > 0.0:
                self.angle = 57.2958 * math.atan(self.__y / self.__x)
            elif self.__x < 0.0:
                if self.__y < 0.0:
                    self.angle = 57.2958 * math.atan(self.__y / self.__x) - 180.0
                else:
                    self.angle = 57.2958 * math.atan(self.__y / self.__x) + 180.0
        return self.angle

    def write_byte(self, addr, reg, data):
        self.i2c.writeto_mem(addr, reg, bytes([data]))

    def read_byte(self, addr, reg):
        return self.i2c.readfrom_mem(addr, reg, 1)[0]

    def read_bytes(self, addr, reg, count):
        return self.i2c.readfrom_mem(addr, reg, count)

    def combine_bytes(self, msb, lsb):
        return (msb << 8) + lsb
