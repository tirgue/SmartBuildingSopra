try:
    from . import PCF8591 as ADC
except:
    import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math 
from enum import Enum

class GAS(Enum):
    LPG = 0   
    CO = 1   
    SMOKE = 2   

class Gas():

    CALIBARAION_SAMPLE_TIMES=50
    CALIBRATION_SAMPLE_INTERVAL=100
    READ_SAMPLE_INTERVAL=20
    READ_SAMPLE_TIMES=5

    RL_VALUE=5
    RO_CLEAN_AIR_FACTOR=9.83

    LPGCurve = [2.3,0.21,-0.47]
    COCurve = [2.3,0.72,-0.34]
    SmokeCurve = [2.3,0.53,-0.44]

    Ro = 10

    def __init__(self, analogChannel, digitalChannel):
        self.analogChannel = analogChannel
        self.digitalChannel = digitalChannel
        GPIO.setup(analogChannel, GPIO.IN)
        print("Calibrating Gas Sensor...")
        self.Ro = self.calibrate()
        print("Calibration done, Ro :", self.Ro, "k")

    def read(self):
        v = ADC.read(self.analogChannel)
        return v

    def calibrate(self):
        val = 0

        for _ in range(self.CALIBARAION_SAMPLE_TIMES):
            val += self.__resistanceCalculation__(self.read())
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000)

        val = val/self.CALIBARAION_SAMPLE_TIMES
        val = val/self.RO_CLEAN_AIR_FACTOR
        return val;   

    def readRs(self):
        rs = 0

        for _ in range(self.READ_SAMPLE_TIMES):
            rs += self.__resistanceCalculation__(self.read())
            time.sleep(self.READ_SAMPLE_INTERVAL/1000)
        
        rs = rs/self.READ_SAMPLE_TIMES
        
        return rs;  

    def getGasConcentration(self, gasId):
        ratioRsRo = self.readRs()/self.Ro
        if gasId == GAS.LPG :
            return self.getConcentration(ratioRsRo, self.LPGCurve)
        if gasId == GAS.CO :
            return self.getConcentration(ratioRsRo, self.COCurve)
        if gasId == GAS.SMOKE :
            return self.getConcentration(ratioRsRo, self.SmokeCurve)
        
        return 0

    def getConcentration(self, rationRsRo, pcurve):
        return pow((math.log10(rationRsRo) - pcurve[1]) / pcurve[2] + pcurve[0], 10)

    def __resistanceCalculation__(self, rawAdc):
        return self.RL_VALUE*(1023-rawAdc)/rawAdc


if __name__ == "__main__":
    from datetime import datetime

    AIN1 = 1
    GPIO25 = 25

    def setup():
        GPIO.setmode(GPIO.BCM)
        ADC.setup(0x48)

    def loop():
        gasSensor = Gas(AIN1, GPIO25)
        while True:
            co = gasSensor.getGasConcentration(GAS.CO)
            lpg = gasSensor.getGasConcentration(GAS.LPG)
            smoke = gasSensor.getGasConcentration(GAS.SMOKE)

            print("*** %s ***" %datetime.now().strftime("%H:%M:%S"))

            print("CO :", co, "ppm")
            print("LPG :", lpg, "ppm")
            print("SMOKE :", smoke, "ppm")

            time.sleep(1)

    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass