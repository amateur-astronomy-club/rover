import serial
import serial.tools.list_ports

import motor2 as motor
from adapted import UltrasonicSensors

trigger_pins = [23, 24, 25, 12, 16, 20]  # physical 16,18,22,32,36,38
echo_pins = [4, 7, 27, 22, 5, 6]  # 7,11,13,15,29,31
m1 = motor.Motor([18, 21, 13])  # physical 12,40,33
m2 = motor.Motor([8, 19, 26])  # physical 24,35,37

FR = 0
FL = 1
BR = 2
BL = 3
F = 4
B = 5

clearance = 30

sensor = UltrasonicSensors(trigger_pins, echo_pins)

ports = list(serial.tools.list_ports.comports())

port_loc = None

for p in ports:
    if "2341" in p[2].lower():
        port_loc = p[0]

        print "Arduino Found!"
        break

if port_loc is None:
    raise Exception("Arduino not found.")

ser = serial.Serial(port_loc)

print "Connected to Arduino"


def loop():
    read_serial = ser.readline().strip()

    sensor_data, solar_panel_data = read_serial.split(';')

    print "Incident Radiation: ", sensor_data[-1:]
    print sensor_data


while True:

    distance = [sensor.distance(i) for i in xrange(6)]
    for i in xrange(6):
        if distance[i] is None:
            distance[i] = 300

    min_d = min(distance)

    if distance[FL] == min_d:
        if distance[F] >= distance[B]:
            motor.turnRightForward(m1, m2)
        else:
            motor.back(m1, m2)
    elif distance[FR] == min_d:
        if distance[F] >= distance[B]:
            motor.turnLeftForward(m1, m2)
        else:
            motor.back(m1, m2)
    elif distance[BL] == min_d:
        if distance[B] >= distance[F]:
            motor.turnLeftBackward(m1, m2)
        else:
            motor.front(m1, m2)
    elif distance[BR] == min_d:
        if distance[B] >= distance[F]:
            motor.turnRightBackward(m1, m2)
        else:
            motor.front(m1, m2)
    elif distance[B] == min_d:
        motor.front(m1, m2)
    elif distance[F] == min_d:
        motor.back(m1, m2)

    loop()
