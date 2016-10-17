import RPi.GPIO as GPIO             #importing GPIO library
import time                         #for delays
GPIO.setmode(GPIO.BCM)              #setting GPIO numbering; BCM sets it according to the Broadcom SOC Channel

TRIG = 23                           #pin 16
ECHO = 24                           #pin 18

print "Distance measurement in progress..."

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG,False)
print "Waiting for the sensor to settle"
time.sleep(2)                       #sleep for 2s

GPIO.output(TRIG, True)
time.sleep(0.00001)                 #pulse for 10us to trigger the sensor
GPIO.output(TRIG, False)

pulse_start = time.time()
while GPIO.input(ECHO)==0:
    pass
pulse_end = time.time()
pulse_duration = pulse_end - pulse_start

#Sound travels at ~343m/s
#34300cm/s = 2*distance/time
#So, distance = time*17150
distance = pulse_duration*17150
distance = round(distance,2)
print "Distance: ", distance, "cm"
print

GPIO.cleanup()
