import os
import json
import threading
from wrapt import synchronized


dir_path = os.path.dirname(os.path.realpath(__file__))
lock = threading.Lock()

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._locked_call(*args, **kwargs)
        return cls._instances[cls]

    @synchronized(lock)
    def _locked_call(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)


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