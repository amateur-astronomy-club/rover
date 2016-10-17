from time import time, sleep

import RPi.GPIO as GPIO


class UltrasonicSensors:
    """
    Example code which prints distance for 10 seconds for one sensor:

    u_sensor = UltrasonicSensor([23], [24])
    start_time = time()
    while time() - start_time < 10:
        print u_sensor.distance(0)
    u_sensor.reset()
    """

    def __init__(self, trigger_pins, echo_pins):
        """
        Setting GPIO numbering; BCM sets it according to the Broadcom SOC Channel
        and initialize Sensors
        :param trigger_pins:
        :param echo_pins:
        """

        self.trigger_pins = trigger_pins
        self.echo_pins = echo_pins

        GPIO.setmode(GPIO.BCM)

        for TRIG in trigger_pins:
            GPIO.setup(TRIG, GPIO.OUT)
        for ECHO in echo_pins:
            GPIO.setup(ECHO, GPIO.IN)

        for TRIG in trigger_pins:
            GPIO.output(TRIG, False)

        # print "Waiting for the sensor to settle"

        sleep(1)

    def reset(self):
        """
        Init has to be called after this.
        """
        GPIO.cleanup()

    def distance(self, sensor_number):
        """
        Returns distance on given sensor number. Returns None when out of range.
        :param sensor_number:
        :return:
        """
        trig = self.trigger_pins[sensor_number]
        echo = self.echo_pins[sensor_number]

        GPIO.output(trig, True)
        sleep(0.00001)  # pulse for 10us to trigger the sensor
        GPIO.output(trig, False)

        while GPIO.input(echo) == 0:
            pass
        pulse_start = time()
        while GPIO.input(echo) == 1:
            # print GPIO.input(ECHO)
            if time() - pulse_start > 0.03:
                return None

        else:
            pulse_end = time()
            pulse_duration = pulse_end - pulse_start

            # Sound travels at ~343m/s
            # 34300cm/s = 2*distance/time
            # So, distance = time*17150
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            return distance
