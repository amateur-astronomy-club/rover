from time import sleep

import serial

import motor
from adapted import UltrasonicSensors

trigger_pins = [23, 24, 25, 12, 16, 20]  # physical 16,18,22,32,36,38
echo_pins = [4, 7, 27, 22, 5, 6]  # 7,11,13,15,29,31
m1 = motor.Motor([18, 21, 13])  # physical 12,40,33
m2 = motor.Motor([8, 19, 26])  # physical 24,35,37

frontRight = 0
frontLeft = 1
backRight = 2
backLeft = 3
front = 4
back = 5

clearance = 30

sensor = UltrasonicSensors(trigger_pins, echo_pins)
ser = serial.Serial('/dev/ttyACM0', 9600)


def loop():
    read_serial = ser.readline().strip()

    solar_panel_data, sensor_data = read_serial.split(';')

    data = solar_panel_data[1:].split("and")
    print int(data[0]), int(data[1])
    print sensor_data

while True:

    distance = [sensor.distance(i) for i in xrange(6)]
    for i in xrange(6):
        if distance[i] is None:
            distance[i] = 300

    if distance[front] > clearance and distance[frontLeft] > clearance and distance[frontRight] > clearance:
        motor.front(m1, m2)

    elif distance[frontRight] > distance[frontLeft]:
        if distance[frontRight] > clearance:
            motor.turnRight(m1, m2)
            sleep(2.5)
            motor.front(m1, m2)

    elif distance[frontLeft] > clearance:
        motor.turnLeft(m1, m2)
        sleep(2.5)
        motor.front(m1, m2)

    else:
        motor.back(m1, m2)
        sleep(5)
        if (distance[backRight] > distance[backLeft]) and distance[backRight] > clearance:
            motor.turnLeft(m1, m2)
            sleep(2.5)
            motor.front(m1, m2)
        elif distance[backLeft] > clearance:
            motor.turnRight(m1, m2)
            sleep(2.5)
            motor.front(m1, m2)

    loop()
