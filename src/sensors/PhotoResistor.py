#!/usr/bin/env python3
try:
    from . import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import datetime
import json

class PhotoResistor():
    	
    def __init__(self, analogChannel, digitalChannel):
        """Initialise a new analog PhotoResistor sensor

        Args:
            analogChannel (int): the number of the channel of the PCF8591 on which the sensor is pluged on
            digitalChannel (int): the number of GPIO of the Raspberry PI on which the sensor is pluged on

        Note: use constants from src.constants to simplify the initialisation (see example below)
        """
        self.analogChannel = analogChannel
        self.digitalChannel = digitalChannel
        GPIO.setup(digitalChannel, GPIO.IN)

    def read(self):
        """Read the input and return the raw value"""
        return ADC.read(self.analogChannel) 


    def export(self):
        ts = datetime.datetime.now().timestamp()
        return json.dumps({"Resistance": self.read(), "Timestamp": ts})



def setup():
	ADC.setup(0x48)
	GPIO.setmode(GPIO.BCM)


if __name__ == "__main__":
    import time

    AIN0 = 0        # Both need to be imported
    GPIO16 = 16     # from constants when used


    def loop():
        photoResistor = PhotoResistor(AIN0, GPIO16)
        while True:
            print(photoResistor.read())
            time.sleep(1)

    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass