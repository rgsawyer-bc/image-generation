from PIL import ImageDraw

class CircleHSV:
    def __init__(self, x: int | float, y: int | float, r: int | float, color: list[int], opacity: int) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.color = color

        


def add(draw: ImageDraw.Draw, point: CircleHSV):
    x, y = point.x, point.y
    r = point.r
    color = point.color
    draw.ellipse(
        [(x - r, y - r), (x + r, y + r)], fill = (c, saturation, value)
        )