import time
import math
from sensors.AnalogTemperature import AnalogTemperature
from sensors.Humiture import Humiture
from constants.ADCPins import *
from constants.GPIOPins import *
try:
    from sensors import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
from azure.iot.device import IoTHubDeviceClient, Message
 
CONNECTION_STRING = "HostName=test-hub-iot-sopra.azure-devices.net;DeviceId=test;SharedAccessKey=TNR/5rzIlvSpR5bwEQTFraUCEW2SY2G4vcuKfMltQ5I="
SEND_DELAY = 5 
MSG_TXT = '{{"Temperature Kelvin": {temperatureKelvin},"Temperature Celsius": {temperatureCelsius}, "Temperature Fahrenheit": {temperatureFahrenheit}}}'




def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client
		
def setup():
        GPIO.setmode(GPIO.BCM)
        ADC.setup(0x48)

def iothub_send_message():
 
    try:
        client = iothub_client_init()
        setup()
        analogTemperature = AnalogTemperature(AIN0, GPIO17)
        humiditure = Humiture(GPIO18)
        while True:
            # Build the message with simulated telemetry values.
            time.sleep(0.1)
            
            temperatures = analogTemperature.export()
            temperatureAndHumiditure = humiditure.export()

            dataToSendToIotHub = [temperatures,temperatureAndHumiditure]

            for d in dataToSendToIotHub:
                message = Message(d)
                # Send the message.
                print( "Sending message: {}".format(message) )
                client.send_message(message)
                print ( "Message successfully sent" )
              
            time.sleep(SEND_DELAY)
 
 
    except KeyboardInterrupt:
        print ( "IoTHubClient stopped" )
 


if __name__ == '__main__':

    iothub_send_message()
