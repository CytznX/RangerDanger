import cv2
import cv

camera = cv2.VideoCapture(int(raw_input("Which interface?(0-1): ")))
RecordVideo = raw_input("Would you like to record?(y/n): ")


if RecordVideo == 'y':

	codec = cv.CV_FOURCC('D','I','V','X')

	size = (int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
	        int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

	video = cv2.VideoWriter()

	video.open('TestVideo.avi', codec, 30, size, 1)

while True:
	
	f,img = camera.read()
	cv2.imshow("webcam",img)
	
	if RecordVideo == 'y':
		video.write(img)

	if (cv2.waitKey(5) == 1048603):
		break

if RecordVideo == 'y':
	video.release()