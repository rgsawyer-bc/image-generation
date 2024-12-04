from triangle import *
from PIL import Image, ImageDraw
from math import sqrt
import random
from gradientPolygon import linear_gradient


class TriangleGrid:
    def __init__(self, width: int, height: int, s: int, outline: int) -> None:
        self.width = width
        self.height = height
        self.s = s
        self.outline = outline


    def generateImage(self) -> Image:
        img = Image.new("HSV", (self.width, self.height))
        draw = ImageDraw.Draw(img, "HSV")

        h = self.s*sqrt(3)/2

        y = 0
        yorientation = "up"

        while y < self.height:
            x = 0
            xorientation = yorientation

            while x < self.width + 2 * self.s:
                center = (x, y)

                saturation = random.choice(range(140, 180))
                difference = random.choice(range(20, 40))

                value = random.choice(range(230, 255))

                hueBase = int(x*y/self.width/self.height * 255)
                hueDifference = 50

                hue = random.choice(range(hueBase, hueBase + hueDifference))
                centerColor = (hue, saturation, value)
                outlineColor = (hue, saturation - difference, value)

                t = Triangle(center, self.s, color = centerColor, orientation = xorientation)
                draw.polygon(t.indeces, fill = t.color, outline = outlineColor, width = self.outline)
                xorientation = "up" if xorientation == "down" else "down"
                x += self.s/2
                
            yorientation = "up" if yorientation == "down" else "down"
            y += h

            
        img = img.convert("RGB")
        img.save("grid/test.png")

        return img
    

class GradientTriangleGrid:
    def __init__(self, width: int, height: int, s: int, outline: int) -> None:
        self.width = width
        self.height = height
        self.s = s
        self.outline = outline


    def generateImage(self) -> Image:
        bigWidth = self.width + 2 * self.s
        bigHeight = self.height + 2 * self.s
        img = Image.new("RGBA", (bigWidth, bigHeight))

        h = self.s*sqrt(3)/2

        y = h
        yorientation = "up"

        while y < bigHeight:
            print(y/self.height)
            x = self.s/2
            xorientation = yorientation

            while x < bigWidth:
                center = (x, y)

                hueBase = int(x*y/bigWidth/bigHeight * 120 + 120) # *255
                hueDifference = 20 # 50

                gradientDifference = 12 # 25

                hue = random.choice(range(hueBase, hueBase + hueDifference))
                c1 = rgb(hue, width = 255)
                c2 = rgb(hue + gradientDifference, width = 255)

                t = Triangle(center, self.s, color = (0, 0, 0), orientation = xorientation)
                gradIndeces = random.sample(t.indeces, 2)
                img = linear_gradient(img, t.indeces, gradIndeces[0], gradIndeces[1], c1, c2)
                xorientation = "up" if xorientation == "down" else "down"
                x += self.s/2
                
            yorientation = "up" if yorientation == "down" else "down"
            y += h

        img.save("grid/bigger.png")

        img = img.crop((self.s, self.s, self.width + self.s, self.height + self.s))

        img.save("grid/gradient test.png")

        return img

GradientTriangleGrid(1920, 1080, 100, 8).generateImage()