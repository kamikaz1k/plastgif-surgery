# Development Plan

1. ~Finding faces in input image~
2. ~Scale new face image to the area of the found faces~
3. ~copy scaled face into original image~
4. ~preserve transparency for png images~
5. ~Run it iteratively for a gif~
6. Find the face in the face image and use that to rescale instead of the image dimensions

# Dependencies
* numpy==1.12.1
* opencv==2.4.13.2
* imageio==2.1.2 (for gif splitting/rendering)

# How to setup dependencies
You can get numpy and imageio from pip
For OpenCV I used homebrew (`brew install opencv`)
(I tried to compile from source but I kept encountering issues...)

# How to use
## Option 1. (and only) Get the source
```
git clone https://github.com/kamikaz1k/plastgif-surgery.git
cd plastgif-surgery
python face_detec_cv3.py <path/to/image> <path/to/face>[ <path/to/output>]
```

Takes a source image and a face image as arguments. (Even animated gifs...)
If the image has any faces, it will copy over it with the face image.

**Arguments:**

`<source>` image can be any format supported by opencv
`<face>` image can be any format support by opencv
If `<face>` is a PNG with an alpha channel, program will try to use to it

## Example Input:
`python face_detec_cv3.py source.gif face.png output`

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