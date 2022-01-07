import RPi.GPIO as GPIO
import time
import os
import json




class RGB_Led():
    	
	def __init__(self):
			
		dir_path = os.path.dirname(os.path.realpath(__file__))
		with open(dir_path + '/../config/' + 'config.json') as file:
			config = json.load(file)
			#self.colors = [0xFF0000, 0xFFFF00, 0x00FF00] # red, yellow, green
			self.pins = {
				'pin_R': config['Capteurs']['RGB Led']['Board-R'], 
				'pin_G': config['Capteurs']['RGB Led']['Board-G'], 
				'pin_B': config['Capteurs']['RGB Led']['Board-B']
			}
			GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
			for i in self.pins:
				GPIO.setup(self.pins[i], GPIO.OUT)   # Set pins' mode is output
				GPIO.output(self.pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
			
			self.p_R = GPIO.PWM(self.pins['pin_R'], 2000)  # set Frequece to 2KHz
			self.p_G = GPIO.PWM(self.pins['pin_G'], 2000)
			self.p_B = GPIO.PWM(self.pins['pin_B'], 2000)
			
			self.p_R.start(0)      # Initial duty Cycle = 0(leds off)
			self.p_G.start(0)
			self.p_B.start(0)


	def off(self):
		GPIO.setmode(GPIO.BOARD)
		for i in self.pins:
			GPIO.setup(self.pins[i], GPIO.OUT)   # Set pins' mode is output
			GPIO.output(self.pins[i], GPIO.HIGH)    # Turn off all leds

	def setColor(self,r,g,b): 
		
		self.p_R.ChangeDutyCycle(r)     # Change duty cycle
		self.p_G.ChangeDutyCycle(g)
		self.p_B.ChangeDutyCycle(b)

	def loop(self):
		self.setColor(0, 0, 0) #   red color
		time.sleep(5)   # 1s
		
	
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
	except KeyboardInterrupt:
		led.destroy()