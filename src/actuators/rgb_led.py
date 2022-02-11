import RPi.GPIO as GPIO
import time
import os
import json




class RGB_Led():
    	
	def __init__(self):
			
		dir_path = os.path.dirname(os.path.realpath(__file__))
		with open(dir_path + '/../config/' + 'config.json') as file:
			config = json.load(file)
			self._colorToDisplay = 1
			self.pins = {
				'pin_R': config['Capteurs']['RGB Led']['Board-R'], 
				'pin_G': config['Capteurs']['RGB Led']['Board-G'], 
				'pin_B': config['Capteurs']['RGB Led']['Board-B']
			}
			GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
			for i in self.pins:
				GPIO.setup(self.pins[i], GPIO.OUT)   # Set pins' mode is output
				GPIO.output(self.pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
			
			self.p_R = GPIO.PWM(self.pins['pin_R'], 2000)  # set Frequece to 2KHz
			self.p_G = GPIO.PWM(self.pins['pin_G'], 2000)
			self.p_B = GPIO.PWM(self.pins['pin_B'], 2000)
			
			self.p_R.start(100)      # Initial duty Cycle = 0(leds off)
			self.p_G.start(100)
			self.p_B.start(100)


	def off(self):
		GPIO.setmode(GPIO.BCM)
		for i in self.pins:
			GPIO.setup(self.pins[i], GPIO.OUT)   # Set pins' mode is output
			GPIO.output(self.pins[i], GPIO.HIGH)    # Turn off all leds

	def setColor(self,r,g,b): 
		
		self.p_R.ChangeDutyCycle(100-r)     # Change duty cycle
		self.p_G.ChangeDutyCycle(100-g)
		self.p_B.ChangeDutyCycle(100-b)
	
	@property
	def colorToDisplay(self):
		return self._colorToDisplay

	@colorToDisplay.setter
	def colorToDisplay(self, value):
			if(value in [0,1,2,3]):
				self._colorToDisplay = value

	def loop(self):
		while True:
			if(self.colorToDisplay == 0) : 
				self.setColor(100,100,100)
			elif(self.colorToDisplay == 1) :
				self.setColor(0, 100, 0) #   green color
			elif(self.colorToDisplay == 2) :
				self.setColor(100, 100, 0) #   yellow color
			elif(self.colorToDisplay == 3) :
				self.setColor(100, 0, 0) #   red color
			time.sleep(3)   # 1s
		
	
	def destroy(self):
		self.p_R.stop()
		self.p_G.stop()
		self.p_B.stop()
		self.off()
		GPIO.cleanup()

if __name__ == "__main__":
	try:
		
		led = RGB_Led()
		led.loop()
		led.destroy()
	except KeyboardInterrupt:
		led.destroy()