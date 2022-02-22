import ctypes
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from main_window import MainWindow

# noinspection PyUnresolvedReferences
import resources

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon(':/icons/app_icon'))

    # Código para cambiar el icono de la aplicación en la barra de tareas
    my_app_id = "designer"
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
