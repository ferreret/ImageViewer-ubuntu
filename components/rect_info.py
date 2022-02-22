""" Clase que representa la información de un bloque. Rectángulo que lo representa y color."""
from PySide6.QtCore import QRectF


class RectInfo:
    # Constructor
    def __init__(self, name: str,  rect: QRectF, fill_color: tuple, border_color: tuple):
        self.name = name
        self.rect = rect
        self.fill_color = fill_color
        self.border_color = border_color
        