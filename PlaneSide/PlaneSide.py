#!/usr/bin/python
import socket
import cv2
import numpy
import time
from threading import Thread
import thread



class VideoForwarder(Thread):
	"""
	INIT CONSTRUCTOR_________________________
	"""
	def __init__(self, Interface = 1):

		#Initialize myself as thread... =P
		Thread.__init__(self)
		
		#Turn the Video stream on/of
		self.Runflag = True
		self.VideoStreams = dict()

		self.Interface = cv2.VideoCapture(0)


		#Some default IP bs...
		self._BuffSize = 1024
		self.Addr = ('', 5555)

		#create the socket that will be listening on
		self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serversock.bind(self.Addr)
		self.serversock.listen(5)

		#Heres the Thread That actually handles the video streams
		self.StreamerThread = thread.start_new_thread(self.VideoStreamThread, ())

		#Start the main thread(This might not work)
		self.start()


	def run(self):

		#All this loop does is listen for connections and spawn mini threads
		while self.Runflag:

			#Here we wait for incoming connection
			clientsock, addr = self.serversock.accept()

			#we spawn new mini thread and pass off connection
			thread.start_new_thread(self.miniThread, (clientsock, addr))


	def stop(self):

		#Kill the Runflag
		self.Runflag = False

		#Create a connection to self so that we skip of blocking call
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(self.Addr)

		#Kill the pipe(s)
		self.serversock.close()
		for sockets in self.VideoStreams:
			sockets[0].close()

		#Wait for streamer thread to join back up with main
		self.StreamerThread.join()

	'''Heres where we spawn a minin thread that manages a individual connection to this machine'''
	def miniThread(self,clientsock,addr):
		
		#PULL IN COMAND 
		while self.Runflag:
			data = clientsock.recv(self._BuffSize)

			#If theres nothing in the pipe... get out!!!
			if not data: 
				break
			elif data.rstrip().startswith('#START_STREAM') and len(data.rstrip().split())== 2:
				self.VideoStreams[addr[0]]= (socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((addr[0],int(data.rstrip().split()[1]))),Lock())

			elif data.rstrip().startswith('#END_STREAM'):
				theLock = self.VideoStreams[addr[0]][1].acquire()
				self.VideoStreams[addr[0]][0].close()
				del self.VideoStreams[addr[0]]
				theLock.release()

			elif data.rstrip().startswith('KILL_ALL'):

				for key in self.VideoStreams.keys():
					theLock=self.VideoStreams[1].acquire()
					self.VideoStreams[key][0].close()
					del self.VideoStreams[key]
					theLock.release()

			elif "#CLOSE" == data.rstrip():
				break

			elif "#KILL" == data.rstrip(): 
				self.stop()
				break # type '#KILL' on client console to close connection from the server side

		clientsock.close()


	def VideoStreamThread(self):

		while self.Runflag:

			if not self.VideoStreams.keys() == []:

				ret, frame = self.Interface.read()

				encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
				result, imgencode = cv2.imencode('.jpg', frame, encode_param)
				data = numpy.array(imgencode)
				stringData = data.tostring()

				for sockets in self.VideoStreams:
					sockets[0].send( str(len(stringData)).ljust(16));
					sockets[0].send( stringData );

			else:
				time.sleep(1)


if __name__ == '__main__':
	client = VideoForwarder()
