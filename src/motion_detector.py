class MotionDetector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def direction(self):
        # (-10) - (-160) = Forward
        # 10 - 160 = Backward

        if (self.x > -10 and self.x < 10) and (self.y > -10 and self.y < 10):
            return "Stable"

        elif self.y < -10:
            return "Foward"
        elif self.y > 10 and self.x > -30:
            return "Backward"

        elif self.x < -10:
            return "Right"

        elif self.x > 10:
            return "Left"
