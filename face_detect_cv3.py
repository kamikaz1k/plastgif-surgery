import cv2
import sys
import numpy as np

WAIT = 1000

def resize_face(x, y, w, h):
    # resize face
    small = cv2.resize(faceImg, (w, h))
    cv2.imshow("resized face", small)
    cv2.waitKey(WAIT)

# Get user supplied values
imagePath = sys.argv[1]
cascPath = sys.argv[2]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
    #flags = cv2.CV_HAAR_SCALE_IMAGE
)

print("Found {0} faces!".format(len(faces)))

faceImg = cv2.imread("face.png")

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    resize_face(x, y, w, h)

cv2.imshow("Faces found", image)
cv2.waitKey(WAIT)

# Original from https://realpython.com/blog/python/face-recognition-with-python/