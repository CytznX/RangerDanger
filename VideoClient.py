#!/usr/bin/python
import socket
import cv2
import numpy



class VideoForwarder():
	"""
	INIT CONSTRUCTOR_________________________
	"""
	def __init__(self, Interface = 1):
		
		self.Runflag = True

		self.Interface = cv2.VideoCapture(0)

		self.TCP_IP = 'localhost'
		self.TCP_PORT = 5001

		self.sock = socket.socket()
		self.sock.connect((self.TCP_IP, self.TCP_PORT))
	
	def go(self):
		self.Runflag = True
		self.run()

	def stop():
		self.Runflag = False

	def run(self):

		while self.Runflag:


			ret, frame = self.Interface.read()

			encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
			result, imgencode = cv2.imencode('.jpg', frame, encode_param)
			data = numpy.array(imgencode)
			stringData = data.tostring()

			self.sock.send( str(len(stringData)).ljust(16));
			self.sock.send( stringData );
		self.sock.close()

if __name__ == '__main__':
	client = VideoForwarder()
	client.go()
