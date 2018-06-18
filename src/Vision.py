from __future__ import division
from scipy.interpolate import interp1d
import numpy as np
import operator
from skimage.measure import label, regionprops
import cv2 as cv
import time
from Servo import Servo
from Movement import Movement
from Contar import Contar
import operator
from skimage.measure import label, regionprops
import random
from Emotions import Emotions as em
#import Neopixel
import threading
from Telegram import Telegram as Tele

class Vision:


		def __init__(self, movement, neo, fps=25):

				self.cap = cv.VideoCapture(0)	#Define camera
				self._frameResize = 0.5			# Resize the camera frame to go faster
				self.cap.set(cv.cv.CV_CAP_PROP_FPS,fps)		 # Set fps of the camera

				ret, self.frame = self.cap.read()			 # Read first frame
				if(ret == False):
						print 'Error opening camera! :('

				self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)		 # Gray frame
				self.emotion=em(neo,movement)


				# Camera resolution
				self.width = int(len(self.frame[0]) * self._frameResize)
				self.height = int(len(self.frame) * self._frameResize)


				self.movement = movement		# Class to move the robot
				self.tele = Tele()
				self.Contar= Contar()

				# ---------------- Face Follower variabes ----------------
				self.face_cascade = cv.CascadeClassifier('lbp.xml')		# Cascade classifier for face detection

				self._img_limit_x = 1.0/2.6			  # Image horizontal limits to start moving camera
				self._img_limit_y = 1.0/2.2			  # Image vertical limits to start moving camera

				self._img_limit_stop_x = 1.0/2.2	  # Center limit horizontal to stop moving
				self._img_limit_stop_y = 1.0/2.2	  # Center limit vertical to stop moving

				self.dirxc = 0			 # Direction to rotate camera horizontally
				self.diryc = 0			 # Direction to rotate camera vertically

				self._maxTimeWithNoFace = 4 # After x seconds with no faces start moving servos to find it
				self._maxTimeCabreo = 13
				self._maxTimeFoto = 3
				self.happyTime = 0
				self._happyTimeMax = 0.5

				self._aux=0
				self._head0=0
				self._neck0=0



				self.threadScanFace = None
				self.scan_event = threading.Event()
				self.read_lock = threading.Lock()
				self.timeScanning  = 0
				self.maxTimeScanning = 14

				self.faceNotMoved = 0
				self.scanDirX = -1
				self.scanDirY = 1
				self._maxTamFace= 1.3*((self.width**2+self.height**2)**0.5)*self._frameResize
				#print 'Cara susto: ' , str(self._maxTamFace)
				self.movement.incial(7)
				self.movement.normalIni(5)

				self.readLock = threading.Lock()
				self.thrCam = threading.Thread(target=self.camGetter)
				self.thrCam.start()
				self.angry = False

		def camGetter(self):
			while True:
				self.readLock.acquire()
				ret, self.frame = self.cap.read()
				self.frame = cv.resize(self.frame, (0,0), fx=self._frameResize, fy=self._frameResize)
				self.readLock.release()
				time.sleep(0.04)

		# def flushBufferCam(self, num):
			# for i in range(num):
				# ret, self.frame = self.cap.read()
			# print '---------- Flushed'

		# Close camera
		def end(self):
				self.cap.release()
				del(self.cap)

		def takePhotos(self, head,neck):

			self.movement.setServosAngles(["Neck","Head"],[neck,head],1)
			self.emotion.fotoMovement()
			time.sleep(1)
			self.readLock.acquire()
			cv.imwrite('1.jpg', self.frame)
			self.readLock.release()

			self.movement.setServosAngles(["Neck","Head"],[neck+10,head+10],1)
			self.emotion.fotoMovement()
			time.sleep(1)
			self.readLock.acquire()
			cv.imwrite('2.jpg', self.frame)
			self.readLock.release()

			self.movement.setServosAngles(["Neck","Head"],[neck-15,head+20],1)
			self.emotion.fotoMovement()
			time.sleep(1)
			self.readLock.acquire()
			cv.imwrite('3.jpg', self.frame)
			self.readLock.release()

			self.movement.setServosAngles(["Neck","Head"],[neck+15,head-20],1)
			self.emotion.fotoMovement()
			time.sleep(1)
			self.readLock.acquire()
			cv.imwrite('4.jpg', self.frame)
			self.readLock.release()

			self.tele.send_image()

		# Run the main code to follow faces
		def runFaceFollower(self):

				faceFound = False
				timeWithNoFace = time.time()
				timeWithFace = 0
				followFaceing = True			# True: faceFollow / False: servoScanFace

				while True:
						# Get camera frame
						#ret, self.frame = self.cap.read()
						#self.frame = cv.resize(self.frame, (0,0), fx=self._frameResize, fy=self._frameResize)
						#self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
						self.readLock.acquire()
						self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
						hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
						self.readLock.release()


						

						if followFaceing:

								lower_red = np.array([0,50,50])
								upper_red = np.array([20,255,255])
								mask0 = cv.inRange(hsv, lower_red, upper_red)
								lower_red = np.array([170,50,50])
								upper_red = np.array([180,255,255])
								mask1 = cv.inRange(hsv, lower_red, upper_red)
								red = mask0+mask1
								red = cv.inRange(hsv, lower_red, upper_red)
								kernelopen = np.ones((2,2),np.uint8)
								kernelclose = np.ones((5,5),np.uint8)

								red = cv.morphologyEx(cv.morphologyEx(red, cv.MORPH_OPEN, kernelopen), cv.MORPH_CLOSE, kernelclose)
								r_labels = label(red)                                   ###### RED LABEL
								rrps = regionprops(r_labels)
								print len(rrps)
								if len(rrps)>0:
								    print max(rrps, key=operator.attrgetter('area')).area
								    if (max(rrps, key=operator.attrgetter('area')).area)>15000:
										#contador = self.Contar.contar(hsv)
										#print hsv
										self.movement.setServosAngles(["Leg","Arm","Head","Neck"],[-30,-30,0,85],5) 
										time.sleep(3)
										self.readLock.acquire()
										hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
										self.readLock.release()
										self.emotion.playcontar(hsv)
										time.sleep(3)
										self.emotion.normal()
								

								faceFound = self.faceFollow()			# Follow the face
								if faceFound:
										print 'Face'
										if self.tele.check():
											print 'Fotoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
											self.stopScanFace()
											self.takePhotos(self._head0,self._neck0)
											self.movement.setServosAngles(["Head","Neck"],[self._head0,-self._neck0],1)
											self.emotion.normal()
											#self.flushBufferCam(2)
										timeWithNoFace = 0
										if timeWithFace == 0:
												timeWithFace = time.time()
										twf = time.time()-timeWithFace
										if twf >= self._happyTimeMax:
												self.emotion.happy(self.angry)
												self.angry = True
								else:			# If we not detect any face:
										print 'No Face'
										timeWithFace = 0
										if timeWithNoFace == 0:
												timeWithNoFace = time.time()	# Start counting time since last detection
										twnf = time.time() - timeWithNoFace
										if (twnf) >= self._maxTimeWithNoFace:	# Past "maxTimeWithNoFace":
												followFaceing = False			 # Start moving servos to find faces
						else:
							print 'start scan face'
								#if (time.time()- timeWithNoFace >= self._maxTimeCabreo):
							#			print "emocion cabreo"
										#self.emotion.anger()
										#timeWithNoFace = time.time()
										#print self.emotion.emo
										#self.emotion.normal() #No lo hace bien 
										#print self.emotion.emo
								#else:
										#followFaceing = self.servoScanFace()
							self.startScanFace()
							followFaceing = True

		def threadGetCam(self):
			while not self.scan_event.is_set():
				#self.read_lock.acquire()
				# ret, self.frame = self.cap.read()
				# self.frame = cv.resize(self.frame, (0,0), fx=self._frameResize, fy=self._frameResize)
				# self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
				#self.read_lock.release()
				self.readLock.acquire()
				self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
				self.readLock.release()

				faceFound = self.faceFollow()
				if faceFound:
					self.stopScanFace()
				print time.time()-self.timeScanning
				if time.time()-self.timeScanning >= self._maxTimeCabreo:
					self.angry=True
					self.emotion.anger()
					#self.movement.setAngry()
					print 'angeeeeeeeeeeeer'
					#self.emotion.normal()

		def startScanFace(self):

			#self.emotion.normal()
			if self.threadScanFace != None:
				self.stopScanFace()
			self.timeScanning = time.time()
			self.scan_event.clear()
			self.threadScanFace = threading.Thread(target=self.threadGetCam)
			self.movement.startThreadScan()
			self.threadScanFace.start()
			self.threadScanFace.join()

		def stopScanFace(self):
			self.scan_event.set()
			try:
				self.threadScanFace.join()
			except:
				pass
			self.movement.stopScanFace()
			self.threadScanFace = None

		# Move servos trying to fins some face
		# def servoScanFace(self, ):
				# print 'Scanning...'
				# self.emotion.normal()
				# x,y,w,h = 0,0,0,0				# coords of face

				# # Move servos

				# a = self.movement.movServoAngle('Head',(self.scanDirX*2), 2)
				# b = self.movement.movServoAngle('Neck',(self.scanDirY*2),2)

				# #sx = self.movement.getServoPos('Head')
				# #sy = self.movement.getServoPos('Neck')


				# if a >= 85 or a <= -85:
						# self.scanDirX = self.scanDirX * -1

				# if b >= 15 or b <= -60:
                                                # self.scanDirY = self.scanDirY * -1

				# face = self.searchFace()				# Search faces


				# if not isinstance(face, bool):
						# return True
				# else:
						# return False




		# Search the nearest face and return its coordinates and size
		def searchFace(self):

				faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 2)	# Search faces

				if not isinstance(faces, tuple):				# If we find some faces
						# Get the biggest (nearest) face
						(maxX,maxY,maxW,maxH) = faces[0]		# coords of first face
						for i in range(1,len(faces)):
								if (maxW**2+maxH**2)**0.5 < (faces[i][2]**2+faces[i][3]**2)**0.5:		# Take the biggest face
										(maxX,maxY,maxW,maxH) = faces[i]


						#cv.rectangle(self.gray,(maxX,maxY),(maxX+maxW,maxY+maxH),(255,0,0),2)	  # Face
						# Center coords
						x=int(maxX+maxW/2)
						y=int(maxY+maxH/2)
						#cv.circle(self.gray,(x,y),10,(255,255,0),2)			# Face center

						return (x,y,maxW,maxH)
				else:
						return False




		# Calculate the needed servo movements to follow a face
		def faceFollow(self):

				self.dirxc = 0
				self.diryc = 0

				x,y,w,h = 0,0,0,0				# coords of face

				face = self.searchFace()				# Search faces
				isFace = not isinstance(face, bool)

				fotoTimeCount = 0

				# Detect when move to follow the face
				if isFace:
						#if self.happyTime == 0:
                                                #             	self.happyTime = time.time()    # Start countin$
                                                #if (time.time() - self.happyTime) >= self._happyTimeMax:
                                                #                self.emotion.happy()
						(x,y,w,h) = face		# coords of face
						taman=(w*w+h*h)**0.5
						# Susto
						if taman>self._maxTamFace:
								print 'Susto'
								servos, pos = self.emotion.susto()
								isFace=0
								self.movement.setServosAngles(servos,pos,6)
								#self.flushBufferCam(10)
								taman=0
								fotoTimeCount = 0
								isFace=0
								self.emotion.normal(False)
						# Detect when face is inside limits
						if x<int(self.width * self._img_limit_x):
								self.dirxc= (1-x/(self.width/2)) * 3
								foto=0
								self._aux=0

						elif x>int(self.width-(self.width*self._img_limit_x)):
								self.dirxc= ((x-(self.width-(self.width/2)))/(self.width/2)) * -3
								foto=0
								self._aux=0
						if y<int(self.height*self._img_limit_y):
								self.diryc= (1-y/(self.height/2)) * 3
								foto=0
								self._aux=0
						elif y>int(self.height-(self.height*self._img_limit_y)):
								self.diryc= ((y-(self.height-(self.height/2)))/(self.height/2)) * -3
								foto=0
								self._aux=0
				else:
						self.happyTime=0


				# Detect when stop moving
				if self.dirxc == 1 and (x>int(self.width*self._img_limit_stop_x)):
						self.dirxc=0
				elif self.dirxc==-1 and (x<=int(self.width-(self.width*self._img_limit_stop_x))):
						self.dirxc=0
				if self.diryc==1 and (y>int(self.height*self._img_limit_stop_y)):
						self.diryc=0
				elif self.diryc==-1 and (y<=int(self.height-(self.height*self._img_limit_stop_y))):
						self.diryc=0

				if isFace  and self.dirxc==0 and self.diryc==0 :
						fotoTimeCount = time.time()
						if(self._aux==0):
								self._aux=fotoTimeCount
				#print  fotoTimeCount-self._aux
				if isFace and self._aux!=0 and ((fotoTimeCount-self._aux) >= self._maxTimeFoto):   #Past "maxTimeWithNoFace":
						print 'Curious'
						self.emotion.curiousMovement()
					                    #Start moving servos to fake take pictures
						self._aux=0
						self.movement.setServosAngles(["Head","Neck"],[self._head0,self._neck0],1)
						isFace=False
						self.emotion.normal()
						
						
						
				

				#print 'X_dir ' + str(self.dirxc) + ' Y_dir ' +	str(self.diryc)

				#cv.rectangle(self.gray,(0,0),(int(self.width * self._img_limit_x),self.height),(255,0,255),1)				  # Left limit
				#cv.rectangle(self.gray,(int(self.width-(self.width*self._img_limit_x)),0),(self.width,self.height),(255,0,255),1)	  # Right limit

				#cv.rectangle(self.gray,(0,0),(self.width,int(self.height*self._img_limit_y)),(0,255,255),1)   # Top limit
				#cv.rectangle(self.gray,(0,int(self.height-(self.height*self._img_limit_y))),(self.width,self.height),(0,255,255),1)   # Bottom limit

				#cv.rectangle(self.gray,(int(self.width*self._img_limit_stop_x),int(self.height*self._img_limit_stop_y)),(int(self.width-(self.width*self._img_limit_stop_x)),int(self.height-(self.height*self._img_limit_stop_y))),(50,50,50),1)	# Stop center
				#cv.rectangle(self.gray,(int(self.width*self._img_limit_stop_x),0),(int(self.width-(self.width*self._img_limit_stop_x)),self.height),(100,0,100),1)  # Stop x center
				#cv.rectangle(self.gray,(0,int(self.height*self._img_limit_stop_y)),(self.width,int(self.height-(self.height*self._img_limit_stop_y))),(0,100,100),1)	# Stop y center

				# Update servo pos
				if (self.dirxc != 0):
						self._head0=self.movement.movServoAngle('Head',self.dirxc, 1)
				if (self.diryc != 0):
						self._neck0=self.movement.movServoAngle('Neck',-self.diryc, 1)

				# cv.imshow('gray', self.gray)
				# cv.waitKey(1)
						
				return isFace
