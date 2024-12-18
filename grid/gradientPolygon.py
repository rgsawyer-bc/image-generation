import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


# Draw polygon with linear gradient from point 1 to point 2 and ranging
# from color 1 to color 2 on given image
def linear_gradient(i, poly, p1, p2, c1, c2):

    # Draw initial polygon, alpha channel only, on an empty canvas of image size
    ii = Image.new('RGBA', i.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(ii)
    draw.polygon(poly, fill=(0, 0, 0, 255), outline=None)

    # Calculate angle between point 1 and 2
    p1 = np.array(p1)
    p2 = np.array(p2)
    angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0]) / np.pi * 180

    # Rotate and crop shape
    temp = ii.rotate(angle, expand=True)
    temp = temp.crop(temp.getbbox())
    wt, ht = temp.size

    # Create gradient from color 1 to 2 of appropriate size
    gradient = np.linspace(c1, c2, wt, True).astype(np.uint8)
    gradient = np.tile(gradient, [2 * h, 1, 1])
    gradient = Image.fromarray(gradient)

    gradient.save("grid/what is that 1.png")

    # Paste gradient on blank canvas of sufficient size
    temp = Image.new('RGBA', (max(i.size[0], gradient.size[0]),
                              max(i.size[1], gradient.size[1])), (0, 0, 0, 0))
    temp.paste(gradient)
    temp.save("grid/what is that 2.png")
    gradient = temp

    # Rotate and translate gradient appropriately
    x = np.sin(angle * np.pi / 180) * ht
    y = np.cos(angle * np.pi / 180) * ht
    gradient = gradient.rotate(-angle, center=(0, 0),
                               translate=(p1[0] + x, p1[1] - y))
    
    gradient.save("grid/what is that 3.png")

    # Paste gradient on temporary image
    ii.paste(gradient.crop((0, 0, ii.size[0], ii.size[1])), mask=ii)

    ii.save("grid/what is that 4.png")

    # Paste temporary image on actual image
    i.paste(ii, mask=ii)

    return i


# Create blank canvas with zero alpha channel
w, h = (800, 600)
image = Image.new('RGBA', (w, h), (0, 0, 0, 0))

# Draw second polygon with linear gradient
polygon = [(500, 50), (650, 250), (775, 150), (700, 25)]
point1 = (700, 25)
point2 = (650, 250)
color1 = (255, 255, 0)
color2 = (0, 0, 255)
image = linear_gradient(image, polygon, point1, point2, color1, color2)

# Draw third polygon with linear gradient
polygon = [(50, 550), (200, 575), (200, 500), (100, 300), (25, 450)]
point1 = (100, 300)
point2 = (200, 575)
color1 = (255, 255, 255)
color2 = (255, 128, 0)
image = linear_gradient(image, polygon, point1, point2, color1, color2)