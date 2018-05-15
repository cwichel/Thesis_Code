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
    def columnCount(self, parent=None, *args, **kwargs):
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
        self.__colors = Utils.get_available_colors()

    def __get_color_icon(self, row):
        value = self.__colors[row][1]
        qitem = QtGui.QColor(value)
        pmap = QtGui.QPixmap(26, 26)
        pmap.fill(qitem)
        icon = QtGui.QIcon(pmap)
        return icon

    def get_item(self, index):
        if 0 <= index < self.rowCount():
            return self.__items[index]
        else:
            return None

    def get_index(self, item):
        try:
            return self.__items.index(item)
        except:
            return -1


# =============================================================================
# Model: List
# items: list: [item_value]
# =============================================================================
class ListModel(QtCore.QAbstractListModel):
    def __init__(self, items, header=u"Empty", parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        # -------------------
        self.__tooltip = header + u": "
        self.__header = header
        self.__list = []
        # -------------------
        self.update_items(items)

    # =================================
    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__list)

    def data(self, index, role=None):
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            return self.__tooltip + unicode(self.__list[row])
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            return unicode(self.__list[row])

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            value = QtCore.QString(value)
            if not value.isEmpty():
                self.__list[row] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString(self.__header)
            else:
                return QtCore.QString(u"%1").arg(section+1)

    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            self.__list.insert(position, u"Empty")
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            value = self.__items[position]
            self.__list.remove(value)
        self.endRemoveRows()
        return True

    def flags(self, index):
        if self.rowCount() > 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # =================================
    def update_items(self, items):
        if len(items) > 0:
            self.__list = sorted(items, key=lambda v: v.upper())
        else:
            self.__list = []
        self.reset()

    def get_item(self, index):
        if 0 <= index < self.rowCount():
            return self.__list[index]
        else:
            return None

    def get_index(self, row):
        try:
            return self.__list.index(row)
        except:
            return -1


# =============================================================================
# Model: Array
# items: list: [[item_value1, item_value2]]
# =============================================================================
class ArrayModel(QtCore.QAbstractTableModel):
    def __init__(self, items, header, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        # -------------------
        self.__tooltip = [item + u": " for item in header]
        self.__header = header
        self.__array = [[]]
        self.__cols = len(header)
        # -------------------
        self.update_items(items)

    # =================================
    def columnCount(self, parent=None, *args, **kwargs):
        return self.__cols

    def rowCount(self, parent=None, *args, **kwargs):
        return sum(1 for item in self.__array if isinstance(item, list))

    def data(self, index, role=None):
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            col = index.column()
            return self.__tooltip[col] + unicode(self.__array[row][col]) if col < self.__cols else u"Not implemented"
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return unicode(self.__array[row][col])

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            value = QtCore.QString(value)
            if not value.isEmpty():
                self.__array[row][col] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString(self.__header[section]) if section < self.__cols else u"Not implemented"
            else:
                return QtCore.QString(u"%1").arg(section+1)

    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            empty_value = [u"Empty" for col in range(self.__cols)]
            self.__array.insert(position, empty_value)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            value = self.__array[position]
            self.__array.remove(value)
        self.endRemoveRows()
        return True

    def insertColumns(self, position, cols, parent=QtCore.QModelIndex(), *args, **kwargs):   # Insert new column
        self.beginInsertColumns(parent, position, position + cols - 1)
        for col in range(cols):
            for row in range(self.rowCount()):
                self.__array[row].insert(position, u"Empty")
        self.endInsertColumns()
        return True

    def removeColumns(self, position, cols, parent=QtCore.QModelIndex(), *args, **kwargs):   # Remove a column
        self.beginRemoveColumns(parent, position, position + cols - 1)
        for col in range(cols):
            for row in range(self.rowCount()):
                value = self.__array[row][col]
                self.__array[row].remove(value)
        self.endRemoveColumns()
        return True

    def flags(self, index):
        if self.rowCount() > 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # =================================
    def update_items(self, items):
        items_sum = sum(1 for item in items if isinstance(item, list))
        if items_sum > 0:
            self.__array = sorted(items, key=lambda v: v.upper())
        self.reset()

    def get_item(self, index):
        if 0 <= index < self.rowCount():
            return self.__array[index]
        else:
            return None

    def get_index(self, row):
        try:
            return self.__array.index(row)
        except:
            return -1


# =============================================================================
# Model: Tree
# items: TreeNode
# =============================================================================
class TreeNode(object):
    def __init__(self, mask, value, parent=None):
        self.__mask = mask
        self.__value = value
        self.__childs = []
        self.__parent = None
        # -------------------
        self.set_parent(parent)
        if self.__parent is not None:
            parent.append_child(self)

    def __repr__(self):
        return self.get_log()

    # =================================
    def set_mask(self, mask):
        self.__mask = mask

    def get_mask(self):
        return self.__mask

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def set_parent(self, parent):
        if isinstance(parent, TreeNode) or parent is None:
            self.__parent = parent

    def get_parent(self):
        return self.__parent

    def append_child(self, child):
        if isinstance(child, TreeNode):
            child.set_parent(self)
            self.__childs.append(child)

    def insert_child(self, index, child):
        if isinstance(child, TreeNode) and 0 <= index <= self.get_child_count():
            child.set_parent(self)
            self.__childs.insert(index, child)
            return True
        return False

    def remove_child(self, index):
        if 0 <= index < self.get_child_count():
            child = self.__childs.pop(index)
            child.set_parent(None)
            del child
            return True
        return False

    def get_child_count(self):
        return len(self.__childs)

    def get_child(self, index):
        if 0 <= index < self.get_child_count():
            return self.__childs[index]
        return None

    def get_index(self, child):
        try:
            return self.__childs.index(child)
        except:
            return None

    def get_parent_index(self):
        if self.__parent is not None:
            return self.__parent.get_index(self)

    def get_log(self, base_tab=-1):
        output = u""
        base_tab += 1
        for tab in range(base_tab):
            output += u"\t"
        output += self.__mask+u"\n"
        for child in self.__childs:
            output += child.get_log(base_tab)
        base_tab -= 1
        return output


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, items, header, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        # -------------------
        self.__root_node = None
        self.__header = header
        # -------------------
        self.update_items(items)

    # =================================
    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        parent_node = self.get_node(parent)
        return parent_node.get_child_count() if parent_node is not None else 0

    def data(self, index, role=None):
        if not index.isValid():
            return None
        this_node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return unicode(this_node.get_mask())

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False
        if role == QtCore.Qt.EditRole:
            this_node = self.get_node(index)
            this_node.set_mask(value)
            return True

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return self.__header

    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        success = False
        parent_node = self.get_node(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            new_child = TreeNode(u"untitled" + unicode(str(row)), u"Empty")
            success = parent_node.insert_child(position, new_child)
        self.endInsertRows()
        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        success = False
        parent_node = self.get_node(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parent_node.remove_child(position)
        self.endRemoveRows()
        return success

    def flags(self, index):
        this_node = self.get_node(index)
        if this_node is not self.__root_node and this_node.get_parent() is not self.__root_node:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEnabled

    def index(self, row, col, parent=None, *args, **kwargs):
        parent_node = self.get_node(parent)
        child_node = parent_node.get_child(row)
        if child_node:
            return self.createIndex(row, col, child_node)
        return QtCore.QModelIndex()

    def parent(self, index=None):
        this_node = self.get_node(index)
        parent_node = this_node.get_parent()
        if parent_node == self.__root_node:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.get_parent_index(), 0, parent_node)

    # =================================
    def get_node(self, index=QtCore.QModelIndex()):
        if index.isValid():
            this_node = index.internalPointer()
            if this_node:
                return this_node
        return self.__root_node

    # =================================
    def update_items(self, node):
        if isinstance(node, TreeNode):
            self.__root_node = node
        self.reset()

    def get_index(self, node):
        if not isinstance(node, TreeNode) or node == self.__root_node:
            return QtCore.QModelIndex()
        return self.createIndex(node.get_parent_index(), 0, node)
