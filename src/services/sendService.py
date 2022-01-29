import threading
from azure.iot.device import IoTHubDeviceClient, Message
 
CONNECTION_STRING = "HostName=test-hub-iot-sopra.azure-devices.net;DeviceId=test;SharedAccessKey=TNR/5rzIlvSpR5bwEQTFraUCEW2SY2G4vcuKfMltQ5I="

class sendService (threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        try:
            client = self.iothub_client_init()
        
            while True:
                item = self.queue.get()
                while True:
                    try:
                        print( "Sending message: {}".format(item) )
                        client.send_message(item)
                        print ( "Message successfully sent" )
                    except :
                        print( "Fail to send message: {}".format(item) )
                        continue
                    break
                self.queue.task_done()

        except :
            raise

    def iothub_client_init(self):
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        return client
