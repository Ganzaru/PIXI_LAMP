from __future__ import division
from scipy.interpolate import interp1d

import time

# Import the PCA9685 module.
import Adafruit_PCA9685 as PWM

# Configure min and max servo pulse lengths
servo_min_sg90 = 200  # Min pulse length out of 4096
servo_max_sg90 = 750  # Max pulse length out of 4096
servo_min_mg996r = 150  # Min pulse length out of 4096
servo_max_mg996r = 600  # Max pulse length out of 4096
freq=50
# Dictionary to identify servo's use
servo_type={"Base": 0, "Leg": 1, "Arm": 2, "Neck": 3, "Head": 4}
mg996r=[0,1,2]
sg90=[3,4]
class Servo:
	# Initialise the PCA9685 using the default address (0x40).
	pwm = PWM.PCA9685()

	# Alternatively specify a different address and/or bus:
	#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

	# Class parameters
	_sType=0
	_maxAngle=90
	_minAngle=0
	_reverse=false
	_waitTime=250; #Time in us per 45 degrees
	_Angle=0
	def __init__(self, type=0, reverse=false):
		self._sType=type
		self._reverse=reverse

	def pulseCalc(self, degrees):
		Time=0
		if ((degrees<this._maxAngle) && (degrees>this._minAngle)):
			Time=(1/freq)*sin(degrees)
		return Time
	
	def translate(self,value):
		return interp1d([self._minAngle,self._maxAngle],[200,750])(value)
	
	# Helper function to make setting a servo pulse width simpler.
	def set_servo_pulse(channel, pulse):
		pulse_length = 1000000    # 1,000,000 us per second
		pulse_length //= freq       # 50 Hz
		print('{0}us per period'.format(pulse_length))
		pulse_length //= 4096     # 12 bits of resolution
		print('{0}us per bit'.format(pulse_length))
		pulse *= 1000
		pulse //= pulse_length
		#set_pwm(channel, on, off)
		pwm.set_pwm(channel, 0, pulse)
	# Set frequency to 50hz, good for servos.
	pwm.set_pwm_freq(freq)

	print('Moving servo on channel 0, press Ctrl-C to quit...')

s=Servo();
s.__init__(0)
while True:
	# Move servo on channel O between extremes.
	pwm.set_pwm(0, 0,s.translate(45))
	
	time.sleep(1)
	pwm.set_pwm(0, 0, s.translate(90))
	
	time.sleep(1)
		
time.sleep(1)