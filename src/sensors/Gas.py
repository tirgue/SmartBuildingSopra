try:
    from . import PCF8591 as ADC
except:
    import PCF8591 as ADC
from typing import Dict, List
import RPi.GPIO as GPIO
import time
import math 
from enum import Enum

class GAS(Enum):
    LPG = 0   
    CO = 1   
    SMOKE = 2   

class Gas():

    CALIBRATION_SAMPLE_TIMES=50
    CALIBRATION_SAMPLE_INTERVAL=100
    READ_SAMPLE_INTERVAL=20
    READ_SAMPLE_TIMES=5

    RL_VALUE=5
    RO_CLEAN_AIR_FACTOR=9.83

    LPGCurve = {
        "a": -0.47,
        "b": 1.31,
    }
    COCurve = {
        "a": -0.32,
        "b": 1.45,
    }
    SmokeCurve = {
        "a": -0.5,
        "b": 1.78,
    }

    Ro = 10

    def __init__(self, analogChannel: int, digitalChannel: int):
        self.analogChannel = analogChannel
        self.digitalChannel = digitalChannel
        GPIO.setup(digitalChannel, GPIO.IN)
        print("Calibrating Gas Sensor...")
        self.Ro = self.calibrate()
        print("Calibration done, Ro :", self.Ro, "k")

    def read(self):
        v = ADC.read(self.analogChannel)
        return v

    def calibrate(self):
        sensorValue = 0

        for _ in range(self.CALIBRATION_SAMPLE_TIMES):
            sensorValue += self.read()
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000)

        sensorValue /= self.CALIBRATION_SAMPLE_TIMES
        rs = ((3.3*10)/sensorValue)-10
        return rs / self.RO_CLEAN_AIR_FACTOR

    def readRs(self):
        sensorValue = 0
        for _ in range(self.READ_SAMPLE_TIMES):
            sensorValue += self.read()
            time.sleep(self.READ_SAMPLE_INTERVAL/1000)

        sensorValue /= self.READ_SAMPLE_TIMES
        rs = ((3.3*10)/sensorValue)-10

        return rs

    def getGasConcentration(self, gasId: GAS):
        ratioRsRo = self.readRs()/self.Ro
        ratioRsRo = math.log10(ratioRsRo)
        if gasId == GAS.LPG :
            return self.getConcentration(ratioRsRo, self.LPGCurve)
        if gasId == GAS.CO :
            return self.getConcentration(ratioRsRo, self.COCurve)
        if gasId == GAS.SMOKE :
            return self.getConcentration(ratioRsRo, self.SmokeCurve)
        
        return 0

    def getConcentration(self, rationRsRo: float, pcurve: Dict):
        gasRatio = (rationRsRo - pcurve.get("b"))/pcurve.get("a")
        ppm = math.pow(10, gasRatio)

        return ppm


if __name__ == "__main__":
    from datetime import datetime

    AIN2 = 2
    GPIO25 = 25

    def setup():
        GPIO.setmode(GPIO.BCM)
        ADC.setup(0x48)

    def loop():
        gasSensor = Gas(AIN2, GPIO25)
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