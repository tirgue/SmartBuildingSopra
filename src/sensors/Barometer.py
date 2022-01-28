import Adafruit_BMP.BMP085 as BMP085
import time
import datetime
import json
import os

class Barometer():
    def __init__(self):
        """Initialise a new pressure sensor

        Note: use constants from src.constants to simplify the initialisation (see example below)
        """
        self.sensor = BMP085.BMP085()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/../config/' + 'config.json') as file:
            config = json.load(file)
            self.ID = config['Capteurs']['Barometer']['ID']


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




def loop():
    while True:
        pressureSensor =  Barometer()
        print ('')
        print ('      Temperature = {0:0.2f} C'.format(pressureSensor.readTemperature()))		# Print temperature
        print ('      Pressure = {0:0.2f} Pa'.format(pressureSensor.readPressure()))	# Print pressure
        print(pressureSensor.export())
        time.sleep(1)			
        print ('')



if __name__ == '__main__':
	try:
		loop()
	except KeyboardInterrupt:
		pass