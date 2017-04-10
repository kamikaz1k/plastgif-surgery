import cv2
import sys
import numpy as np
import pdb
import imageio

WAIT = 1000
DEBUG = False

def resize_face(faceImg, w, h):
    # resize face
    small = cv2.resize(faceImg, (w, h))
    # cv2.imshow("resized face", small)
    # cv2.waitKey(WAIT)
    return small

def face_swap(face, img, xPos, yPos):

    hasAlpha = True if face.shape[2] == 4 else False
    if hasAlpha and DEBUG:
        print "It has alpha channel!"

    if DEBUG:
        cv2.imshow("Face before", face)
        cv2.waitKey(200)

    # split out the alpha channel
    if hasAlpha:
        b,g,r,mask = cv2.split(face)
        # do a threshold mask to zero out alpha 0
        face = cv2.bitwise_and(face, face, mask=mask)

    if DEBUG:
        cv2.imshow("Face after", face)
        cv2.waitKey(200)

    # Create a blank image with the face positioned in the correct location
    blank_image = np.zeros((img.shape[0], img.shape[1], face.shape[2]), np.uint8)
    blank_image[yPos : yPos+face.shape[0], xPos: xPos+face.shape[1]] = face
    # idea from http://stackoverflow.com/questions/12881926/create-a-new-rgb-opencv-image-using-python
    
    # drop the alpha channel
    if hasAlpha:
        blank_image = blank_image[:, :, :3]

    # Find locations of indices to slice
    locs = np.where(blank_image != 0)
    # idea from http://stackoverflow.com/questions/41572887/equivalent-of-copyto-in-python-opencv-bindings

    # Slice the indices for the face location
    img[locs[0], locs[1], locs[2]] = blank_image[locs[0], locs[1], locs[2]]
    # cv2.imshow("Face swap", img)
    # cv2.waitKey(WAIT)

def find_and_replace(image, face):

    # Create the haar cascade
    cascPath = "haarcascade_frontalface_default.xml" 
    faceCascade = cv2.CascadeClassifier(cascPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        resized = resize_face(face, w, h)
        face_swap(resized, image, x, y)

    return image

if __name__ == "__main__":
    '''Takes a source image and a face image as arguments. 
    If the image has any faces, it will copy over it with the face image 

    Arguments:
    arg1 -- <source>
    arg2 -- <face>
    <source> image can be any format supported by opencv
    <face> image can be any format support by opencv. 
    If <face> is a PNG with an alpha channel, program will try to use to it
    '''
    # Get user supplied values
    imagePath = sys.argv[1]
    facePath = sys.argv[2]

    print "arguments given", imagePath, facePath

    face = cv2.imread(facePath, -1)

    # if gif
    if imagePath.endswith("gif"):
        images = imageio.mimread(imagePath)
        output = []
        for image in images:
            # switch from RGB to BGR
            r,g,b,a = cv2.split(image)
            image = cv2.merge((b,g,r))
            image = find_and_replace(image, face)
            output.append(image)
            if DEBUG:
                cv2.imshow("Faces found", output[-1])
                cv2.waitKey(0)
        pdb.set_trace()
        imageio.mimwrite("output.gif", output)

    else:
        # Read the image
        image = cv2.imread(imagePath)

        image = find_and_replace(image, face)

        cv2.imshow("Faces found", image)
        cv2.waitKey(0)

# Original from https://realpython.com/blog/python/face-recognition-with-python/