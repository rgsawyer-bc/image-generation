from PIL import Image, ImageDraw
import numpy as np
from math import sin, cos, pi
import random

import scipy

def red(x, width = 1920):
    return(int(
      127.5*sin((pi/width)*(2*x-width/2))+127.5
    ))
def green(x, width = 1920):
    return(int(
      127.5*sin((pi/width)*(2*x-(7*width)/6))+127.5
    ))
def blue(x, width = 1920):
    return(int(
      127.5*sin((pi/width)*(2*x-(11*width)/6))+127.5
    ))

def rgb(x, width = 255):
    return(
        [red(x, width), green(x, width), blue(x, width)]
    )

width = 1000
height = 1000

img = Image.new( "RGB", (width, height) )
draw = ImageDraw.Draw(img, "RGBA")

maxscale = 250

startCircles = 100
endCircles = 50
maxj = 100
step = 5

slope = (startCircles - endCircles)/maxj


for j in range(0, maxj, step):
    r = 100 - j
    circles = int(startCircles - slope*j)
    opacity = int((j/8)**2)
    xs = scipy.stats.norm.rvs(loc = width/2, scale = maxscale - j*3/4, size = circles) #maxscale = 200, -j*1/2
    ys = scipy.stats.norm.rvs(loc = height/2, scale = maxscale - j*3/4, size = circles)
    points = [(xs[i], ys[i]) for i in range(circles)]

    c = rgb(j*2)

    c.append(opacity)
    c = tuple(c)

    for i in range(circles):
        x, y = points[i]
        draw.ellipse(
            [(x - r, y - r), (x + r, y + r)], fill = c
        )

img.save("trying to make a paint splotch/bargain.png")