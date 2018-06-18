from Movement import Movement
from Vision import Vision
from Neopixel import Neopixel as Neo

import signal
import sys




neo = Neo()
movement = Movement()
vision = Vision(movement, neo)

def signal_handler(signal, frame):
	print('has pulsado ctrl c')
	global vision
	vision.end()
	neo.end()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


vision.runFaceFollower()


