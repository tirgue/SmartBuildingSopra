import os
import json
from services.singleton import Singleton

dir_path = os.path.dirname(os.path.realpath(__file__))



class configService(metaclass=Singleton) :
    
    def __init__(self):
        self.path = dir_path + '/../config/' + 'config.json'
        with open(self.path) as file:
            self.config = json.load(file)
            self.stamp = self.getCurrentStamp()
    
    def getConfig(self):
        if self.configWasUpdated() :
            self.refreshConfig()

        return self.config
    
    def refreshConfig(self):
        with open(self.path) as file:
            self.config = json.load(file)
            self.stamp = self.getCurrentStamp()
    
    def getCurrentStamp(self):
        return os.stat(self.path).st_mtime
    
    def configWasUpdated(self) :
        return self.stamp != self.getCurrentStamp()