import json, requests
import sys
import time
import urllib
import urllib2
import threading
import signal
import subprocess


# ===============================
# -------  @PixiLampBot  -------
# ===============================

class Telegram():

	def __init__(self):

		self.telegramAPI = '556145401:AAE4xhgn-TgKqXIg9L1d2SCLsY08wLhUjuc'
		self.time2update = 2
		self.lastTime = 0

		self.run_event = threading.Event()
		self.chackLock = threading.Lock()
		self.thr = threading.Thread(target=self.run)
		self.thr.start()
		self.chat_id = 0
		
		self.takePhoto = False


	def end(self):
		self.run_even.set()
	
	
	def send_image(self):
		print 'Sending...'
		thr = threading.Thread(target=self.sender)
		thr.start()
	
	def sender(self):
		for i in [1,2,3,4]:
			imageFile = str(i) + '.jpg'
			command = 'curl -s -X POST https://api.telegram.org/bot' + self.telegramAPI + '/sendPhoto -F chat_id=' + self.chat_id + " -F photo=@" + imageFile
			print command
			subprocess.call(command.split(' '))
	
			
	def check(self):
		self.chackLock.acquire()
		r = self.takePhoto
		self.takePhoto = False
		self.chackLock.release()
		return r


	def run(self):
		while not self.run_event.is_set():
			self.updateTelegram()
			time.sleep(self.time2update)


	def updateTelegram(self):

		response = requests.get(url='https://api.telegram.org/bot' + self.telegramAPI + '/getUpdates')
		data = json.loads(response.text)

		command = data['result'][-1]['message']['text']
		date = data['result'][-1]['message']['date']
		self.chat_id = str(data['result'][-1]['message']['chat']['id'])

		if command == '/foto':
			if (date+self.time2update*10 >= time.time() and date != self.lastTime):
				self.lastTime = date
				print 'Foto ' + command
				#self.send_image('img.png',chat_id)
				self.chackLock.acquire()
				self.takePhoto = True
				self.chackLock.release()


