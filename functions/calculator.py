import math


def RP_calculate(x, y, z):
    roll = math.atan2(y, z) * 57.3
    pitch = math.atan2((-x), math.sqrt(y * y + z * z)) * 57.3
    return roll, pitch
