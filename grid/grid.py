from triangle import *
from PIL import Image, ImageDraw
from math import sqrt
import random


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

TriangleGrid(1920, 1080, 100, 8).generateImage()