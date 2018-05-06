# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from PyQt4 import QtCore, QtGui


# =============================================================================
# Model: Color List
# color = array: [color_name, hex_value]
# =============================================================================
class ColorListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        # -------------------
        self.__colors = None
        # -------------------
        self.__get_colors()

    # =================================
    def columnCount(self, *args, **kwargs):
        return 1

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__colors)

    def data(self, index, role=None):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            return self.__colors[row][0]
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            return self.__get_color_icon(row)
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            return u"Hex code: " + unicode(self.__colors[row][1])

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString(u"Palette")
            else:
                return QtCore.QString(u"%1").arg(section)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # =================================
    def __get_colors(self):
        from saccadeapp.core import Utils
        # -------------------
        self.__colors = Utils.get_colors()

    def __get_color_icon(self, row):
        value = self.__colors[row][1]
        qitem = QtGui.QColor(value)
        pmap = QtGui.QPixmap(26, 26)
        pmap.fill(qitem)
        icon = QtGui.QIcon(pmap)
        return icon

    def get_item_by_id(self, index):
        if 0 <= index < self.rowCount():
            return self.__items[index]
        else:
            return None

    def get_id_by_item(self, item):
        try:
            return self.__items.index(item)
        except:
            return -1


# =============================================================================
# Model: List
# items: list: [item_value]
# =============================================================================
class ListModel(QtCore.QAbstractListModel):
    def __init__(self, items, parent=None, header=u"Empty"):
        QtCore.QAbstractListModel.__init__(self, parent)
        # -------------------
        self.__items = None
        self.__tooltip = header + u": "
        self.__header = header
        self.__has_items = False
        # -------------------
        self.update_items(items)

    # =================================
    def columnCount(self, *args, **kwargs):
        return 1

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__items) if self.__has_items else 0

    def data(self, index, role=None):
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            return self.__tooltip + unicode(self.__items[row])
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            return unicode(self.__items[row])

    def setData(self, index, value, role=None):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            value = QtCore.QString(value)
            if not value.isEmpty():
                self.__items[row] = unicode(value)
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString(self.__header)
            else:
                return QtCore.QString(u"%1").arg(section)

    def insertRows(self, position, rows, parent=None, *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            self.__items.insert(position, u"Empty")
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=None, *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            value = self.__items[position]
            self.__items.remove(value)
        self.endRemoveRows()
        return True

    def flags(self, index):
        if self.__has_items:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # =================================
    def update_items(self, items):
        if items is not []:
            self.__has_items = True
            self.__items = sorted(items, key=lambda v: v.upper())
        else:
            self.__has_items = False
            self.__items = None
        self.reset()

    def get_item_by_id(self, index):
        if 0 <= index < self.rowCount():
            return self.__items[index]
        else:
            return None

    def get_id_by_item(self, item):
        try:
            return self.__items.index(item)
        except:
            return -1

    def has_items(self):
        return self.__has_items

