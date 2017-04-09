import cv2
import sys
import numpy as np
import pdb

WAIT = 1000

def resize_face(w, h):
    # resize face
    small = cv2.resize(faceImg, (w, h))
    # cv2.imshow("resized face", small)
    # cv2.waitKey(WAIT)
    return small

def face_swap(face, img, xPos, yPos):
    # Create a blank image with the face positioned in the correct location
    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[yPos : yPos+face.shape[0], xPos: xPos+face.shape[1]] = face
    # idea from http://stackoverflow.com/questions/12881926/create-a-new-rgb-opencv-image-using-python
    
    # Find locations of indices to slice
    locs = np.where(blank_image != 0)
    # idea from http://stackoverflow.com/questions/41572887/equivalent-of-copyto-in-python-opencv-bindings

    # Slice the indices for the face location
    img[locs[0], locs[1], locs[2]] = blank_image[locs[0], locs[1], locs[2]]
    # cv2.imshow("Face swap", img)
    # cv2.waitKey(WAIT)

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
    # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    resized = resize_face(w, h)
    face_swap(resized, image, x, y)

cv2.imshow("Faces found", image)
cv2.waitKey(0)

# Original from https://realpython.com/blog/python/face-recognition-with-python/