# To establish I2C communication between Arduino
import smbus

# for RPI version 1, use ?bus = smbus.SMBus(0)?
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04


def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1


def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number


from time import sleep

import motor

m1 = motor.Motor([18, 21, 13])  # physical 12, 40, 33
m2 = motor.Motor([8, 19, 26])

motor.stop(m1, m2)

print "Commands"
print "E --> Exit"
print "F --> Forward"
print "L --> Left"
print "R --> Right"
print "B --> Back"
print "S --> Set Speed"

while True:
    inp = raw_input("Enter Command: ").strip()
    inp_p = inp.lower()
    if inp_p == 'E':
        break
    elif inp_p == "B":
        motor.back(m1, m2)
        sleep(2)
        motor.stop(m1, m2)
    elif inp_p == "F":
        motor.front(m1, m2)
        sleep(2)
        motor.stop(m1, m2)
    elif inp_p == "L":
        motor.turnLeft(m1, m2)
        sleep(2)
        motor.stop(m1, m2)
    elif inp_p == "R":
        motor.turnRight(m1, m2)
        sleep(2)
        motor.stop(m1, m2)
    elif inp_p == "S":
        speed = input("Enter Speed: ")
        writeNumber(speed)
