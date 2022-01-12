import time
import math
import json
import os 
from sensors.AnalogTemperature import AnalogTemperature
from sensors.Humiture import Humiture
from sensors.Barometer import Barometer
from sensors.PhotoResistor import PhotoResistor
from sensors.Gas import Gas
from constants.ADCPins import *
from constants.GPIOPins import *
import zmq

try:
    from sensors import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
from azure.iot.device import IoTHubDeviceClient, Message
 
CONNECTION_STRING = "HostName=test-hub-iot-sopra.azure-devices.net;DeviceId=test;SharedAccessKey=TNR/5rzIlvSpR5bwEQTFraUCEW2SY2G4vcuKfMltQ5I="
SEND_DELAY = 5 
PORT = 10219




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
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/config/' + 'config.json') as file:
            config = json.load(file)
            analogTemperature = AnalogTemperature()
            photoResistor = PhotoResistor()
            humiditure = Humiture()
            #barometer = Barometer()
            gas = Gas()
            while True:
                # Build the message with simulated telemetry values.
                time.sleep(0.1)
                
                temperatures = analogTemperature.export()
                temperatureAndHumiditure = humiditure.export()
                resistancePhotoResitor = photoResistor.export()
                #pressure = barometer.export()
                gasMeasure = gas.export()

                dataToSendToIotHub = [temperatures,temperatureAndHumiditure,resistancePhotoResitor,gasMeasure]

                for d in dataToSendToIotHub:
                    message = Message(d)
                    # Send the message.
                    print( "Sending message: {}".format(message) )
                    client.send_message(message)
                    print ( "Message successfully sent" )
                
                time.sleep(SEND_DELAY)
 
 
    except KeyboardInterrupt:
        raise
 
def handleConfigUpdate():

    try:
        while True:
            #  Wait for next request from client
            message = socket.recv()
            print("Received request: %s" % message)
            #  Send reply back to client
            socket.send_string("Ok")
    except : 
        raise

if __name__ == '__main__':

    try:
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:{}".format(PORT))
        iothub_send_message()
    except Exception as e: 
        print("kill")
    finally : 
        socket.close()
