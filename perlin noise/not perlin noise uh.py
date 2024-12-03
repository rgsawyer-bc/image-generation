from PIL import Image, ImageDraw
import moviepy.editor as mpe
import numpy as np
import math
import random
from gradients import *

class Fur():
    def __init__(self, width: int, height: int, speed:int, density:int, frames:int) -> None:
        self.width = width
        self.height = height
        self.speed = speed
        self.density = density
        self.frames = frames

        xs = random.choices(range(width), k = density)
        ys = random.choices(range(int(-width/2), height + int(width/2)), k = density)

        self.points = [
            [xs[i], ys[i]] for i in range(density)
        ]

        self.image = Image.new( mode = "HSV", size = (self.width, self.height) )


    def updatePoints(self, vectorField):
        for point in self.points:
            vector = vectorField(point)
            # print(vector)
            point[0] = point[0] + vector[0]
            point[1] = point[1] + vector[1]


    def plot(self, img: Image, t: int, maxt: int) -> Image:
        copy = img.copy()
        draw = ImageDraw.Draw(copy, "HSV")


        start = 200
        r = start - start * t/maxt

        # saturation = int(255*t/maxt)
        saturation = 240
        value = int(255*t/maxt)

        colorMod = int(360*t/maxt)

        for index, point in enumerate(self.points):
            x, y = point
            c = int(x/self.width*63.76 + 337.18) % 360

            draw.ellipse(
                [(x - r, y - r), (x + r, y + r)], fill = (c, saturation, value)
            )

        return copy
    

    def video(self, vectorField) -> Image:
        img = self.image
        framelist = []

        for i in range(self.frames):
            print(i)

            img = self.plot(img, i, self.frames)
            framelist.append(img)

            self.updatePoints(vectorField)

        framelist = [frame.convert("RGB") for frame in framelist]

        clips = [mpe.ImageClip(np.array(img)).set_duration(.016) for img in framelist]
        video = mpe.concatenate_videoclips(clips)
        video.write_videofile("WACKY VIDEO.mp4", fps=60)

        lastImage = framelist[-1]
        lastImage.save("last image.png")

        return lastImage
    

def radial(p: list[int | float]) -> list[float]:
    x, y = p
    return(
        (1/100)*(-y + (1080/2)),
        (1/100)*(x - (1920/2))
    )

Fur(1920, 1080, 0, 1000, 480).video(radial)