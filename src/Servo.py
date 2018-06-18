from __future__ import division
from scipy.interpolate import interp1d
import Adafruit_PCA9685 as PWM
import time
import threading
#from testFakePWM import PWM


def times(angle):
        if angle < 0:
		angle *= -1
        ms=((100.0*60.0)/(100*5.0*360.0))*(angle)
        return ms



class Servo:
		# Class parameters

		def __init__(self, pwm, stype=0, reverse=False):
				
				self.servo_type={"Base": 0, "Leg": 2, "Arm": 4, "Neck": 6, "Head": 8}

				if stype == 0:
					self._maxAngle=360
                                	self._minAngle=-360
					self._maxFreq = 409
                                        self._minFreq = 205
				else:
					self._maxAngle=90
					self._minAngle=-90
					self._maxFreq = 480
					self._minFreq = 150


				self.pwm = pwm
				self.sType = stype
				self.reverse = reverse
				self.angle = 0

				

		def getAngle(self):
				return self.angle


		# Set servo to given angle
		def translate(self,angleDegree):
				if angleDegree > self._maxAngle:
						angleDegree = self._maxAngle
				elif angleDegree < self._minAngle:
						angleDegree = self._minAngle

				self.angle = angleDegree


				if self.sType != 0:
					angleDegree = int(interp1d([self._minAngle,self._maxAngle],[self._minFreq,self._maxFreq])(angleDegree))
					self.pwm.set_pwm(self.sType,0,angleDegree)
				else:
					th = threading.Thread(target=self.movBase, args=[angleDegree])
					th.start()
					#p=0
					#if angleDegree > 0:
					#	p = self._maxFreq
					#elif angleDegree < 0:
					#	p = self._minFreq
					#print times(angleDegree)
					#self.pwm.set_pwm(self.sType,0,p)
					#time.sleep(times(angleDegree))
					#self.pwm.set_pwm(self.sType,1,0)

				print 'Servo ' + str(self.sType) + ' ' + str(self.angle) + ' : ' + str(angleDegree)

		def movBase(self, angleDegree):
			p=0
			if angleDegree > 0:
				p = self._maxFreq
			elif angleDegree < 0:
				p = self._minFreq
			print times(angleDegree)
			self.pwm.set_pwm(self.sType,0,p)
			time.sleep(times(angleDegree))
			self.pwm.set_pwm(self.sType,1,0)
