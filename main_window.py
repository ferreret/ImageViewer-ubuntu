import os.path

from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QAction, Qt, QActionGroup, QIcon, QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QToolBar, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QDockWidget, \
    QListWidget, QListView, QListWidgetItem

from functools import partial
import util

# TODO: Localización de los textos


# ----------------------------------------------------------------------------------------------------------------------
# Main Window
# Implementing designer funcionality
# ----------------------------------------------------------------------------------------------------------------------
from components.image_info import ImageInfo
from components.rect_info import RectInfo
from qtImageViewer import QtImageViewer


class MainWindow(QMainWindow):
    # Enums
    # ------------------------------------------------------------------------------------------------------------------
    FIRST_IMAGE, PREVIOUS_IMAGE, NEXT_IMAGE, LAST_IMAGE = range(4)

    # ------------------------------------------------------------------------------------------------------------------
    # Constructor
    def __init__(self):
        super().__init__()
        self.thumbnail_list = None
        self.viewer = None
        self.images = []
        self.setWindowTitle("Form Designer")
        self.setMinimumSize(1280, 1024)

        self.create_left_dock_panel()
        self.create_viewer()
        self.create_menubar()
        self.create_statusbar()

    # ------------------------------------------------------------------------------------------------------------------
    # Create menu bar
    def create_menubar(self):
        menu = self.menuBar()

        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        file_menu = menu.addMenu("File")
        edit_menu = menu.addMenu("Edit")

        # Add action to file menu
        open_file = QAction(QIcon(":/icons/open_icon"), "Open Image File", self)
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)
        file_menu.addAction(open_file)
        toolbar.addAction(open_file)

        # Add QActionGroup to edit menu
        viewer_mode_normal = QAction(QIcon(":/icons/normal_mode_icon"), "Normal mode", self)
        viewer_mode_normal.setCheckable(True)
        viewer_mode_normal.setChecked(True)
        viewer_mode_normal.triggered.connect(self.viewer.setViewerMode)

        viewer_mode_design = QAction(QIcon(":/icons/design_mode_icon"), "Design", self)
        viewer_mode_design.setCheckable(True)
        viewer_mode_design.triggered.connect(self.viewer.setDesignMode)

        toolbar.addSeparator()
        toolbar.addAction(viewer_mode_normal)
        toolbar.addAction(viewer_mode_design)

        edit_menu.addSeparator()
        edit_menu.addAction(viewer_mode_normal)
        viewer_mode_group = QActionGroup(self)
        viewer_mode_group.addAction(viewer_mode_normal)
        viewer_mode_group.addAction(viewer_mode_design)
        edit_menu.addAction(viewer_mode_normal)
        edit_menu.addAction(viewer_mode_design)
        edit_menu.addSeparator()

        delete_sel_items = QAction(QIcon(":/icons/delete_items_icon"), "Delete Selected Items", self)
        delete_sel_items.triggered.connect(self.viewer.deleteSelectedItems)
        edit_menu.addAction(delete_sel_items)

        toolbar.addSeparator()
        toolbar.addAction(delete_sel_items)

        self.addToolBar(toolbar)

    # ------------------------------------------------------------------------------------------------------------------
    # Create status bar
    def create_statusbar(self):
        self.statusBar().showMessage("Ready")

    # ------------------------------------------------------------------------------------------------------------------
    # Create viewer
    def create_viewer(self):
        layout = QVBoxLayout()
        # Configuración del visor
        self.viewer = QtImageViewer()
        self.viewer.keep_aspect_ratio = True
        self.viewer.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.viewer.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.viewer.canPan = True
        self.viewer.canZoom = True
        self.viewer.canRotate = True

        # Añado la signal de elemento creado
        self.viewer.rectCreated.connect(self.rect_created)

        layout.addWidget(self.viewer)
        widget = QWidget()
        widget.setLayout(layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(0)
        button_first = QPushButton("First")
        button_first.setIcon(QIcon(":/icons/navigation_first"))

        # noinspection PyUnresolvedReferences
        button_first.clicked.connect(partial(self.navigate_buttons, self.FIRST_IMAGE))
        button_previous = QPushButton("Previous")
        button_previous.setIcon(QIcon(":/icons/navigation_previous"))
        # noinspection PyUnresolvedReferences
        button_previous.clicked.connect(partial(self.navigate_buttons, self.PREVIOUS_IMAGE))
        button_next = QPushButton("Next")
        button_next.setIcon(QIcon(":/icons/navigation_next"))
        button_next.setLayoutDirection(Qt.RightToLeft)
        # noinspection PyUnresolvedReferences
        button_next.clicked.connect(partial(self.navigate_buttons, self.NEXT_IMAGE))
        button_last = QPushButton("Last")
        button_last.setIcon(QIcon(":/icons/navigation_last"))
        button_last.setLayoutDirection(Qt.RightToLeft)
        # noinspection PyUnresolvedReferences
        button_last.clicked.connect(partial(self.navigate_buttons, self.LAST_IMAGE))

        buttons_layout.addWidget(button_first)
        buttons_layout.addWidget(button_previous)
        buttons_layout.addWidget(button_next)
        buttons_layout.addWidget(button_last)
        buttons_layout.addStretch(0)

        layout.addLayout(buttons_layout)

        self.setCentralWidget(widget)

    # ------------------------------------------------------------------------------------------------------------------
    # Create left dock panel
    def create_left_dock_panel(self):
        dock_navigation = QDockWidget("Navigation", self)
        dock_navigation.setWindowTitle("Navigation")

        dock_navigation.setFeatures(QDockWidget.DockWidgetMovable |
                                    QDockWidget.DockWidgetFloatable)

        dock_navigation.setMinimumWidth(150)
        dock_navigation.setMinimumHeight(150)

        widget = QWidget()
        layout = QVBoxLayout()

        # Create navigation tree

        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setViewMode(QListView.IconMode)
        self.thumbnail_list.setIconSize(QSize(128, 128))
        self.thumbnail_list.setResizeMode(QListView.Adjust)
        self.thumbnail_list.setSizeAdjustPolicy(QListView.AdjustToContents)
        # self.thumbnail_list.setMovement(QListView.Static)
        self.thumbnail_list.setSpacing(10)
        # self.thumbnail_list.setWordWrap(True)
        # self.thumbnail_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.thumbnail_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.thumbnail_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # noinspection PyUnresolvedReferences
        self.thumbnail_list.currentRowChanged.connect(self.on_thumbnail_list_currentRowChanged)

        # thumbnail_list.customContextMenuRequested.connect(self.show_thumbnail_context_menu)

        layout.addWidget(self.thumbnail_list)

        widget.setLayout(layout)

        dock_navigation.setWidget(widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock_navigation)

    # ------------------------------------------------------------------------------------------------------------------
    # Add thumbnail to list
    def add_thumbnail_to_list(self, image: QImage):
        item = QListWidgetItem()
        item.setIcon(QIcon(QPixmap.fromImage(image)))
        item.setText(str(self.thumbnail_list.count()))
        self.thumbnail_list.addItem(item)

# ----------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Open image in designer
    def open_file(self):
        filenames = util.loadImagesFromFile(self, "sample_images")
        # image, name = util.loadImageFromFile(self, "sample_images")

        if filenames:
            if self.viewer.hasImage():
                self.viewer.deleteAllItems()
            for filename in filenames:
                if os.path.isfile(filename):
                    image = QImage(filename)

                    self.add_thumbnail_to_list(image)
                    self.images.append(ImageInfo(image))
            self.thumbnail_list.setCurrentRow(len(self.images) - 1)
            self.statusBar().showMessage(f"Loaded {len(filenames)} images")

        # if images is not None:
        #     if self.viewer.hasImage():
        #         self.viewer.deleteAllItems()
        #     self.statusBar().showMessage("Image loaded: " + name)
        #     self.add_thumbnail_to_list(image)
        #     self.images.append(ImageInfo(image))
        #     # Set selected item in thumbnail list
        #     self.thumbnail_list.setCurrentRow(len(self.images) - 1)

    # ------------------------------------------------------------------------------------------------------------------
    # Navigate to index image
    def navigate_buttons(self, navigation_button_index: int):
        if navigation_button_index == self.FIRST_IMAGE:
            self.thumbnail_list.setCurrentRow(0)
        elif navigation_button_index == self.PREVIOUS_IMAGE and self.thumbnail_list.currentRow() > 0:
            self.thumbnail_list.setCurrentRow(self.thumbnail_list.currentRow() - 1)
        elif navigation_button_index == self.NEXT_IMAGE \
                and self.thumbnail_list.currentRow() < self.thumbnail_list.count() - 1:
            self.thumbnail_list.setCurrentRow(self.thumbnail_list.currentRow() + 1)
        elif navigation_button_index == self.LAST_IMAGE:
            self.thumbnail_list.setCurrentRow(self.thumbnail_list.count() - 1)

    # ------------------------------------------------------------------------------------------------------------------
    # EVENTS
    # ------------------------------------------------------------------------------------------------------------------
    # event thumbnail_list selected item changed
    def on_thumbnail_list_currentRowChanged(self, current_row):
        if current_row >= 0:
            self.viewer.deleteAllItems()
            self.viewer.setImage(self.images[current_row].image)
            self.viewer.addRects(self.images[current_row].rects)

    # ------------------------------------------------------------------------------------------------------------------
    # Rect created in viewer event
    def rect_created(self, name: str, rect: QRect, fill_color: tuple, border_color: tuple):
        self.statusBar().showMessage("Rect created: " + name)
        self.images[self.thumbnail_list.currentRow()].add_rect(RectInfo(name, rect, fill_color, border_color))
