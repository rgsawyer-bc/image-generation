from PIL import Image, ImageDraw
import moviepy.editor as mpe
import numpy as np
import math
import random
from gradients import *

def normalize(vec: tuple[int]):
    norm = math.sqrt(vec[0]**2 + vec[1] ** 2)

    if norm == 0:
        return((0, 0))

    return (
        (vec[0] / norm, vec[1] / norm)
    )

def innerProduct(vec1: tuple[int | float], vec2: tuple[int | float]):
    return(
        vec1[0]*vec2[0] + vec1[1]*vec2[1]
    )

def fade(x: float) -> float:
    return x*x*x*(x*(x*6 - 15) + 10)

def fade2(x: float) -> float:
    return x


class PerlinGrid():
    #make top and bottom vectors equal on the boundary ??
    def __init__(self, freq: int, width: int, height: int, fade = fade, color = rgb) -> None:
        self.freq = freq
        self.height = height
        self.width = width
        self.fade = fade
        self.color = color

        #if (
        #    height % freq != 0 or width % freq != 0
        #):
        #    raise ValueError("dumb fuck")
        
        self.vecs = [
            (1, 0), (-1, 0), (0, 1), (0, -1)
        ]
        
        self.vecGrid = [[0 for i in range(width + 1)] for j in range(height + 1)]
        self.valGrid = [[0 for i in range(width + 1)] for j in range(height + 1)]

        for i in range(0, height + 1, freq):
            for j in range(0, width + 1, freq):
                # selectedVec = random.choice(self.vecs)
                #self.vecGrid[i][j] = selectedVec

                angle = math.tau * random.random()

                self.vecGrid[i][j] = (math.cos(angle), math.sin(angle))


    def getAdjacentIndeces(self, coord: tuple[int]) -> list[tuple[int]]:
        x, y = coord
        freq = self.freq
        lowX = int(x - (x % freq))
        lowY = int(y - (y % freq))

        adjacentIndeces = [
            (lowX, lowY), (lowX + freq, lowY), (lowX, lowY + freq), (lowX + freq, lowY + freq)
        ]

        return adjacentIndeces
    

    def getAdjacentVectors(self, coord: tuple[int]) -> list[tuple[int]]:
        indeces = self.getAdjacentIndeces(coord)

        vectors = [self.vecGrid[coord[1]][coord[0]] for coord in indeces]
        return vectors
    

    def getInwardVectors(self, coord: tuple[int]) -> list[tuple[int]]:
        indeces = self.getAdjacentIndeces(coord)

        unnormalized = [
            ((coord[0] - pos[0])/self.freq, (coord[1] - pos[1])/self.freq) for pos in indeces
        ]
        
        return unnormalized
    

    def getInnerProducts(self, coord: tuple[int]) -> list[tuple[int]]:
        inwards = self.getInwardVectors(coord)
        adjacent = self.getAdjacentVectors(coord)

        return(
            [innerProduct(inwards[i], adjacent[i]) for i in range(4)]
        )
    

    def getVal(self, coord: tuple[int]) -> float: # [0, 1]
        #lowx, lowx + freq, lowy + freq, both
        x, y = coord
        freq = self.freq
        modX, modY = x % freq, y % freq
        p00, p10, p01, p11 = self.getInnerProducts(coord)

        xweight = self.fade((freq - modX)/freq)
        yweight = self.fade((freq - modY)/freq)

        x1 = p00*xweight + p10*(1-xweight)
        x2 = p01*xweight + p11*(1-xweight)
        avg = x1*yweight + x2*(1-yweight)

        output = avg/2 + 1/2

        return output


    def updateVals(self):
        for y in range(self.height):
            for x in range(self.width):
                self.valGrid[y][x] = self.getVal((x,y))


    def generateImage(self):
        # self.updateVals()
        img = Image.new( mode = "RGB", size = (self.width, self.height) )
        pixels = img.load()

        for y in range(self.height):
            for x in range(self.width):
                colorVal = int(255 * self.valGrid[y][x])
                #color = self.color(colorVal)
                color = colorVal
                pixels[x, y] = color

        return(img)


class PerlinFlowField(PerlinGrid):
    def __init__(self, freq: int, width: int, height: int, speed:int, density:int, frames:int, fade = fade, color = rgb, wraparound = False, image = None) -> None:
        super().__init__(freq, width, height, fade, color)
        self.speed = speed
        self.frames = frames
        self.wraparound = False

        if image is None:
            self.image = Image.new( mode = "RGB", size = (self.width, self.height) )
        else:
            self.image = image

        # self.updateVals()

        xs = random.choices(range(width), k = density)
        ys = random.choices(range(height), k = density)

        self.points = [
            [xs[i], ys[i]] for i in range(density)
        ]

    
    def updatePoints(self):
        for point in self.points:
            # angle = self.getVal(point)
            angle = 2 * math.pi * self.getVal(point)

            xdir = self.speed * math.cos(angle)
            ydir = self.speed * math.sin(angle)

            newx = (point[0] + xdir) % self.width
            newy = (point[1] + ydir) % self.height

            point[0] = newx
            point[1] = newy
    

    def video(self) -> None:
        img = self.image
        framelist = []

        for i in range(self.frames):
            print(i)

            img = self.plot(img, i, self.frames)
            framelist.append(img)

            self.updatePoints()


        clips = [mpe.ImageClip(np.array(img)).set_duration(.016) for img in framelist]
        video = mpe.concatenate_videoclips(clips)
        video.write_videofile("WACKY VIDEO.mp4", fps=60)

        lastImage = framelist[-1]
        
        if lastImage.mode != 'RGB':
            lastImage = lastImage.convert('RGB')

        lastImage.save("last image.png")

        return lastImage


    def field(self, density: int) -> Image:
        img = Image.new( mode = "RGB", size = (self.width, self.height) )
        draw = ImageDraw.Draw(img)

        r = 8
        d = 30

        for x in range(0, self.width, density):
            for y in range(0, self.height, density):
                draw.ellipse(
                    [(x - r, y - r), (x + r, y + r)], fill = (255, 255, 255, 1)
                )

                angle = 2 * math.pi * self.getVal((x,y))

                draw.line((x, y, x + d*math.cos(angle), y + d*math.sin(angle)), width = 5)

        return img
    

class Points(PerlinFlowField):
    def __init__(self, freq: int, width: int, height: int, speed:int, density:int, frames:int, fade = fade, color = rgb, wraparound = False) -> None:
        super().__init__(freq, width, height, speed, density, frames, fade, color, wraparound)


    def plot(self, img: Image, t: int, maxt: int) -> Image:
        copy = img.copy()
        draw = ImageDraw.Draw(copy, "RGB")


        start = 200
        r = start - start * t/maxt

        saturation = int(255 - 255 * t/maxt)

        colorMod = 255*t/maxt

        for index, point in enumerate(self.points):
            x, y = point

            draw.ellipse(
                [(x - r, y - r), (x + r, y + r)], fill = self.color(colorMod)
            )

        return copy


class Fur(PerlinFlowField):
    def __init__(self, freq: int, width: int, height: int, speed:int, density:int, frames:int, fade = fade, color = rgb, wraparound = False) -> None:
        super().__init__(freq, width, height, speed, density, frames, fade, color, wraparound)


    def plot(self, img: Image, t: int, maxt: int) -> Image:
        copy = img.copy()
        draw = ImageDraw.Draw(copy, "RGB")


        start = 200
        r = start - start * t/maxt

        saturation = int(255 - 255 * t/maxt)

        colorMod = 255*t/maxt

        for index, point in enumerate(self.points):
            x, y = point

            draw.ellipse(
                [(x - r, y - r), (x + r, y + r)], fill = self.color(colorMod)
            )

        return copy
    

class MulticolorFur(PerlinFlowField):
    def __init__(self, freq: int, width: int, height: int, speed:int, density:int, frames:int, fade = fade, color = rgb, wraparound = False) -> None:
        super().__init__(freq, width, height, speed, density, frames, fade = fade, color = rgb, wraparound = False)

    
    def plot(self, img: Image, t: int, maxt: int) -> Image:
        copy = img.copy()
        draw = ImageDraw.Draw(copy, "RGB")


        start = 120
        r = start - start * t/maxt

        saturation = int(255 - 255 * t/maxt)

        colorMod = 255*t/maxt

        for index, point in enumerate(self.points):
            x, y = point

            if x < self.width / 2:
                if y < self.height / 2:
                    c = fire(colorMod)
                else:
                    c = redBlueFire(colorMod)
            else:
                if y < self.height / 2:
                    c = greenFire(colorMod)
                else:
                    c = greenRedFire(colorMod)
            draw.ellipse(
                [(x - r, y - r), (x + r, y + r)], fill = c
            )

        return copy
    

class RainbowFur(PerlinFlowField):
    def __init__(self, freq: int, width: int, height: int, speed:int, density:int, frames:int, fade = fade, color = rgb, wraparound = False, image = None) -> None:
        super().__init__(freq, width, height, speed, density, frames, fade = fade, color = rgb, wraparound = False)

        if image is None:
            self.image = Image.new( mode = "HSV", size = (self.width, self.height) )
        else:
            self.image = image


    def plot(self, img: Image, t: int, maxt: int) -> Image:
        copy = img.copy()
        draw = ImageDraw.Draw(copy, "HSV")


        start = 200
        r = start - start * t/maxt

        # saturation = int(255*t/maxt)
        saturation = 150
        value = int(255*t/maxt)

        colorMod = int(360*t/maxt)

        for index, point in enumerate(self.points):
            x, y = point
            c = int(x/self.width*63.76 + 300) % 360

            draw.ellipse(
                [(x - r, y - r), (x + r, y + r)], fill = (c, saturation, value)
            )

        return copy
    

    def video(self) -> None:
        img = self.image
        framelist = []

        for i in range(self.frames):
            print(i)

            img = self.plot(img, i, self.frames)
            framelist.append(img)

            self.updatePoints()

        framelist = [frame.convert("RGB") for frame in framelist]

        clips = [mpe.ImageClip(np.array(img)).set_duration(.016) for img in framelist]
        video = mpe.concatenate_videoclips(clips)
        video.write_videofile("WACKY VIDEO.mp4", fps=60)

        lastImage = framelist[-1]
        lastImage.save("last image.png")

        return lastImage
    

class RainbowFurNewVec(RainbowFur):
    def __init__(self, freq: int, width: int, height: int, speed:int, density:int, frames:int, fade = fade, color = rgb, wraparound = False, image = None) -> None:
        super().__init__(freq, width, height, speed, density, frames, fade = fade, color = rgb, wraparound = False)

    
    def getVal(self, coord: tuple[int]) -> float: # [0, 1]
        x, y = coord
    

class Wuh(PerlinFlowField):
    def __init__(self, freq: int, width: int, height: int, speed:int, density:int, frames:int, fade = fade, color = rgb, wraparound = False) -> None:
        super().__init__(freq, width, height, speed, density, frames, fade = fade, color = rgb, wraparound = False)

        self.pointColors = [
            self.color(i) for i in random.choices(range(256), k = density)
        ]


    def plot(self, img: Image, t: int, maxt: int) -> Image:
        copy = img.copy()
        draw = ImageDraw.Draw(copy, "RGB")


        start = 200
        r = start - start * t/maxt

        saturation = int(255 - 255 * t/maxt)

        colorMod = 255*t/maxt
        c = greenRedFire(colorMod)

        for index, point in enumerate(self.points):
            x, y = point
            color = self.pointColors[index]

            draw.ellipse(
                [(x - r, y - r), (x + r, y + r)], outline = color, width = 5
            )

        return copy
    

class Wuhg(PerlinFlowField):
    def __init__(self, freq: int, width: int, height: int, speed:int, density:int, frames:int, fade = fade, color = rgb, wraparound = False) -> None:
        super().__init__(freq, width, height, speed, density, frames, fade = fade, color = rgb, wraparound = False)

        self.pointColors = [
            self.color(i) for i in random.choices(range(256), k = density)
        ]


    def plot(self, img: Image, t: int, maxt: int) -> Image:
        copy = img.copy()
        draw = ImageDraw.Draw(copy, "RGBA")


        start = 200
        r = start - start * t/maxt

        opacity = 100

        colorMod = 255*t/maxt
        c = greenRedFire(colorMod)

        for index, point in enumerate(self.points):
            x, y = point
            color = self.pointColors[index]

            draw.ellipse(
                [(x - r, y - r), (x + r, y + r)], outline = color, width = 20
            )

        return copy


a = RainbowFur(500, 2000, 1000, speed = 2, density = 1000, frames = 240, fade = fade)
# a = PerlinFlowField(500, 1500, 1500, speed = 2, density = 500, frames = 240, fade = fade)

a.video()