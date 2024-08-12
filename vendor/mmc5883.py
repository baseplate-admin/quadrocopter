from machine import I2C, Pin
import time

MMC5883MA_I2C_ADDR = 0x30  # I2C address of the MMC5883MA sensor

# MMC5883MA Registers
MMC5883MA_XOUT0 = 0x00
MMC5883MA_XOUT1 = 0x01
MMC5883MA_YOUT0 = 0x02
MMC5883MA_YOUT1 = 0x03
MMC5883MA_ZOUT0 = 0x04
MMC5883MA_ZOUT1 = 0x05
MMC5883MA_STATUS = 0x07
MMC5883MA_CONTROL0 = 0x08
MMC5883MA_CONTROL1 = 0x09
MMC5883MA_PRODUCT_ID = 0x2F


class MMC5883MA:
    def __init__(
        self,
        scl,
        sda,
        i2c_id,
        addr=MMC5883MA_I2C_ADDR,
        hard_iron_offset=(0, 0, 0),
        soft_iron_matrix=None,
    ):
        self.i2c = I2C(i2c_id, scl=scl, sda=sda)
        self.addr = addr

        # Hard iron offsets (x_offset, y_offset, z_offset)
        self.hard_iron_offset = hard_iron_offset

        # Soft iron correction matrix (3x3 matrix)
        if soft_iron_matrix is None:
            # If not provided, use the identity matrix (no soft iron correction)
            self.soft_iron_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        else:
            self.soft_iron_matrix = soft_iron_matrix

        # Check the product ID
        product_id = self.i2c.readfrom_mem(self.addr, MMC5883MA_PRODUCT_ID, 1)[0]
        if product_id != 0x0C:
            raise ValueError("MMC5883MA not found")

        # Reset the sensor
        self.i2c.writeto_mem(self.addr, MMC5883MA_CONTROL1, b"\x80")
        time.sleep(0.01)

    def read_data(self):
        # Trigger a measurement
        self.i2c.writeto_mem(self.addr, MMC5883MA_CONTROL0, b"\x01")

        # Wait for the measurement to complete
        while not (self.i2c.readfrom_mem(self.addr, MMC5883MA_STATUS, 1)[0] & 0x01):
            time.sleep(0.001)

        # Read the X, Y, Z data
        data = self.i2c.readfrom_mem(self.addr, MMC5883MA_XOUT0, 6)

        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]

        # Convert to signed 16-bit integers
        x = self._convert_to_signed(x)
        y = self._convert_to_signed(y)
        z = self._convert_to_signed(z)

        # Apply hard iron offset correction
        x -= self.hard_iron_offset[0]
        y -= self.hard_iron_offset[1]
        z -= self.hard_iron_offset[2]

        # Apply soft iron correction
        x_corr = (
            x * self.soft_iron_matrix[0][0]
            + y * self.soft_iron_matrix[0][1]
            + z * self.soft_iron_matrix[0][2]
        )
        y_corr = (
            x * self.soft_iron_matrix[1][0]
            + y * self.soft_iron_matrix[1][1]
            + z * self.soft_iron_matrix[1][2]
        )
        z_corr = (
            x * self.soft_iron_matrix[2][0]
            + y * self.soft_iron_matrix[2][1]
            + z * self.soft_iron_matrix[2][2]
        )

        # Return the corrected data as a tuple
        return x_corr, y_corr, z_corr

    def _convert_to_signed(self, val):
        # Convert the unsigned 16-bit integer to signed
        if val >= 32768:
            return val - 65536
        else:
            return val

    def read_magnetic_field(self):
        # Read the corrected data
        x_corr, y_corr, z_corr = self.read_data()

        # Convert to microteslas (1 count = 0.25 uT)
        x_uT = x_corr * 0.25
        y_uT = y_corr * 0.25
        z_uT = z_corr * 0.25

        return x_uT, y_uT, z_uT
