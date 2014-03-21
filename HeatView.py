 
import cv2


class HeatCam():

	def __init__(self, TrainingData = "haarcascade_frontalface_alt.xml"):

		#Create the Video Interfaces
		self.b=[]

		for x in range(0, int(raw_input("How Many Devices?: "))):
			self.b += [cv2.VideoCapture(x)]

	def run(self):

		for x in range(0,len(self.b)):
			cv2.namedWindow("Interface "+str(x))

		i=0

		while(1):
			
			#_,img = cv2.VideoCapture(i%len(self.b)).read()
			_,img = self.b[i%len(self.b)].read()			
			img = cv2.flip(img,1)

			try: 
				cv2.imshow("Interface "+str(i%len(self.b)),img)

			except cv2.error:
				print "had to bail on norm", img

				#FOR FUTUR USE
				#sudo ./usbreset /dev/bus/usb/001/012

			i+=1

			x = cv2.waitKey(5)
			if x == 1048603:
				cv2.destroyAllWindows()
				for pipes in self.b:
					pipes.release()
				break


if __name__ == '__main__':
	tracker = HeatCam()
	tracker.run()