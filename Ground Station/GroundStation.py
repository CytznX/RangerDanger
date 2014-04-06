#!/usr/bin/python
import socket
import cv2
import numpy


class videoReciever():
	"""
	INIT CONSTRUCTOR_________________________
	"""
	def __init__(self,):

		self.TCP_IP = 'localhost'
		self.TCP_PORT = 5001
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((self.TCP_IP, self.TCP_PORT))
		self.s.listen(5)

	def recvall(self, sock, count):
	    buf = b''
	    while count:
	        newbuf = sock.recv(count)
	        if not newbuf: return None
	        buf += newbuf
	        count -= len(newbuf)
	    return buf


	def run(self):

		conn, addr = self.s.accept()

		while True:
			length = self.recvall(conn,16)
			stringData = self.recvall(conn, int(length))
			data = numpy.fromstring(stringData, dtype='uint8')

			decimg=cv2.imdecode(data,1)
			cv2.imshow('SERVER',decimg)

			wtkey = cv2.waitKey(5)
			ifs data == None: 
				break
			elif wtkey == 1048603:
				cv2.destroyAllWindows()
				break
			else:
				print  cv2.waitKey(5)
		self.s.close()

if __name__ == '__main__':
	client = videoReciever()
	client.run()
