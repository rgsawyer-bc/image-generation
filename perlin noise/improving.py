import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from PIL import Image, ImageDraw
import numpy as np
import math
import random
from gradients import *
from moviepy import *


noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

print('g')

w = 1000
h = 1000

xpix, ypix = w, h
time = 1
slow = 1
speed = 1/3
frames = []
for t in range(0, time, slow):
    print(t/time)
    frame = Image.new("RGB", (w, h))
    pixels = frame.load()
    elapsed = t/time*speed
    for i in range(xpix):
        for j in range(ypix):
            tiles = [1,1,1]
            x = i/xpix
            y = j/ypix
            noise_val = noise1([x, y, elapsed], tile_sizes = tiles) + .5
            noise_val += 0.5 * (noise2([x, y, elapsed], tile_sizes = tiles) + .5)
            noise_val += 0.25 * (noise3([x, y, elapsed]) + .5)
            noise_val += 0.125 * (noise4([x, y, elapsed]) + .5)

            val = int(noise_val * 255/1.75)


            pixels[i, j] = fire(val)

    frames.append(frame)

clips = [ImageClip(np.array(img)).with_duration(.016*slow) for img in frames]
video = concatenate_videoclips(clips)
video.write_videofile('perlin noise/outputs/multilayer perlin noise.mp4', fps=int(60/slow))

frame.save('perlin noise/outputs/multilayer perlin noise.png')