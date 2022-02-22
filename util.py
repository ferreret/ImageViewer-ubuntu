# --------------------------------------------------------------------------------------------------------------
import os
from typing import Union, Optional, Tuple, Any, List

from PySide6.QtGui import QImage
from PySide6.QtWidgets import QFileDialog


# ----------------------------------------------------------------------------------------------------------------------------
def loadImagesFromFile(parent, startupDir) -> List[str]:
    """ Load an image from file.
    Without any arguments, loadImageFromFile() will pop up a file dialog to choose the image file.
    With a fileName argument, loadImageFromFile(fileName) will attempt to load the specified image file directly.
    """
    # TODO Adaptar los filtros de imagen para todos los tipos que necesite
    fileNames, _ = QFileDialog.getOpenFileNames(parent, "Open image file.", dir=startupDir, filter="Image files (*.png "
                                                                                                   "*.jpg *.bmp *.tif)")
    # print(fileNames)

    return fileNames

    # if len(fileName) and os.path.isfile(fileName):
    #     image = QImage(fileName)
    #     name = os.path.basename(fileName)
    #     return image, name


