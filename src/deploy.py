import time
import os 
from constants.ADCPins import *
from constants.GPIOPins import *
from services.configService import configService
from services.sensorServiceProvider import services
import threading
from persistqueue import Queue
from services.sendService import sendService

SEND_DELAY = 10 
lock = threading.Lock()
instance_sensor = []
configService0 = configService()
configService1 = configService()
print(configService0 == configService1)

def get_message(q):

    try:
        initialiseSensor()        
        while True:
            lock.acquire()
            for e in instance_sensor : 
                q.put(e.export())
            lock.release()
            time.sleep(SEND_DELAY)
 
    except :
        raise

def handleConfigUpdate():

    try:
        while True:
            if configService0.configWasUpdated():
                lock.acquire()
                initialiseSensor()
                lock.release()
            time.sleep(1)
    except : 
        raise

"""
To initialize the right sensor instance
Have to be maintened frequently
"""
def initialiseSensor():
        config = configService0.getConfig()
        global instance_sensor
        del instance_sensor[:]

        for key in config["Capteurs"]:
            try:
                instance_sensor.append(services.get(key))
            except Exception as e :
                print("can't instantiate : "+str(e))
                continue




if __name__ == '__main__':

    try:
        q = Queue(path="./persistance")
        t1 = sendService(q)
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
