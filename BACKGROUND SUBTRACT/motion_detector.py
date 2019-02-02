# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import urllib
import numpy as np
cnt=0;
time.sleep(5);
webcam = cv2.VideoCapture(0)
firstFrame = None
fgbg = cv2.createBackgroundSubtractorMOG2()
cnt=1
while True:
##        imgPath=urllib.urlopen(url)
##        imgNp=np.array(bytearray(imgPath.read()),dtype=np.uint8)
##        frame=cv2.imdecode(imgNp,-1)
        fr,frame=webcam.read();
        cnt=cnt+1
        val=str(cnt)+'.jpg'
        cv2.imwrite(val,frame)
        text = "Unoccupied"

        # resize the frame, convert it to grayscale, and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the first frame is None, initialize it
        if firstFrame is None:
                firstFrame = gray
                continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = fgbg.apply(gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        # loop over the contours
        for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                img=frame;
##                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if cv2.contourArea(c) > 10000:
                        ImageCropped=img[y:y+w,x:x+h];
                        cnt=cnt+1;
                        text='occupied'
##        if len(cnts) > 0:
##                        # find the largest contour in the mask, then use
##                        # it to compute the minimum enclosing circle and
##                        # centroid
##                c2 = max(cnts, key=cv2.contourArea)
##                ((x, y), radius) = cv2.minEnclosingCircle(c2)
##                M = cv2.moments(c2)
##                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
##                print c2
	# draw the text and timestamp on the frame
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
                break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
