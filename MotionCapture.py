import cv, cv2
import numpy as np
import datetime
import os

# Embed this shit, brah! We need it ON the dirigible, not the GCS :)

# And now for something completely different: a man with a tape recorder up his nose.
class MotionDetector():
	"""
	INIT CONSTRUCTOR_________________________
	"""
	def __init__(self, Interface = 1, winName = "Movement Indicator" , VideoLogFolder = "MotionCapture"):


		#Debug
		self.debug = False

		#Create the Video Interfaces
		self.Interface = Interface
		self.VideoInterface = cv2.VideoCapture(Interface)

		#Creates ViewScreen
		self.winName = winName
		cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

		#Video Record Folder
		self.VideoLogFolder = "VideoRecords/"+VideoLogFolder+"/"

		#video startime delay
		self.VideoStartTime = None

		#Future video interface
		self.video = None

	"""
	Cool method that generates a "motion" image... idk if you want we to explain it ... come find me
	"""
	def diffImg(self, t0, t1, t2):

		d1 = cv2.absdiff(t2, t1)
		d2 = cv2.absdiff(t1, t0)
		return cv2.bitwise_and(d1, d2)


	def Run(self, VidName = 'MotionTestVideo', record = False , length = 10):
		
		# Read three images first:
		if not self.Interface == 1:

			t_minus = cv2.cvtColor(self.VideoInterface.read()[self.Interface], cv2.COLOR_RGB2GRAY)
			t = cv2.cvtColor(self.VideoInterface.read()[self.Interface], cv2.COLOR_RGB2GRAY)
			t_plus = cv2.cvtColor(self.VideoInterface.read()[self.Interface], cv2.COLOR_RGB2GRAY)

		else:

			t_minus = self.VideoInterface.read()[1]
			t = self.VideoInterface.read()[1]
			t_plus = self.VideoInterface.read()[1]


		#IF where recording check for some things
		if record:

			#Check to see if record directory exists
			if not os.path.isdir(self.VideoLogFolder):
				os.makedirs(self.VideoLogFolder)
				print "Made the Directory"


			#Get some video info
			codec = cv.CV_FOURCC('D','I','V','X')

			size = (int(self.VideoInterface.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
			        int(self.VideoInterface.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))


		#Lazy way to do this... but... oh well
		count = 1
		while True:

			img = self.VideoInterface.read()[self.Interface]

			#Get the differecen in immages...pssst...its a method call(look below.... errr... above)
			motionPic = self.diffImg(t_minus, t, t_plus)
			cv2.imshow(self.winName, motionPic )
			
			# Read next image
			if not self.Interface == 1:
				t_minus = t
				t = t_plus
				t_plus = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			else:
				t_minus = t
				t = t_plus
				t_plus = img

			#Again... if its recording do some magic
			if record: 

				#grean the mean and standard deviation of the "Motion" pic
				mean,deviation = cv2.meanStdDev(motionPic)

				#Debug
				if self.debug: print "The mean: ", sum(mean)[0], " And the Deviation:",sum(deviation)[0]

				#IF we see movement
				if self.VideoStartTime==None:
					
					if sum(mean)[0]>20 or sum(deviation)[0]>20 :
						#Assighn video StartTime
						self.VideoStartTime = datetime.datetime.now()

						#Create a video writer
						self.video = cv2.VideoWriter()
						print self.VideoLogFolder+VidName+str(count)
						self.video.open(self.VideoLogFolder+VidName+"_"+str(count)+'.avi', codec, 30, size, 1)
						count+=1

						if self.debug: print "started Recording"

				elif (sum(mean)[0]>20 or sum(deviation)[0]>20):
					self.VideoStartTime = datetime.datetime.now()
					self.video.write(img)

					if self.debug: print "Wrote a frame"

				elif (datetime.datetime.now()-self.VideoStartTime).total_seconds()<length:
					self.video.write(img)

					if self.debug: print "wrote a frame... but no motion... "+ str((datetime.datetime.now()-self.VideoStartTime).total_seconds())

				else:
					
					#close the video file "save"
					self.video.release()

					#Wipe the Vars clean
					self.video = None
					self.VideoStartTime = None

					print "print clost video"


			#Check to see if esc been pressed
			if cv2.waitKey(5) == 1048603:
				cv2.destroyAllWindows()

				#If its recording bust out
				if record and not self.video== None :
					self.video.release()
				break

if __name__ == '__main__':
	tracker = MotionDetector()
	tracker.Run(record =True)


