""" Clase donde guardo la información de la imagen y los rectángulos de la misma. """
from components.rect_info import RectInfo


class ImageInfo:
    def __init__(self, image):
        self.image = image
        self.rects = []

    def add_rect(self, rect: RectInfo):
        self.rects.append(rect)
