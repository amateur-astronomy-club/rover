import motor
from time import sleep

m1 = motor.Motor([18, 21, 13])  # physical 12, 40, 33
m2 = motor.Motor([8, 19, 26])

print "Commands"
print "E --> Exit"
print "F --> Forward"
print "L --> Left"
print "R --> Right"
print "B --> Back"

while True:
    inp = raw_input("Enter Command: ").strip()
    inp_p = inp.lower()
    if inp_p == 'E':
        break
    elif inp_p == "B":
        motor.back(m1, m2)
        sleep(2)
    elif inp_p == "F":
        motor.front(m1, m2)
        sleep(2)
    elif inp_p == "L":
        motor.turnLeft(m1, m2)
        sleep(2)
    elif inp_p == "R":
        motor.turnRight(m1, m2)
        sleep(2)
