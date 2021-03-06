import math
import numpy as np
import cv2
import imutils

class Vision:
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier('/home/pi/jaghr-jaguar/cv/Cascades/haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

    def get_x_center(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2

    def get_y_center(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2

    def get_bounding_box(self):
        ret, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )

        # Return the bounding box of the largest detected face
        max_area = mx = my = mw = mh = 0
        for (x, y, w, h) in faces:
            if w * h > max_area:
                max_area = w * h
                (mx, my, mw, mh) = (x, y, w, h)

        # cv2.rectangle(img,(mx,my),(mx+mw,my+mh),(255,0,0),2)
        # cv2.imshow("Detect Face", img)
        # cv2.waitKey(30)
        return mx, my, mw, mh

    def get_horizontal_angle(self, relativeX):
        # Viewing angle: 54º x 41º
        hFOV = math.radians(54)
        focal = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2) / math.tan(hFOV / 2)
        return math.degrees(math.atan(relativeX / focal))

    def get_vertical_angle(self, relativeY):
        # Viewing angle: 54º x 41º
        vFOV = math.radians(41)
        focal = (self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2) / math.tan(vFOV / 2)
        return math.degrees(math.atan(relativeY / focal))

    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()

# Testing code
if __name__ == "__main__":
    faceCascade = cv2.CascadeClassifier('/home/pi/jaghr-jaguar/cv/Cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    # print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.set(3, 640) # set Width
    cap.set(4, 480) # set Height
    while True:
        ret, img = cap.read()
        # img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = imutils.resize(gray, width=540)
        # img = imutils.resize(img, width=540)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        max_area = mx = my = mw = mh = 0
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            # Detect largest face
            if w * h > max_area:
                max_area = w * h
                (mx, my, mw, mh) = (x, y, w, h)
        # print(mx, my, mw, mh)
        # print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2 - my - my / 2)
        cv2.imshow('Detect Face', img)
        k = cv2.waitKey(30) & 0xff

        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
