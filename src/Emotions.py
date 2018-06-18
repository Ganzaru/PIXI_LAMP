from Neopixel import Neopixel as neo
from Movement import Movement
from Contar import Contar as contar
import time

class Emotions:

	def __init__(self,neo,movement):
		self.n=neo
		self.mov=movement
		self.n.normal()
		self.c= contar()
		self.emo = 'normal'

	def fotoMovement(self):
		self.n.doFlash()

	def curiousMovement(self):
		n = self.mov.getServoAngle('Neck')
		h = self.mov.getServoAngle('Head')
		self.mov.setServosAngles(["Leg","Arm","Neck","Head"],[-45,-60,n-100,h-100],3)
		time.sleep(0.6)
		self.mov.setServosAngles(["Leg","Arm","Neck","Head"],[-55,-90,n-100,h+150],3)
		time.sleep(0.6)
		self.mov.setServosAngles(["Leg","Arm","Neck","Head"],[-55,-90,n-100,h-100],3)
		time.sleep(0.6)
		self.mov.setServosAngles(["Leg","Arm","Neck","Head"],[-45,-60,n,h],3)
		time.sleep(1)

	def happy(self, angry=False):
		if self.emo != 'happy':
			self.n.doHappy()
			self.mov.setServosAngles(["Leg","Arm"],[-80,-80],1)
			self.mov.normal(2)
			time.sleep(0.3)
			self.mov.setServosAngles(["Leg","Arm"],[-80,-80],1)
			self.mov.normal(2)
			self.emo = 'happy'
			if angry:
				self.mov.normal()
			print self.emo
		#self.n.normal()
		#self.emo='normal'
		#time.sleep(3)
		#self.n.end()

	def normal(self, mov=True):

		if self.emo != 'normal':
			self.n.normal()
			self.emo = 'normal'
			print self.emo
			if mov:
				self.mov.setServosAngles(["Head","Neck"],[15, -10], 5)
				self.mov.normal(5)

	def anger(self):
		if self.emo != 'anger':
			self.n.doCabreo()
			self.emo = 'anger'
			self.mov.cabreada(5)
			print self.emo

	def susto(self):
		if self.emo != 'susto':
			servos,pos = self.mov.getAllPos()
			self.n.susto()
			self.mov.asustada(1)
			self.emo='susto'
			print self.emo
			print servos, pos
			return servos,pos

	def playcontar(self, hsv):

		contador=[]
		contador = self.c.contar(hsv)

		self.n.doColorSet([0,0,0])

		i=0
		c=0
		for obj in contador:
			if (c==0 or c==5):
				color=[0,255,0]
			if (c==1 or c==6):
				color=[255,0,0]
			if (c==2 or c==7):
				color=[0,0,255]
			if (c==3 or c==8):
				color=[0,255,255]
			if (c==4 or c==8):
				color=[255,255,0]
			if c==5:
				i=i+1

			print c, obj
			self.n.ColorPlay(color, i, obj)
			
			i=i+obj
			c=c+1

		self.mov.setServoAngle("Neck",20,3)
		i=0
		c=0
		time.sleep(5)
