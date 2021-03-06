import math
import sys
import time
from grove.adc import ADC

class GroveLoudnessSensor:
 
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC(address=8)
 
    @property
    def value(self):
        return self.adc.read(self.channel)
 
Grove = GroveLoudnessSensor