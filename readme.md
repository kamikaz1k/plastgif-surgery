# Development Plan

1. ~Finding faces in input image~
2. ~Scale new face image to the area of the found faces~
3. ~copy scaled face into original image~
4. ~preserve transparency for png images~
5. ~Run it iteratively for a gif~
6. Find the face in the face image and use that to rescale instead of the image dimensions


# Dependencies (3.6)
* imageio==2.3.0
* numpy==1.14.5
* opencv-python==3.4.1.15
* Pillow==5.1.0

## How to setup dependencies
```
virtualenv venv # create virtualenv
source venv/bin/activate # activate virtualenv
pip install -r requirements.txt # install dependencies
```

# Dependencies (2.7)
* numpy==1.12.1
* opencv==2.4.13.2
* imageio==2.1.2 (for gif splitting/rendering)


## (Old) How to setup dependencies
You can get numpy and imageio from pip
For OpenCV I used homebrew (`brew install opencv`)
(I tried to compile from source but I kept encountering issues...)

# How to use
## First, get the source:
```
git clone https://github.com/kamikaz1k/plastgif-surgery.git
```

## Option 1. Serve as a web app
```
pip install flask # install flask for webserver
python app.py # start server
# visit http://localhost:5000/
```

## Option 2. Run in your own python script
```
import face_swap
face_swap.plastgifSurgery("source.gif", "face.png", "output.gif")
```

## Option 3. Run from console
```
cd plastgif-surgery
python face_detect_cv3.py <path/to/image> <path/to/face>[ <path/to/output>]
```

Takes a source image and a face image as arguments. (Even animated gifs...)
If the image has any faces, it will copy over it with the face image.

**Arguments:**

`<source>` image can be any format supported by opencv
`<face>` image can be any format support by opencv
If `<face>` is a PNG with an alpha channel, program will try to use to it

# Example Input:
`python face_detect_cv3.py source.gif face.png output`

*Source:*

![source.gif](source.gif)

*Face:*

![face.png](face.png)

*Output:*

![output.gif](output.gif)

# All the things I leaned to get this thing working:
* Inspiration: http://blog.zikes.me/post/how-i-ruined-office-productivity-with-a-slack-bot/
* Starting point: https://realpython.com/blog/python/face-recognition-with-python/
* Understanding masks and early numpy: http://stackoverflow.com/a/41573727/4765841
* Advanced masking to handle PNG alpha channel: http://docs.opencv.org/trunk/d0/d86/tutorial_py_image_arithmetics.html
* Numpy trick 1 (omit alpha): http://stackoverflow.com/a/35902359/4765841
* Numpy trick 2 (splice indices): http://stackoverflow.com/a/12890573/4765841
* Numpy trick 3 (swap channels): http://stackoverflow.com/a/39270509/4765841

## Interested in how I made this? [Read my post!](https://medium.com/@kamikaz1_k/programming-skills-to-be-useless-while-feeling-productive-776fa97dca35)
