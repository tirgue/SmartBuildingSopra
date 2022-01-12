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
import threading

try:
    from sensors import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
from azure.iot.device import IoTHubDeviceClient, Message
 
CONNECTION_STRING = "HostName=test-hub-iot-sopra.azure-devices.net;DeviceId=test;SharedAccessKey=TNR/5rzIlvSpR5bwEQTFraUCEW2SY2G4vcuKfMltQ5I="
SEND_DELAY = 2 
PORT = 10219
dir_path = os.path.dirname(os.path.realpath(__file__))

global config
global analogTemperature
global photoResistor
global humiditure
#global barometer = Barometer()
global gas



def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client
		
def setup():
    GPIO.setmode(GPIO.BCM)
    ADC.setup(0x48)

def iothub_send_message(lock):
 
    try:
        client = iothub_client_init()
        setup()
        with open(dir_path + '/config/' + 'config.json') as file:
            global config,analogTemperature,photoResistor,humiditure,gas
            config = json.load(file)
            analogTemperature = AnalogTemperature()
            photoResistor = PhotoResistor()
            humiditure = Humiture()
            #barometer = Barometer()
            gas = Gas()
            while True:
                lock.acquire()
                # Build the message with simulated telemetry values.                
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
                lock.release()
 
 
    except :
        raise
 
def handleConfigUpdate(lock):

    try:
        while True:
            #  Wait for next request from client
            message = socket.recv()
            print("Received request: %s" % message)
            with open(dir_path + '/config/' + 'config.json') as file:
                lock.acquire()
                global config,analogTemperature,photoResistor,humiditure,gas
                config = json.load(file)
                del analogTemperature,photoResistor,humiditure,gas
                analogTemperature = AnalogTemperature()
                photoResistor = PhotoResistor()
                humiditure = Humiture()
                #barometer = Barometer()
                gas = Gas()
                time.sleep(5)
                lock.release()
                socket.send_string("Ok")
    except : 
        raise

if __name__ == '__main__':

    try:
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:{}".format(PORT))
        lock = threading.Lock()
        t1 = threading.Thread(target=iothub_send_message,args=[lock])
        t2 = threading.Thread(target=handleConfigUpdate,args=[lock])

        t1.daemon=True
        t2.daemon=True

        t1.start()
        t2.start()
        while True: time.sleep(5)
        
    except Exception as e: 
        print(str(e))
    finally : 
        print("end program")

        socket.close()
