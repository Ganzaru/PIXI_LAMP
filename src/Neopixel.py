import time
from neopixel import *
import argparse
import threading


class Neopixel:


	def __init__(self):

		# LED strip configuration:
		LED_COUNT	   = 24		 # Number of LED pixels.
		LED_PIN		   = 18		 # GPIO pin connected to the pixels (18 uses PWM!).
		#LED_PIN		= 10	  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
		LED_FREQ_HZ	   = 800000	 # LED signal frequency in hertz (usually 800khz)
		LED_DMA		   = 10		 # DMA channel to use for generating signal (try 10)
		LED_BRIGHTNESS = 50		# Set to 0 for darkest and 255 for brightest
		LED_INVERT	   = False	 # True to invert the signal (when using NPN transistor level shift)
		LED_CHANNEL	   = 0		 # set to '1' for GPIOs 13, 19, 41, 45 or 53

		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
		self.strip.begin()

		self.thr = None
		self.stopFlag = threading.Event()


	def end(self):
		self.stopThread()
		self.colorWipe(Color(0,0,0), 10)

	def ColorSet(self, color):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
		self.strip.show()

	def ColorPlay(self, color, pos, num):
		
		for i in range(pos, pos+num):
			self.strip.setPixelColor(i, Color(color[0],color[1],color[2]))
			#self.colorWipe(Color(255, 0, 0))  # Red wipe
		self.strip.show()

	# Define functions which animate LEDs in various ways.
	def colorWipe(self, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChase(self, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		while not self.stopFlag.is_set():
			for j in range(iterations):
				for q in range(3):
					for i in range(0, self.strip.numPixels(), 3):
						self.strip.setPixelColor(i+q, color)
						if self.stopFlag.is_set(): return
					self.strip.show()
					time.sleep(wait_ms/1000.0)
					for i in range(0, self.strip.numPixels(), 3):
						self.strip.setPixelColor(i+q, 0)
						if self.stopFlag.is_set(): return

	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		while not self.stopFlag.is_set():
			for j in range(256*iterations):
					for i in range(self.strip.numPixels()):
						self.strip.setPixelColor(i, self.wheel((i+j) & 255))
						if self.stopFlag.is_set(): return
					self.strip.show()
					time.sleep(wait_ms/1000.0)

	def rainbowCycle(self, wait_ms=1, iterations=4):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		self.strip.setBrightness(50)
		for j in range(256*iterations):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.wheel((int(i * 256/ self.strip.numPixels()) + j) & 255))
			self.strip.show()
			time.sleep(wait_ms/1000.0)
		self.ColorSet(Color(20,20,20))

	def theaterChaseRainbow(self, wait_ms=1):
		"""Rainbow movie theater light style chaser animation."""
		while not self.stopFlag.is_set():
			for j in range(256):
					for q in range(3):
						for i in range(0, self.strip.numPixels(), 3):
							self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
							if self.stopFlag.is_set(): return
					self.strip.show()
					time.sleep(wait_ms/1200.0)
					for i in range(0, self.strip.numPixels(), 3):
						self.strip.setPixelColor(i+q, 0)
						if self.stopFlag.is_set(): return

	def brightenAndDark(self):
		j=20
		for j in range (256):
			for i in range (0, self.strip.numPixels(),1):
				self.strip.setPixelColor(i,j)
				if self.stopFlag.is_set(): return
			self.strip.show()
			time.sleep(0.01)

			for j in range (256,20,-1):
				for i in range (0, self.strip.numPixels(),1):
					self.strip.setPixelColor(i,j)
					if self.stopFlag.is_set(): return
				self.strip.show()
				time.sleep(0.01)

			j=20
			for j in range (256):
				for i in range (0, self.strip.numPixels(),1):
					self.strip.setPixelColor(i,j)
					if self.stopFlag.is_set(): return
				self.strip.show()

	def Breathe(self, iterations=1):
		#self.strip.setBrightness(50)
		while True:
				self.ColorSet(Color(0,55,0))
				for j in range(iterations):
					for i in range(55,0):
						#self.strip.setPixelColor(i, Color(0,0,255))
						self.strip.setBrightness(i)
						self.strip.show()
						if self.stopFlag.is_set(): return
						time.sleep(0.01)
					time.sleep(0.5)
					for i in range(55):
						self.strip.setBrightness(i)
						self.strip.show()
						if self.stopFlag.is_set(): return
						time.sleep(0.01)
		#self.strip.setBrightness(50)

	def flash(self):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(100,100,100))
			if self.stopFlag.is_set(): return
		self.strip.show()
		for c in range(255,0,-50):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, Color(c,c,c))
			if self.stopFlag.is_set(): return
		time.sleep(0.1)
		self.strip.show()

	def fadeIn(self):
		for b in range(0,255,8):
			for i in range (0, self.strip.numPixels(),1):
				self.strip.setPixelColor(i,Color(0,(75*b)/255,(140*b)/255))
				if self.stopFlag.is_set(): return
			self.strip.show()
			time.sleep(0.01)

	def doTheaterChaseRainbow(self):
		self.stopThread()
		self.thr = threading.Thread(target=self.theaterChaseRainbow)
		self.thr.start()

	def doBrightenAndDark(self):
		self.stopThread()
		self.thr = threading.Thread(target=self.brightenAndDark)
		self.thr.start()

	def doFadeIn(self):
		self.stopThread()
		self.thr = threading.Thread(target=self.fadeIn)
		self.thr.start()

	def doTheaterChase(self, color):
		self.stopThread()
		self.thr = threading.Thread(target=self.theaterChase, args = [Color(color[0],color[1],color[2])] )
		self.thr.start()

	def doColorSet(self, color):
		self.stopThread()
		self.thr = threading.Thread(target=self.ColorSet, args = [Color(color[0], color[1], color[2])] )
		self.thr.start()
		
	def doColorWipe(self, color):
		self.stopThread()
		self.thr = threading.Thread(target=self.colorWipe, args = [Color(color[0],color[1],color[2])] )
		self.thr.start()

	def doRainbow(self):
		self.stopThread()
		self.thr = threading.Thread(target=self.rainbowCycle)
		self.thr.start()

	def doFlash(self):
		self.stopThread()
		self.thr = threading.Thread(target=self.flash)
		self.thr.start()

	def doHappy(self, wait_ms=1, iterations=4):
		self.doRainbow()
	#self.stopThread()
	#self.thr=threading.Thread(target=self.rainbowCycle)
	#self.thr.start()
	#self.thr.join()
	#self.thr=threading.Thread(target=self.theaterChaseRainbow)
	#self.thr.start()
	#def doColorBreathe(self, color, iterations=10):
	#self.ColorSet(Color(color[0], color[1], color[2])
	#self.stopThread()
	#self.thr=threading.Thread(target=self.Breathe, args = [iterations])
	#self.thr.start()


	def normal(self):
		self.doColorSet([20,20,20])

	def doCabreo(self):
		#self.doColorSet([220,20,60])
		print 'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
		self.stopThread()
		self.thr = threading.Thread(target=self.Breathe)
		self.thr.start()


	def susto(self):
		self.doColorSet([75,0,140])



	def stopThread(self):
		if self.thr != None:
			self.stopFlag.set()
			self.thr.join()
			self.stopFlag.clear()

	def prueba(self):
		self.doHappy()


	def test(self):
		try:
			while True:
				#print("Brightness and Dark test")
				#self.brightenAndDark()
				self.fadeIn()
				self.theaterChaseRainbow()
				print ('Color wipe animations.')
				self.colorWipe(Color(255, 0, 0))  # Red wipe
				self.colorWipe(Color(0, 255, 0))  # Blue wipe
				self.colorWipe(Color(0, 0, 255))  # Green wipe
				print ('Theater chase animations.')
				self.theaterChase(Color(127, 127, 127))	 # White theater chase
				self.theaterChase(Color(127,   0,	0))	 # Red theater chase
				self.theaterChase(Color(  0,   0, 127))	 # Blue theater chase
				print ('Rainbow animations.')

				self.rainbow()
				self.rainbowCycle()
				self.theaterChaseRainbow()

		except KeyboardInterrupt:
			self.end()
