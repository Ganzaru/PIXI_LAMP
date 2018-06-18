import time
import RPi.GPIO as GPIO
from scipy.interpolate import interp1d

class Base:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(11,GPIO.OUT)
		GPIO.setup(13,GPIO.OUT)
		GPIO.setup(15,GPIO.OUT)
		GPIO.setup(7,GPIO.OUT)
	def translate(self, angleDegree):
		if angleDegree > 90:
			angleDegree = 90
		elif angleDegree < -90:
			angleDegree = -90
		mspD = ((1000.0*60.0)/(2.0*360.0))
		pulse=mspD/angleDegree
		if angleDegree>0:
			GPIO.output(15, GPIO.HIGH)
			GPIO.output(13,GPIO.LOW)
			GPIO.output(11, GPIO.HIGH)
			time.sleep(pulse)
		elif angleDegree<0:
			GPIO.output(15, GPIO.LOW)
			GPIO.output(13, GPIO.HIGH)
			GPIO.output(11, GPIO.HIGH)
			time.sleep(pulse)
		else:
			return 0
		GPIO.output(11, GPIO.LOW)
