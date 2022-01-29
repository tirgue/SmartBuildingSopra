try:
    from . import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
import math
import json
import datetime
from services.configService import configService


class AnalogTemperature():
    def __init__(self):
        """Initialise a new analog temperature sensor

        Args:
            analogChannel (int): the number of the channel of the PCF8591 on which the sensor is pluged on
            digitalChannel (int): the number of GPIO of the Raspberry PI on which the sensor is pluged on

        Note: use constants from src.constants to simplify the initialisation (see example below)
        """
        self.configService = configService()
        self.config = self.configService.getConfig()

        self.analogChannel = self.config['Capteurs']['AnalogTemperature']['AIN']
        self.ID = self.config['Capteurs']['AnalogTemperature']['ID']
        self.digitalChannel = self.config['Capteurs']['AnalogTemperature']['GPIO']
        GPIO.setup(self.digitalChannel, GPIO.IN)

    def read(self):
        """Read the input and return the raw value"""
        return ADC.read(self.analogChannel) 

    def readKelvin(self):
        """Read the input and return the temperature expressed in Kelvin"""
        analogVal = self.read()
        Vr = 5 * float(analogVal) / 255
        Rt = 10000 * Vr / (5 - Vr)
        temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
        return temp

    def readCelcius(self):
        """Read the input and return the temperature expressed in Celcius"""
        return self.readKelvin() - 273.15

    def readFahrenheit(self):
        """Read the input and return the temperature expressed in Fahrenheit"""
        return (self.readCelcius() * 9/5) + 32

    def export(self):
        try : 
            ts = datetime.datetime.now().timestamp()
            return json.dumps({"Temperature Kelvin": self.readKelvin(),"Temperature Celsius": self.readCelcius(), "Temperature Fahrenheit": self.readFahrenheit(), "ID" : self.ID, "Timestamp": ts})
        except : 
            ts = datetime.datetime.now().timestamp()
            return json.dumps({"Temperature Kelvin": None,"Temperature Celsius": None, "Temperature Fahrenheit": None, "ID": self.ID, "Timestamp": ts})

class AnalogTemperatureBuilder:
    
    def __init__(self):
        self._instance = None
        
    def __call__(self):
        
        if not self._instance:
            self._instance = AnalogTemperature()
        else :
            del self._instance
            self._instance = AnalogTemperature()
        return self._instance
    def __del__(self): 
        print("Destructor called, Example deleted.") 
