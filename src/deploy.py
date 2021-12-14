import time
import math


from azure.iot.device import IoTHubDeviceClient, Message
 
CONNECTION_STRING = "HostName=test-hub-iot-sopra.azure-devices.net;DeviceId=test;SharedAccessKey=TNR/5rzIlvSpR5bwEQTFraUCEW2SY2G4vcuKfMltQ5I="
 
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
            time.sleep(5)
 
 
    except KeyboardInterrupt:
        print ( "IoTHubClient stopped" )
 
if __name__ == '__main__':
    iothub_send_message()
