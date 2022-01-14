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
import threading

try:
    from sensors import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
from azure.iot.device import IoTHubDeviceClient, Message
 
CONNECTION_STRING = "HostName=test-hub-iot-sopra.azure-devices.net;DeviceId=test;SharedAccessKey=TNR/5rzIlvSpR5bwEQTFraUCEW2SY2G4vcuKfMltQ5I="
SEND_DELAY = 5 
dir_path = os.path.dirname(os.path.realpath(__file__))
lock = threading.Lock()





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
       
        global analogTemperature,photoResistor,humiditure,gas
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
 
def handleConfigUpdate():

    try:
        InitialStamp = os.stat(dir_path + '/config/config.json').st_mtime


        while True:
            currentStamp = os.stat(dir_path + '/config/config.json').st_mtime
            print("On Test")
            if InitialStamp != currentStamp:
            
                lock.acquire()
                print("On entre")
                global analogTemperature,photoResistor,humiditure,gas
                
                del analogTemperature,photoResistor,humiditure,gas
                analogTemperature = AnalogTemperature()
                photoResistor = PhotoResistor()
                humiditure = Humiture()
                #barometer = Barometer()
                gas = Gas()
                InitialStamp = currentStamp
                lock.release()
            time.sleep(1)
    except : 
        raise

if __name__ == '__main__':

    try:
        
        
        t1 = threading.Thread(target=iothub_send_message,args=())
        t2 = threading.Thread(target=handleConfigUpdate,args=())

        t1.daemon=True
        t2.daemon=True

        t1.start()
        t2.start()
        while True: time.sleep(5)
        
    except Exception as e: 
        print(str(e))
    finally : 
        print("end program")
