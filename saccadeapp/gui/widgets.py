# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from PyQt4 import QtCore, QtGui


# ===============================================
# Class: ImageLabel (with zoom popup)
# ===============================================
class ImageLabel(QtGui.QLabel):
    def __init__(self, parent):
        super(ImageLabel, self).__init__(parent=parent)
        self.__image = None
        self.__popup = None

    def set_image(self, image):
        from os import path
        from PIL import Image
        if image is None:
            return
        if isinstance(image, Image.Image):
            self.__image = image
        elif image != u"" and path.isfile(path=image):
            self.__image = Image.open(image)
        self.show_image()

    def remove_image(self):
        self.__image = None
        self.clear()
        self.setText(u"No image")

    def get_image(self):
        return self.__image

    def show_image(self):
        from PIL import ImageQt as IQt
        if self.__image is not None:
            image = IQt.ImageQt(self.__image).scaledToHeight(60)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.setPixmap(pixmap)

    def enterEvent(self, event):
        # Display zoomed image popup
        if self.__image is not None:
            self.__popup = ImagePopup(self)
            self.__popup.show()
            event.accept()


class ImagePopup(QtGui.QLabel):
    def __init__(self, parent):
        from PIL import ImageQt as IQt
        super(ImagePopup, self).__init__(parent)
        # Create a bigger pixmap
        image = IQt.ImageQt(parent.get_image()).scaledToHeight(300)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.setPixmap(pixmap)
        # Center the zoomed image
        thumb = parent.pixmap()
        position = self.cursor().pos()
        position.setX(position.x() - thumb.size().width())
        position.setY(position.y() - thumb.size().height())
        self.move(position)
        # Configure
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)

    def leaveEvent(self, *args, **kwargs):
        self.destroy()

