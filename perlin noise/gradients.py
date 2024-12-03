# all must take an integer in [0,255] and return an rgb tuple

from math import sin, cos, pi

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
        (red(x, width), green(x, width), blue(x, width))
    )

def fire(x):
    x = x/255
    r = (19/40) * sin(pi*x - (pi/2)) + (21/40)
    g = 0 if x <= .5 else 2*x - 1

    return (int(255*r), int(255*g), 0)

def redBlueFire(x):
    x = x/255
    r = (19/40) * sin(pi*x - (pi/2)) + (21/40)
    b = 0 if x <= .5 else 2*x - 1

    return (int(255*r), 0, int(255*b))

def blueFire(x):
    x = x/255
    b = (19/40) * sin(pi*x - (pi/2)) + (21/40)
    g = 0 if x <= .5 else 2*x - 1

    return (0, int(255*g), int(255*b))

def greenFire(x):
    x = x/255
    g = (19/40) * sin(pi*x - (pi/2)) + (21/40)
    b = 0 if x <= .5 else 2*x - 1

    return (0, int(255*g), int(255*b))

def greenRedFire(x):
    x = x/255
    g = (19/40) * sin(pi*x - (pi/2)) + (21/40)
    r = 0 if x <= .5 else 2*x - 1

    return (int(255*r), int(255*g), 0)

def bw(x):
    bruh = int(x)
    return (bruh, bruh, bruh)

def redYellow(x):
    return (255, int(255 - x), 100)