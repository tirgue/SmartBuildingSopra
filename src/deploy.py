import time
import math
from sensors.AnalogTemperature import AnalogTemperature
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
MSG_TXT = '{{"Temperature": {temperature}}}'




def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client
		

def iothub_send_message():
 
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
 
        while True:
            # Build the message with simulated telemetry values.
            time.sleep(0.1)
            
            msg_txt_formatted = "bonjour"
            message = Message(msg_txt_formatted)
 
              # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(SEND_DELAY)
 
 
    except KeyboardInterrupt:
        print ( "IoTHubClient stopped" )
 
def setup():
        GPIO.setmode(GPIO.BCM)
        ADC.setup(0x48)

if __name__ == '__main__':
    setup()
    analogTemperature = AnalogTemperature(AIN0, GPIO17)

    print(analogTemperature.export())
    iothub_send_message()
