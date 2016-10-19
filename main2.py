import math

import motor
from adapted import UltrasonicSensors

trigger_pins = [23, 24, 25, 12, 16, 20]  # physical 16,18,22,32,36,38
echo_pins = [4, 7, 27, 22, 5, 6]  # 7,11,13,15,29,31

memory = 100  # How many old values of sensor to store


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def map_to_1(distance):
    distance *= 2 / 100  # approx give 1 on sigmoid for distances 2.5m +
    return 2 - sigmoid(distance)  # give 1 for near 0 values and


class AutoPilot:
    def __init__(self):
        self.m1 = motor.Motor([18, 21, 13])  # physical 12,40,33
        self.m2 = motor.Motor([8, 19, 26])  # physical 24,35,37
        self.sensor = UltrasonicSensors(trigger_pins, echo_pins)
        self.old_values = [[0 for i in xrange(100)] for j in xrange(6)]
