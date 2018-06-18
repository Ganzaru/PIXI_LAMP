from Servo import Servo
import Adafruit_PCA9685 as PWM
#from testFakePWM import PWM
import time
import threading

class Movement():



	def __init__(self):
		_servo_type={"Base": 0, "Leg": 2, "Arm": 4, "Neck": 6, "Head": 8}
		self.pwm =PWM.PCA9685()		# Initialise the PCA9685 using the default address (0x40).
		self.pwm.set_pwm_freq(50)
		# Create all the servos
		self.servos = {}
		for i in _servo_type.keys():
			self.servos[i] = Servo(self.pwm, _servo_type[i])
			print 'Servo "' + i + '" on channel ' + str(_servo_type[i])
		self.scanThread = None
		self.scan_event = threading.Event()
		self.angryLock = threading.Lock()
		self.angry=False


	def getServoAngle(self, serv):
		return self.servos[serv].getAngle()


	# Move servo to given position with given speed
	def setServoAngle(self, serv, angle, speed):
		# serv: "Base" / "Leg" / "Arm" ....
		# angle: Target angle
		# speed: How many steps to do to reach the angle (min 1)


		slp = 50	# Time to sleep in each iteration (ms)

		actualAng = self.servos[serv].getAngle()
		movSlice = float(angle - actualAng) / float(speed)

		for i in range(speed-1):
			actualAng += movSlice
			self.servos[serv].translate(int(actualAng))
			time.sleep(slp/1000.0)

		actualAng += movSlice
		self.servos[serv].translate(int(actualAng))
		self.servos[serv].translate(angle)

	# Move servo to given position with given speed
	def setServosAngles(self, serv, angle, speed):
		# serv: "Base" / "Leg" / "Arm" ....
		# angle: Target angle
		# speed: How many steps to do to reach the angle (min 1)


		slp = 50	# Time to sleep in each iteration (ms)
		actualAng = []
		movSlice = []
		i=0
		for servo in serv:

			actualAng.append(self.servos[servo].getAngle())
			movSlice.append(float(angle[i] - actualAng[i]) / float(speed))
			i=i+1

		for i in range(speed-1):

			for servo in range(len(serv)):
				actualAng[servo] += movSlice[servo]
				self.servos[serv[servo]].translate(int(actualAng[servo]))
				time.sleep(slp/1000.0)

		for servo in range(len(serv)):
			actualAng[servo] += movSlice[servo]
			self.servos[serv[servo]].translate(int(actualAng[servo]))
			self.servos[serv[servo]].translate(angle[servo])



	# Increment the servo position with the given speed
	# Return its final position
	def movServoAngle(self, serv, increment, speed):
		# serv: "Base" / "Leg" / "Arm" ....
		# increment: increment to rotate the angle
		# speed: How many steps to do to reach the angle (min 1)

		slp = 50	# Time to sleep in each iteration

		actualAng = self.servos[serv].getAngle()

		if increment == 0:
			return

		angle = actualAng+increment
		movSlice = float(angle - actualAng) / float(speed)

		for i in range(speed-1):
			actualAng += movSlice
			self.servos[serv].translate(int(actualAng))
			time.sleep(slp/1000.0)

		actualAng += movSlice
		self.servos[serv].translate(int(actualAng))

		return  int(actualAng)

# =============== Thread Scan Face ===============================================================


	def setAngry(self):
		self.angryLock.acquire()
		self.angry = True
		self.angryLock.release()
		print 'eeeeeeeeeeeeeeeeeeeeeeeeeeeee'


	def threadScan(self):
		incX = 1
		incY = 1
		self.angryLock.acquire()
		self.angry = False
		self.angryLock.release()

		while not self.scan_event.is_set():
			self.angryLock.acquire()
			a = self.angry
			self.angryLock.release()
			print  a

			if not a:
				sx = self.servos['Head'].getAngle()		# Get angle
				sy = self.servos['Neck'].getAngle()

				sx = min(90, max(-90, sx + incX*1))		# Increase angle (Between -90 & 90)
				sy = min(90, max(-90, sy + incY))

				if sx >= 90 or sx <= -90:				# Change direction when reach limits
					incX *= -1
				if sy >= 20 or sy <= -30:
					incY *= -1

				self.servos['Head'].translate(int(sx))	# Set angle to servos
				self.servos['Neck'].translate(int(sy))
				time.sleep(0.04)
			else:
				for i in range(0,5,1):
					print 'Baseeeeeeeeeeeee'
					self.setServoAngle("Base",10,1)
					time.sleep(1)
				for i in range(5,0,-1):
					self.setServoAngle("Base",-10,1)
					time.sleep(1)

	def startThreadScan(self):
		if self.scanThread != None:
			self.scan_event.set()
			self.scanThread.join()
		self.scan_event.clear()
		self.scanThread = threading.Thread(target=self.threadScan)
		self.scanThread.start()

	def stopScanFace(self):
		self.scan_event.set()
		try:
			self.scanThread.join()
		except:
			pass

	def getAllPos(self):
		servos = self.servos.keys()
		pos = []
		for s in servos:
			pos.append(self.servos[s].getAngle())
		return servos,pos

	def getServoPos(self, serv):
		return self.servos[serv].getAngle()

	def incial(self,speed):
		#self.setServosAngles(["Neck","Head","Arm","Leg"],[0,0,-90,-90],speed)
		self.servos['Head'].translate(0)
		self.servos['Neck'].translate(70)
		self.servos['Leg'].translate(-90)
		self.servos['Arm'].translate(-90)


	def normalIni(self,speed):
		self.setServosAngles(["Head","Neck","Leg","Arm"],[15,-0,-65,-35],speed)

	def normal(self,speed):
		self.setServosAngles(["Leg","Arm"],[-65,-35],speed)

	def asustada(self,speed):
		self.setServosAngles(["Neck","Leg","Arm"],[-80,-90,-70],speed)
	def cabreada(self, speed):
		self.setServosAngles(["Neck","Leg","Arm"], [-70, -60, -90, -60], speed)
		time.sleep(2)
		self.normalIni(5)




