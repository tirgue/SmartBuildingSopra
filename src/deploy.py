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
from persistqueue import Queue

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
instance_sensor = []





def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client
		
def setup():
    GPIO.setmode(GPIO.BCM)
    ADC.setup(0x48)

def get_message(q):

    try:
        setup()
        initialiseSensor()
       
        global instance_sensor
        
        while True:
            lock.acquire()
            for e in instance_sensor : 
                q.put(e.export())
            lock.release()
            time.sleep(SEND_DELAY)
 
    except :
        raise

def iothub_send_message(q):
 
    try:
        client = iothub_client_init()
        
        while True:
            item = q.get()
            while True:
                try:
                    print( "Sending message: {}".format(item) )
                    client.send_message(item)
                    print ( "Message successfully sent" )
                except :
                    print( "Fail to send message: {}".format(item) )
                    continue
                break
            q.task_done()

    except :
        raise
 
def handleConfigUpdate():

    try:
        InitialStamp = os.stat(dir_path + '/config/config.json').st_mtime
        
        while True:
            currentStamp = os.stat(dir_path + '/config/config.json').st_mtime
            if InitialStamp != currentStamp:
                lock.acquire()
                initialiseSensor()
                InitialStamp = currentStamp
                lock.release()
            time.sleep(1)
    except : 
        raise

"""
To initialize the right sensor instance
Have to be maintened frequently
"""
def initialiseSensor():
    with open(dir_path + '/config/' + 'config.json') as file:
        config = json.load(file)
        available_sensor = ["AnalogTemperature","Barometer","PhotoResistor","Gas","Humiditure"]
        global instance_sensor
        instance_sensor.clear()

        if "AnalogTemperature" in config["Capteurs"]:
            instance_sensor.append(AnalogTemperature())
        if "PhotoResistor" in config["Capteurs"]:
            instance_sensor.append(PhotoResistor())
        if "Gas" in config["Capteurs"]:
            instance_sensor.append(Gas())
        if "Humiture" in config["Capteurs"]:
            instance_sensor.append(Humiture())




if __name__ == '__main__':

    try:
        
        q = Queue(path="./persistance")
        t1 = threading.Thread(target=iothub_send_message,args=(q,))
        t2 = threading.Thread(target=handleConfigUpdate,args=())
        t3 = threading.Thread(target=get_message,args=(q,))

        t1.daemon=True
        t2.daemon=True
        t3.daemon=True

        t1.start()
        t2.start()
        t3.start()
        while True: time.sleep(5)
        
    except Exception as e: 
        print(str(e))
    finally : 
        print("end program")
