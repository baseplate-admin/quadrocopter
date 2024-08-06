import math

# 57.3 = LSB/dp


def RP_calculate(x, y, z):
    roll = math.atan2(y, z) * 57.3
    pitch = math.atan2((-x), math.sqrt(y**2 + z**2)) * 57.3
    return roll, pitch
