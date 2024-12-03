import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from PIL import Image, ImageDraw
import numpy as np
import math
import random
from gradients import *
from moviepy import *

class PerlinColors:
    def __init__(self, width: int, height: int, density: int, octaves: int, opacity: int = 100) -> None:
        self.height = height
        self.width = width
        self.density = density
        self.opacity = opacity

        frac = 4/5

        xs = random.choices(range(width), k = density)
        ys = random.choices(range(height), k = density)
        self.points = [[xs[i], ys[i]] for i in range(density)]
        self.radii = random.choices(range(5, 100), k = int(frac * density))
        self.radii += random.choices(range(5, 20), k = density - int(frac * density))

        self.noise = PerlinNoise(octaves = octaves)

        self.xnoise = PerlinNoise(octaves = 10)
        self.xoffsets = random.choices([i/1000 for i in range(10000)], k = density)
        self.ynoise = PerlinNoise(octaves = 10)
        self.yoffsets = random.choices([i/1000 for i in range(10000)], k = density)


    def generateImage(self, time = 0) -> Image:
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img, "RGBA")

        for index, point in enumerate(self.points):
            xoffset = self.xoffsets[index]
            yoffset = self.yoffsets[index]

            r = self.radii[index]
            opacity = int(1/(.001 * r) - 5)

            x = point[0] + (60 - r/2) * self.xnoise([xoffset + 5*time/6])
            y = point[1] + (60 - r/2) * self.ynoise([yoffset + 5*time/6])

            perlinVal = self.noise([x/self.height, y / self.height, time]) + .5
            c = rgb(perlinVal + 1.5, width = 2)
            ca = c + tuple([opacity])

            # c = rgb(r + 100, width = 300)
            # ca = c + tuple([opacity])

            draw.ellipse(
                [(x - r, y - r), (x + r, y + r)], fill = ca
            )

        return img
    

    def generateVideo(self, frames: int, speed: int) -> None:
        framelist = []
        for time in range(frames):
            t = time/60*speed
            print(t)
            framelist.append(self.generateImage(t*speed))

        clips = [ImageClip(np.array(img)).with_duration(.016) for img in framelist]
        video = concatenate_videoclips(clips)
        video.write_videofile('perlin noise/outputs/perlin colors.mp4', fps=int(60))

        
    
a = PerlinColors(1920, 1080, 5000, 4, opacity = 25)
a.generateImage().save("perlin noise/outputs/g.png")
# a.generateVideo(60, speed = 1/8)

