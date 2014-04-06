import os
import cv2, cv
import datetime

camera = cv2.VideoCapture(int(raw_input("Which interface?(0-1): ")))
RecordVideo = raw_input("Would you like to record?(y/n): ")


VideoFolder = "VideoRecords/ManualRecordings/"
imgFolder ="ImgRecords/ManualSnapshots/" 

#Check to see if record directorys exists
if not os.path.isdir(VideoFolder):
	os.makedirs(VideoFolder)
	print "Made the Directory"

if not os.path.isdir(imgFolder):
	os.makedirs(imgFolder)
	print "Made the Directory"


if RecordVideo == 'y':

	codec = cv.CV_FOURCC('D','I','V','X')

	size = (int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
	        int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

	video = cv2.VideoWriter()

	video.open('TestVideo.avi', codec, 30, size, 1)

imgcount= 0 
vidcount= 0

while True:
	
	f,img = camera.read()
	
	ret,thresh4 = cv2.threshold(img,75,255,cv2.THRESH_BINARY)
	cv2.imshow("webcam",img)
	cv2.imshow("threshhold2",thresh4)
	
	if RecordVideo == 'y':
		video.write(img)
	

	wtkey = cv2.waitKey(5)
	if ( wtkey== 1048603 ) or(wtkey ==27):
		break
	elif wtkey ==1048586:
		#TSH ENTER: 1048586
		pass
	elif wtkey == 1048608:
		#TSH SPACE: 1048608
		print "yeah", imgFolder+"SnapShop("+str(imgcount)+datetime.datetime.now().strftime(',%D')+").jpg"
		cv2.imwrite(imgFolder+"SnapShop("+str(imgcount)+datetime.datetime.now().strftime(',%D')+").jpg", img)
		imgcount+=1
	elif not wtkey == -1: 
		print wtkey

if RecordVideo == 'y':
	video.release()