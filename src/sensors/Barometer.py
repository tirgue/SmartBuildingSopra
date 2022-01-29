import Adafruit_BMP.BMP085 as BMP085
import time
import datetime
import json
from services.configService import configService

class Barometer():
    def __init__(self):
        """Initialise a new pressure sensor

        Note: use constants from src.constants to simplify the initialisation (see example below)
        """
        self.sensor = BMP085.BMP085()
        self.configService = configService()
        self.config = self.configService.getConfig()
        
        self.ID = self.config['Capteurs']['Barometer']['ID']


    def readTemperature(self):
        return  self.sensor.read_temperature()	# Read temperature to veriable temp
    
    def readPressure(self):
        return self.sensor.read_pressure()	# Read pressure to veriable pressure
    
    def export(self):
        try : 
            ts = datetime.datetime.now().timestamp()
            return json.dumps({"Temperature Celsius": self.readTemperature(),"Pressure": self.readPressure(),"ID": self.ID, "Timestamp": ts})
        except : 
            ts = datetime.datetime.now().timestamp()
            return json.dumps({"Temperature Celsius": None,"Pressure": None,"ID": self.ID, "Timestamp": ts})



class BarometerBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        if self._instance:
            del self._instance
        self._instance = Barometer()
        return self._instance