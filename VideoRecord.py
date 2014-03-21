import cv2
import cv

camera = cv2.VideoCapture(0)


codec = cv.CV_FOURCC('D','I','V','X')
print codec

size = (int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

video = cv2.VideoWriter()
print video.open('TestVideo.avi', codec, 30, size, 1)
print video,video.isOpened()

while True and video.isOpened():
   f,img = camera.read()
   video.write(img)
   cv2.imshow("webcam",img)
   if (cv2.waitKey(5) == 1048603):
       break
       
video.release()