from math import sqrt, sin, cos, pi

class Triangle:
    def __init__(self, center: tuple[int], sidelen: int, color: tuple[int], orientation: str = "down") -> None:
        self.center = center
        self.sidelen = sidelen
        self.color = color

        x, y = center
        h = sidelen * sqrt(3) / 2
        low = y - h/3
        high = y + 2*h/3

        if orientation == "down":
            self.indeces = [
                (x - sidelen/2, low), (x + sidelen/2, low), (x, high)
            ]
        else:
            self.indeces = [
                (x - sidelen/2, high), (x + sidelen/2, high), (x, low)
            ]

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