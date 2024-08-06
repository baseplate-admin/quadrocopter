from machine import Pin, I2C

I2C_ADDR = const(0x69)


class L3G4200:
    CTRL_REG1 = 0x20
    CTRL_REG2 = 0x21
    CTRL_REG3 = 0x22
    CTRL_REG4 = 0x23
    CTRL_REG5 = 0x24
    OUT_X_L = 0x28
    OUT_X_H = 0x29
    OUT_Y_L = 0x2A
    OUT_Y_H = 0x2B
    OUT_Z_L = 0x2C
    OUT_Z_H = 0x2D

    def __init__(self, scl, sda, i2c_id, address=I2C_ADDR, deg_sec=2000):
        self.i2c = I2C(i2c_id, scl=scl, sda=sda, freq=100000)
        self.address = address
        self.deg_sec = deg_sec
        self.dataL = bytearray(1)
        self.dataH = bytearray(1)

        # where device is i2c instance and deg_sec is dps (250, 500, 2000)
        self.i2c.writeto_mem(self.address, self.CTRL_REG1, bytearray([0b00001111]))

        self.i2c.writeto_mem(self.address, self.CTRL_REG2, bytearray([0b00000000]))

        self.i2c.writeto_mem(self.address, self.CTRL_REG3, bytearray([0b00001000]))

        if self.deg_sec == 250:
            self.i2c.writeto_mem(self.address, self.CTRL_REG4, bytearray([0b00000000]))
        elif self.deg_sec == 500:
            self.i2c.writeto_mem(self.address, self.CTRL_REG4, bytearray([0b00010000]))
        else:
            self.i2c.writeto_mem(self.address, self.CTRL_REG4, bytearray([0b00110000]))

        self.i2c.writeto_mem(self.address, self.CTRL_REG5, bytearray([0b00000000]))

    @staticmethod
    def __convert_val(n):
        # assign sign for 16 bit (65536) value
        if n > 32767:
            n -= 65536
        return n / 10  # convert to floating point number

    def __read_val(self, axisL, axisH):
        # reads registers and converts to human readable values
        self.i2c.readfrom_mem_into(self.address, axisL, self.dataL)
        self.i2c.readfrom_mem_into(self.address, axisH, self.dataH)
        val = self.__convert_val((self.dataH[0] << 8) | self.dataL[0])
        return val

    @property
    def xyz_values(self):
        # outputs dict of xyz values
        x = self.__read_val(self.OUT_X_L, self.OUT_X_H)
        y = self.__read_val(self.OUT_Y_L, self.OUT_Y_H)
        z = self.__read_val(self.OUT_Z_L, self.OUT_Z_H)
        return {"x": x, "y": y, "z": z}
