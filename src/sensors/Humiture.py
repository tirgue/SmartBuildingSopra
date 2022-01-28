import RPi.GPIO as GPIO
import time
import json
import datetime
import os

class Humiture():
    def __init__(self):
        """Initialise a new humiture sensor

        Args:
            digitalChannel (int): the number of GPIO of the Raspberry PI on which the sensor is pluged on
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/../config/' + 'config.json') as file:
            config = json.load(file)
            self.ID = config['Capteurs']['Humiture']['ID']
            self.digitalChannel = config['Capteurs']['Humiture']['GPIO']

    def read(self):
        """Read the input and return the raw value"""
        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5
        MAX_UNCHANGE_COUNT = 100
        
        GPIO.setup(self.digitalChannel, GPIO.OUT)
        GPIO.output(self.digitalChannel, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(self.digitalChannel, GPIO.LOW)
        time.sleep(0.02)
        GPIO.setup(self.digitalChannel, GPIO.IN, GPIO.PUD_UP)
        
        unchanged_count = 0
        last = -1
        data = []
        while True:
            current = GPIO.input(self.digitalChannel)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > MAX_UNCHANGE_COUNT:
                    break

        state = STATE_INIT_PULL_DOWN

        lengths = []
        current_length = 0

        for current in data:
            current_length += 1

            if state == STATE_INIT_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_INIT_PULL_UP
                else:
                    continue
            if state == STATE_INIT_PULL_UP:
                if current == GPIO.HIGH:
                    state = STATE_DATA_FIRST_PULL_DOWN
                else:
                    continue
            if state == STATE_DATA_FIRST_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_DATA_PULL_UP
                else:
                    continue
            if state == STATE_DATA_PULL_UP:
                if current == GPIO.HIGH:
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN
                else:
                    continue
            if state == STATE_DATA_PULL_DOWN:
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP
                else:
                    continue
        if len(lengths) != 40:
            #print ("Data not good, skip")
            return None, None

        shortest_pull_up = min(lengths)
        longest_pull_up = max(lengths)
        halfway = (longest_pull_up + shortest_pull_up) / 2
        bits = []
        the_bytes = []
        byte = 0

        for length in lengths:
            bit = 0
            if length > halfway:
                bit = 1
            bits.append(bit)
        #print ("bits: %s, length: %d" % (bits, len(bits)))
        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0
        #print (the_bytes)
        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
            #print ("Data not good, skip")
            return None, None

        return the_bytes[0], the_bytes[2]

    def readHumidityAndTemperature(self):
        """Read the input and return the humidity expressed in % and the temperature expressed in Celcius
        Note: Need to wait at least 1 sec between 2 measurements"""
        return self.read()

    def export(self):
        try : 
            ts = datetime.datetime.now().timestamp()
            humidity, temperature = self.readHumidityAndTemperature()
            return json.dumps({"Humidity": humidity,"Temperature Celsius": temperature,"ID": self.ID,"Timestamp" : ts})
        except :
            ts = datetime.datetime.now().timestamp()
            return json.dumps({"Humidity": None,"Temperature Celsius": None,"ID": self.ID,"Timestamp" : ts})


if __name__ == "__main__":
    import time
    from datetime import datetime

    
    def setup():
        GPIO.setmode(GPIO.BCM)
    
    def loop():
        humiture = Humiture()
        while True:
            humidity, temperature = humiture.readHumidityAndTemperature()

            if humidity or temperature:
                print("*** %s ***" %datetime.now().strftime("%H:%M:%S"))

                print("Humidity : %s %%" %humidity)
                print("Celcius : %s °C" %temperature)

            time.sleep(1)

    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass    