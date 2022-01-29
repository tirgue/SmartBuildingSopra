#!/usr/bin/env python3
try:
    from . import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import datetime
import json
from services.configService import configService

class PhotoResistor():
    	
    def __init__(self):
        """Initialise a new analog PhotoResistor sensor

        Args:
            analogChannel (int): the number of the channel of the PCF8591 on which the sensor is pluged on
            digitalChannel (int): the number of GPIO of the Raspberry PI on which the sensor is pluged on

        Note: use constants from src.constants to simplify the initialisation (see example below)
        """
        self.configService = configService()
        self.config = self.configService.getConfig()
        self.analogChannel = self.config['Capteurs']['PhotoResistor']['AIN']
        self.digitalChannel = self.config['Capteurs']['PhotoResistor']['GPIO']
        self.ID = self.config['Capteurs']['PhotoResistor']['ID']
        GPIO.setup(self.digitalChannel, GPIO.IN)

    def read(self):
        """Read the input and return the raw value"""
        return ADC.read(self.analogChannel) 


    def export(self):
        try :
            ts = datetime.datetime.now().timestamp()
            return json.dumps({"Resistance": self.read(),"ID": self.ID, "Timestamp": ts})
        except :
            ts = datetime.datetime.now().timestamp()
            return json.dumps({"Resistance": None,"ID": self.ID, "Timestamp": ts})



class PhotoResistorBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        if self._instance:
            del self._instance
        self._instance = PhotoResistor()
        return self._instance