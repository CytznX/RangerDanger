 
import cv2


class FaceDetect():

	def __init__(self, TrainingData = "haarcascade_frontalface_alt.xml"):
		
		#Pull in the cascade feature template we want to use
		self.cascade = cv2.CascadeClassifier(TrainingData)

		#Create the Video Interfaces
		self.b = cv2.VideoCapture(0)
		

	def detect(self, img):
	    rects = self.cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

	    if len(rects) == 0:
	        return [], img
	    rects[:, 2:] += rects[:, :2]
	    return rects, img

	def box(self, rects, img):
		for x1, y1, x2, y2 in rects:
			cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
	
	def compare(self, rects, img):
		crop_img = img[y1:y2, x1:x2, :] 
						
	def run(self):


		cv2.namedWindow("FaceTracker")

		i=0

		while(1):

			_,orig_img = self.b.read()
			orig_img = cv2.flip(orig_img, 1)
			
			orig_img = cv2.GaussianBlur(orig_img, (5,5), 0)
			
			if i%2==0:
				rects, img = self.detect(orig_img)
				
			self.box(rects, img)
			
			cv2.imshow("FaceTracker",img)

			i+=1

			x = cv2.waitKey(5)
			if x == 1048603:
				cv2.destroyAllWindows()
				self.b.release()
				break


if __name__ == '__main__':
	tracker = FaceDetect()
	tracker.run()