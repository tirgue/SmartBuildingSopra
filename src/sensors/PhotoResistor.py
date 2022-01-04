#!/usr/bin/env python3
try:
    from . import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import datetime
import json
import os

class PhotoResistor():
    	
    def __init__(self):
        """Initialise a new analog PhotoResistor sensor

        Args:
            analogChannel (int): the number of the channel of the PCF8591 on which the sensor is pluged on
            digitalChannel (int): the number of GPIO of the Raspberry PI on which the sensor is pluged on

        Note: use constants from src.constants to simplify the initialisation (see example below)
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/../config/' + 'config.json') as file:
            config = json.load(file)
            self.analogChannel = config['Capteurs']['PhotoResistor']['AIN']
            self.digitalChannel = config['Capteurs']['PhotoResistor']['GPIO']
            GPIO.setup(self.digitalChannel, GPIO.IN)

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




    def loop():
        photoResistor = PhotoResistor()
        while True:
            print(photoResistor.read())
            time.sleep(1)

    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass