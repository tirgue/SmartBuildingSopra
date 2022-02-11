from sensors.AnalogTemperature import AnalogTemperatureBuilder
from sensors.Humiture import HumitureBuilder
from sensors.Barometer import BarometerBuilder
from sensors.PhotoResistor import PhotoResistorBuilder
from sensors.Gas import GasBuilder
try:
    from sensors import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
import factory.objectFactory as objectFactory

class SensorServiceProvider(objectFactory.ObjectFactory):
    def get(self, sensor):
        return self.create(sensor)
    

def setup():
    GPIO.setmode(GPIO.BCM)
    ADC.setup(0x48)

setup()
services = SensorServiceProvider()
services.register_object('AnalogTemperature', AnalogTemperatureBuilder())
services.register_object('Humiture', HumitureBuilder())
#services.register_object('Barometer', BarometerBuilder())
services.register_object('PhotoResistor', PhotoResistorBuilder())
services.register_object('Gas', GasBuilder())