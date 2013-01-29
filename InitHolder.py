from threading import *
import threading
import socket

class Server(Thread):
	def __init__(self, hostname, port, callback):
		import logging
		Thread.__init__(self)
		self.logger = logging.getLogger()
		self.hostname = hostname
		self.port = port
		self.callback = callback
		self.running = True
		self.threads = []
	def quit(self):
		self.running = False
		self._Thread__stop()
		for t in self.threads:
			if ( t.isAlive() ):
				t._Thread__stop()
		
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(1)
		self.logger.debug("listening at %s:%d" % (self.hostname, self.port,))
		
		while self.running:
			conn, address = self.socket.accept()
			self.logger.debug("Got connection")
			process = threading.Thread(target=self.callback, args=(conn, address))
			process.start()
			self.threads.append(process)
			#self.logger.debug("Started process %r", process)
			
		self.socket.close()