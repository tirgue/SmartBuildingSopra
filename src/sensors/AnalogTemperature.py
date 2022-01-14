try:
    from . import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
import math
import json
import datetime
import os

class AnalogTemperature():
    def __init__(self):
        """Initialise a new analog temperature sensor

        Args:
            analogChannel (int): the number of the channel of the PCF8591 on which the sensor is pluged on
            digitalChannel (int): the number of GPIO of the Raspberry PI on which the sensor is pluged on

        Note: use constants from src.constants to simplify the initialisation (see example below)
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/../config/' + 'config.json') as file:
            config = json.load(file)
            self.analogChannel = config['Capteurs']['AnalogTemperature']['AIN']
            self.digitalChannel = config['Capteurs']['AnalogTemperature']['GPIO']
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
            return json.dumps({"Temperature Kelvin": self.readKelvin(),"Temperature Celsius": self.readCelcius(), "Temperature Fahrenheit": self.readFahrenheit(), "Timestamp": ts})
        except : 
            ts = datetime.datetime.now().timestamp()
            return json.dumps({"Temperature Kelvin": None,"Temperature Celsius": None, "Temperature Fahrenheit": None, "Timestamp": ts})


def setup():
        GPIO.setmode(GPIO.BCM)
        ADC.setup(0x48)
if __name__ == "__main__":
    import time
    from datetime import datetime

   
    def setup():
        GPIO.setmode(GPIO.BCM)
        ADC.setup(0x48)

    def loop():
        analogTemperature = AnalogTemperature()
        while True:
            kelvin = round(analogTemperature.readKelvin(), 2)
            celcius = round(analogTemperature.readCelcius(), 2)
            fahrenheit = round(analogTemperature.readFahrenheit(), 2)

            print("*** %s ***" %datetime.now().strftime("%H:%M:%S"))

            print("Kelvin : %s K" %kelvin)
            print("Celcius : %s °C" %celcius)
            print("Fahrenheit : %s °F" %fahrenheit)

            time.sleep(1)

    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass