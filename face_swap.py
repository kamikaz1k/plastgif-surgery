from __future__ import print_function
import cv2
import imageio
import numpy as np


def resizeFaceWithinBox(face, width, height):
    return cv2.resize(face, (width, height))

def copyFaceWithinBox(image, face, xPos, yPos, width, height):

    face = resizeFaceWithinBox(face, width, height)

    hasAlpha = face.shape[2] == 4

    # split out the alpha channel
    if hasAlpha:
        b,g,r,mask = cv2.split(face)
        # do a threshold mask to zero out pixel using alpha channel
        face = cv2.bitwise_and(face, face, mask=mask)
        # drop the alpha channel
        face = face[:,:,:3]

    # Find locations of indices to slice
    locs = np.where(face != 0)

    # Slice the indices for the face location
    image[locs[0]+yPos, locs[1]+xPos, locs[2]] = face[locs[0], locs[1], locs[2]]

    return image

def findFaces(image, cascPath="haarcascade_frontalface_default.xml"):

    faceCascade = cv2.CascadeClassifier(cascPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def getFrames(imagePath):
    frames = imageio.mimread(imagePath)
    return frames

def saveGifImage(image, imagePath):
    # since imageio reads as RGB
    # you need to save with imageio too
    imageio.imwrite(imagePath, image)

def readImage(imagePath):
    return cv2.imread(imagePath)

def readTransparentImage(imagePath, mode="BGR"):
    if mode == "RGB":
        image = imageio.imread(imagePath)
    else:
        image = cv2.imread(imagePath, -1)

    return image

def replaceFaces(image, face, faceIndex=-1):

    faces = findFaces(image)

    if faceIndex > -1 and faces[faceIndex]:
        return copyFaceWithinBox(image, face, *faces[faceIndex])

    for dims in faces:
        image = copyFaceWithinBox(image, face, *dims)

    return image

def swapFacesUsingFrameData(bgPath, facePath, outputPath, frames):

    if not bgPath.endswith(".gif"):
        raise ValueError("bgPath must be a gif")

    # Read in images
    images = getFrames(bgPath)
    durations = [frame['duration'] for frame in frames]

    face = readTransparentImage(facePath, mode="RGB")
    output = []

    for idx, image in enumerate(images):
        # image = replaceFaces(image, face)
        image = copyFaceWithinBox(image, face, frames[idx]['x'], frames[idx]['y'], frames[idx]['w'], frames[idx]['h'])
        output.append(image)

    outputPath = outputPath if outputPath.endswith(".gif") else outputPath + ".gif"
    imageio.mimwrite(outputPath, output, duration=durations)

    return outputPath

def plastgifSurgery(bgPath, facePath, outputPath="output"):

    if bgPath.endswith(".gif"):
        # Read in images
        images = getFrames(bgPath)
        durations = [image.meta['duration']/1000 for image in images]

        face = readTransparentImage(facePath, mode="RGB")
        output = []

        for image in images:
            image = replaceFaces(image, face)
            output.append(image)

        outputPath = outputPath if outputPath.endswith(".gif") else outputPath + ".gif"
        imageio.mimwrite(outputPath, output, duration=durations)

    else:
        # Read the images
        image = readImage(bgPath)
        face = readTransparentImage(facePath)

        image = replaceFaces(image, face)
        outputPath = outputPath + ".png"

        cv2.imwrite(outputPath, image)

    return outputPath


if __name__ == "__main__":

    import sys

    imagePath = sys.argv[1]
    facePath = sys.argv[2]
    image = cv2.imread(imagePath)
    face = cv2.imread(facePath, -1)

    locs = findFaces(image)
    image = copyFaceWithinBox(
        image,
        face,
        locs[0][0],
        locs[0][1],
        locs[0][2],
        locs[0][3]
    )

    cv2.imwrite("trimmed.png", image)