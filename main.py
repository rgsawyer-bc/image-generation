from PIL import Image, ImageDraw, ImageFont
from numpy import sin
import numpy as np
import random
import ImageChops as ic
from io import BytesIO
from datetime import datetime

from point import Point

def getTime():
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  return(current_time)

pi = 3.14159265358979323846


def red(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-width/2))+127.5
    )
def green(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-(7*width)/6))+127.5
    )
def blue(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-(11*width)/6))+127.5
    )

def rainbow(type = 'square', width = 1920, height = 1080, maxsquaresize = 100, opacity = 100, skipsave = False):
  print('Generating...')
  img = Image.new( mode = "RGB", size = (width, height) )
  draw = ImageDraw.Draw(img, 'RGBA')
  
  def red(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-width/2))+127.5
    )
  def green(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-(7*width)/6))+127.5
    )
  def blue(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-(11*width)/6))+127.5
    )

  font1 = ImageFont.truetype('Creepster-Regular.ttf', 100)
  
  for x in range(-1 * maxsquaresize, width):
    yloc = np.random.randint(height) - maxsquaresize/2
    squaresize = np.random.randint(maxsquaresize)
    draw.ellipse([(x,yloc),(x+squaresize,yloc+squaresize)], fill=(int(red(x, width)), int(green(x, width)), int(blue(x, width)), opacity))
    #draw.text((width/2,height/2), text = 'splendid', font = font1, fill = (255, 255, 255, 255))
  if skipsave == True:
    pass
  else:
    print('Saving...')
    img.save('rainbow.png')
    print('Done!')
  return(img)

def rainbowgif(width = 1920, height = 1080, maxsquaresize = 100, opacity = 100, frames = 40):
  print('Generating...')
  framelist = []
  for i in range(frames):
    framelist.append(rainbow(width = width, height = height, maxsquaresize = 75+(100//frames)*3*i, opacity = 100-(100//frames)*i), skipsave = True)
  print('Saving...')
  framelist[0].save('rainbowgif.gif', save_all = True, append_images = framelist[1:], duration = 50, loop = 0)
  print('Done!')

def movingsquares(filename = 'redrain.gif', width = 1920, height = 1080, maxsquarelen = 100, opacity = 100, frames = 40):

  xvellower, xvelupper, yvellower, yvelupper = 10, 20, 10, 20
  
  print('Generating...')
  squares = [Point(x = i, 
                   y = random.randrange(-maxsquarelen, height + maxsquarelen + 1),
                   velx = random.randrange(xvellower, xvelupper), 
                   vely = random.randrange(yvellower, yvelupper), 
                   accx = 0, accy = 0, 
                   color = (255, 0, 0),
                   opacity = 100, type = 'square', 
                   sidelen = random.randrange(maxsquarelen))
             for i in range(-maxsquarelen, width + maxsquarelen + 1)]
  framelist = []
  for frame in range(frames):
    print(frame)
    img = Image.new( mode = "RGB", size = (width, height) )
    draw = ImageDraw.Draw(img, 'RGBA')
    for i in squares:
      draw.polygon(xy = i.indeces, fill = (i.r, i.g, i.b, i.opacity))
      i.updatePos(1),
      i.resetPos(i.sidelen, width, height)
      i.updateSquare()
    framelist.append(img)
  print('Saving... (this may take a while)')
  framelist[0].save(filename, save_all = True, append_images = framelist[1:], duration = 50, loop = 0)
  print('Done!')

def cascadingSquares(squares = 40, filename = 'redrain.gif', width = 1920, height = 1080, maxsquarelen = 100, opacity = 100, frames = 40):
  squares = [Point(
    x = width/2,
    y = height/2,
    velx = 0,
    vely = 0,
    accx = 0,
    accy = 0,
    rot = 0,
    velrot = i,
    accrot = 0, #-.025 * i + .1,
    color = (int(red(120*i)), int(green(120*i)), int(blue(120*i))),
    opacity = 255,
    type = 'square',
    sidelen = 500 - 10*i) for i in range(40)
  ]
  framelist = []
  for frame in range(frames):
    img = Image.new( mode = "RGB", size = (width, height) )
    draw = ImageDraw.Draw(img, 'RGBA')
    for i in squares:
      draw.polygon(xy = i.indeces, fill = (i.r, i.g, i.b, i.opacity))
      i.updatePos(1)
      i.updateRot(1)
      i.resetPos(maxsquarelen, width, height)
      i.updateSquare()
    framelist.append(img)
  print('Saving... (this may take a while)')
  framelist[0].save('joog.gif', save_all = True, append_images = framelist[1:], duration = 50, loop = 0)
  print('Done!')
  #270 frames for a perfect loop

def addTest(squares = 40, filename = 'redrain.gif', width = 1920, height = 1080, maxsquarelen = 100, opacity = 100, frames = 40):
  rainbowtop = rainbow(width = width, height = height)
  squares = [Point(
    x = -height,
    y = height/2,
    velx = 4*i,
    vely = 0,
    accx = 0,
    accy = 0,
    rot = 0,
    velrot = i,
    accrot = 0, #-.025 * i + .1,
    color = (0, 0, 0),
    opacity = 80,
    type = 'square',
    sidelen = int(height - (height/50)*i)) for i in range(40)
  ]
  print('Generating...')
  framelist = []
  for frame in range(frames):
    img = Image.new( mode = "RGB", size = (width, height), color = (255, 255, 255) )
    draw = ImageDraw.Draw(img, 'RGBA')
    for i in squares:
      draw.polygon(xy = i.indeces, fill = (i.r, i.g, i.b, i.opacity))
      i.updatePos(1, airresist = True, k = .05)
      i.updateRot(1, airresist = True, k = .05)
      #i.resetPos(maxsquarelen, width, height)
      i.updateSquare()
    framelist.append(ic.add(img, rainbowtop))
  print('Saving... (this may take a while)')
  framelist[0].save('will this work 2.gif', save_all = True, append_images = framelist[1:], duration = 50, loop = 0)
  print('Done!')

def bokeh(image, density = 16, clustersize = 3, opacitymodifier = 9, lowersizerange = 0, uppersizerange = 200, sort = False):
  print('\n--Bokeh Image Generation--')
  if type(image) == str:
    img = Image.open(image)
    img = img.convert('RGB')
  else:
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img, 'RGBA')
  xsize, ysize = img.size[0], img.size[1]
  if clustersize%2 == 0:
    clustermodifier = int((1/2)*(clustersize-2) + 1)
  else:
    clustermodifier = int((1/2)*(clustersize-2) + .5)
  #print(clustermodifier)

  print(f'Initializing {getTime()}')
  points = []
  for i in range(clustermodifier, xsize - clustermodifier, density): #clustersize this
    for j in range(1, ysize - clustermodifier, density): #clustersize this
      pixels = [(img.getpixel((x,y))) for x in range(i-clustermodifier, i+clustermodifier+1) for y in range(j-clustermodifier, j+clustermodifier+1)]
      colors = (
        sum(tuple[0] for tuple in pixels)/(clustersize ** 2), #clustersize this
        sum(tuple[1] for tuple in pixels)/(clustersize ** 2),
        sum(tuple[2] for tuple in pixels)/(clustersize ** 2)
      )
      points.append(Point(
        x = i,
        y = j,
        type = 'square',
        color = (colors[0], colors[1], colors[2]),
        opacity = int(sum(colors)/opacitymodifier), #clustersize this
        sidelen = random.randrange(lowersizerange, uppersizerange)
      ))
  newimg = Image.new( mode = "RGB", size = (xsize, ysize) )
  draw = ImageDraw.Draw(newimg, 'RGBA')
  print(f'Generating {getTime()}')

  if sort == True:
    def opacity(point):
      return(point.opacity)
    points.sort(key = opacity)
  
  for i in points:
    #print(i.indeces[1], i.indeces[3])
    #print(i.r, i.g, i.b)
    draw.ellipse([i.indeces[3], i.indeces[1]], fill = (i.r, i.g, i.b, i.opacity))
  print(f'Saving {getTime()}')
  newimg.save('bokeh.jpg')
  print(f'Finished {getTime()}')
  return(newimg)

def bokehmoving(image, density = 16, clustersize = 3, opacitymodifier = 9, lowersizerange = 0, uppersizerange = 200, sort = False, lowervelx = 0, uppervelx = 20, lowervely = 0, uppervely = 20, framecount = 20):
  print('\n--Bokeh GIF Generation--')
  if type(image) == str:
    img = Image.open(image)
    img = img.convert('RGB')
  else:
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img, 'RGBA')
  xsize, ysize = img.size[0], img.size[1]
  if clustersize%2 == 0:
    clustermodifier = int((1/2)*(clustersize-2) + 1)
  else:
    clustermodifier = int((1/2)*(clustersize-2) + .5)
  #print(clustermodifier)

  print(f'Initializing {getTime()}')
  points = []
  for i in range(clustermodifier, xsize - clustermodifier, density): #clustersize this
    for j in range(1, ysize - clustermodifier, density): #clustersize this
      pixels = [(img.getpixel((x,y))) for x in range(i-clustermodifier, i+clustermodifier+1) for y in range(j-clustermodifier, j+clustermodifier+1)]
      colors = (
        sum(tuple[0] for tuple in pixels)/(clustersize ** 2), #clustersize this
        sum(tuple[1] for tuple in pixels)/(clustersize ** 2),
        sum(tuple[2] for tuple in pixels)/(clustersize ** 2)
      )
      points.append(Point(
        x = i,
        y = j,
        velx = random.randrange(lowervelx, uppervelx+1) if lowervelx != uppervelx else lowervelx,
        vely = random.randrange(lowervely, uppervely+1) if lowervely != uppervely else lowervely,
        type = 'square',
        color = (colors[0], colors[1], colors[2]),
        opacity = int(sum(colors)/opacitymodifier), #clustersize this
        sidelen = random.randrange(lowersizerange, uppersizerange)
      ))
  print(f'Generating {getTime()}')

  if sort == True:
    def opacity(point):
      return(point.opacity)
    points.sort(key = opacity)

  frames = []
  for frame in range(framecount):
    newimg = Image.new( mode = "RGB", size = (xsize, ysize) )
    draw = ImageDraw.Draw(newimg, 'RGBA')
    for i in points:
    #print(i.indeces[1], i.indeces[3])
    #print(i.r, i.g, i.b)
      draw.ellipse([i.indeces[3], i.indeces[1]], fill = (i.r, i.g, i.b, i.opacity))
      i.updatePos(1)
      i.resetPos(i.sidelen, xsize, ysize)
      i.updateSquare()
    frames.append(newimg)
  
  print(f'Saving {getTime()}')
  
  frames[0].save('this may be splendid.gif', save_all = True, append_images = frames[1:], duration = 50, loop = 0)
  print(f'Finished {getTime()}')
  return('this may be splendid.gif')



#bokehmoving('loudy cloudy.jpg', framecount = 100)

#bokeh('city2.jpg', clustersize = 3, density = 16, opacitymodifier = 9, uppersizerange=100, sort = True)




#https://stackoverflow.com/questions/2275446/python-animation-with-pil
  
    
