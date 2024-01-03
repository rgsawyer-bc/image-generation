from math import floor, sin, cos, radians, sqrt

class Point:
  def __init__(self, x, y, velx = 0, vely = 0, accx = 0, accy = 0, color = (255, 255, 255), opacity = 255, rot = 0, velrot = 0, accrot = 0, type = None, sidelen = -1):
    self.x = x
    self.y = y
    self.velx = velx
    self.vely = vely
    self.accx = accx
    self.accy = accy
    self.r = int(color[0])
    self.g = int(color[1])
    self.b = int(color[2])
    self.opacity = opacity
    self.rot = radians(rot - 45)
    self.velrot = radians(velrot)
    self.accrot = radians(accrot)
    self.sidelen = sidelen
    self.type = type
    if self.type == 'square':
      self.dist = sqrt(2 * ((sidelen/2) ** 2))
      self.indeces = (
        (self.dist * cos(self.rot) + self.x, self.dist * sin(self.rot) + self.y),
        (-self.dist * sin(self.rot) + self.x, self.dist * cos(self.rot) + self.y),
        (-self.dist * cos(self.rot) + self.x, -self.dist * sin(self.rot) + self.y),
        (self.dist * sin(self.rot) + self.x, -self.dist * cos(self.rot) + self.y)
      )

  def updatePos(self, t, airresist = False, k = 0):
    if airresist == True:
      self.accx = -k * self.velx
      self.accy = -k * self.vely
    self.x = self.x + self.velx * t
    self.y = self.y + self.vely * t
    self.velx = self.velx + self.accx * t
    self.vely = self.vely + self.accy * t

  def updateRot(self, t, airresist = False, k = 0):
    if airresist == True:
      self.accrot = -k * self.velrot
    self.rot = self.rot + self.velrot * t
    self.velrot = self.velrot + self.accrot * t

  def updateSquare(self):
    self.indeces = (
        (self.dist * cos(self.rot) + self.x, self.dist * sin(self.rot) + self.y),
        (-self.dist * sin(self.rot) + self.x, self.dist * cos(self.rot) + self.y),
        (-self.dist * cos(self.rot) + self.x, -self.dist * sin(self.rot) + self.y),
        (self.dist * sin(self.rot) + self.x, -self.dist * cos(self.rot) + self.y)
      )

  def resetPos(self, outermargin, width, height):
    self.x = (
      self.x - 
      floor(
        (self.x+outermargin)/(width + 2*outermargin)
      ) * (width + 2*outermargin)
    )

    self.y = (
      self.y - 
      floor(
        (self.y+outermargin)/(height + 2*outermargin)
      ) * (height + 2*outermargin)
    )
    
  def __str__(self):
    return(f'Pos: ({self.x}, {self.y})\nVel: ({self.velx}, {self.vely})\nAcc: ({self.accx}, {self.accy})')

class Circle:
  def __init__(self, x, y, velx, vely, accx, accy, radius, color = (255, 255, 255), opacity = 255):
    self.x = x
    self.y = y
    self.velx = velx
    self.vely = vely
    self.accx = accx
    self.accy = accy
    self.r = color[0]
    self.g = color[1]
    self.b = color[2]
    self.opacity = opacity
    self.radius = radius
