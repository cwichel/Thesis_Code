# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import glob as gl
from PyQt4 import QtGui, QtCore, uic


# =============================================================================
# View Models
# =============================================================================
# =============================================== List-like
class ListModel(QtCore.QAbstractListModel):
    def __init__(self, data=[], header=u'Empty', parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        # ==============
        self.listData = data
        self.listHead = header
        self.listTool = header + ': '

    # ================================= Item Flags
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # ================================= Data Presentation
    def data(self, index, role=None):                           # Element View
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            return self.listTool + self.listData[row]
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.listData[row]
            return value

    def headerData(self, section, orientation, role=None):      # Header
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString(self.listHead)

    # ================================= Data Size
    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.listData)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    # ================================= Data Handler
    def setData(self, index, value, role=QtCore.Qt.EditRole):                                   # Edit
        if role == QtCore.Qt.EditRole:
            row = index.row()
            value = QtCore.QString(value)
            if not value.isEmpty():
                self.listData[row] = unicode(value)
                self.dataChanged.emit(index, index)
                return True
        return False

    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):         # Insert new row
        self.beginInsertRows(parent, position, position+rows-1)
        for row in range(rows):
            defaultValue = u'Empty'
            self.listData.insert(position, defaultValue)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):         # Remove a row
        self.beginRemoveRows(parent, position, position+rows-1)
        for row in range(rows):
            value = self.listData[position]
            self.listData.remove(value)
        self.endRemoveRows()
        return True

    # ================================= Extras
    def setDataFromPath(self, path):
        try:
            filePath = gl.glob(path)
            fileList = [unicode(os.path.splitext(os.path.basename(itm))[0]) for itm in filePath]
            self.listData = fileList
            return True
        except:
            return False

    def addNewValue(self, value):
        try:
            self.insertRows(0, 1)
            self.listData[0] = unicode(QtCore.QString(value))
            self.listData = sorted(self.listData)
            self.reset()
            return True
        except:
            return False

    def removeValue(self, value):
        try:
            value = QtCore.QString(value)
            if value in self.listData:
                index = self.listData.index(unicode(value))
                self.removeRows(index, 1)
            self.reset()
            return True
        except:
            return False

    def getItemById(self, index):
        if 0 <= index < self.rowCount():
            return self.listData[index]
        else:
            return None

    def getIdByItem(self, value):
        try:
            return self.listData.index(unicode(value))
        except:
            return -1


# =============================================== Table-like
class tableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[]], headers=[u'Empty1', u'Empty2'], parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        # ==============
        if data is [[]]:
            self.tableData = data
        else:
            self.tableData = data
        # ==============
        self.tableHead = headers[0:2]
        self.tableTool = [headers[0] + ': ', headers[1] + ': ']
        self.defaultValue = u'Empty'

    # ================================= Item Flags
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # ================================= Data Presentation
    def data(self, index, role=None):                           # Element View
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            col = index.column()
            if col < len(self.tableTool):
                return QtCore.QString(self.tableTool[col]) + str(self.tableData[row][col])
            else:
                return QtCore.QString(u'Not implemented ') + str(self.tableData[row][col])
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.tableData[row][col]
            return value

    def headerData(self, section, orientation, role=None):      # Header
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.tableHead):
                    return QtCore.QString(self.tableHead[section])
                else:
                    return QtCore.QString(u'Not implemented')

    # ================================= Data Size
    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.tableData)

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    # ================================= Data Handler
    def setData(self, index, value, role=QtCore.Qt.EditRole):                                   # Edit
        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            if not value.isEmpty():
                self.tableData[row][col] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):         # Insert new row
        self.beginInsertRows(parent, position, position+rows-1)
        for row in range(rows):
            defaultValues = [self.defaultValue for col in range(self.columnCount())]
            self.tableData.insert(position, defaultValues)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):         # Remove a row
        self.beginRemoveRows(parent, position, position+rows-1)
        for row in range(rows):
            value = self.tableData[position]
            self.tableData.remove(value)
        self.endRemoveRows()
        return True

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex(), *args, **kwargs):   # Insert new column
        self.beginInsertColumns(parent, position, position + columns - 1)
        for col in range(columns):
            for row in range(self.rowCount()):
                self.tableData[row].insert(position, self.defaultValue)
        self.endInsertColumns()
        return True

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex(), *args, **kwargs):   # Remove a column
        self.beginRemoveColumns(parent, position, position + columns - 1)
        for col in range(columns):
            for row in range(self.rowCount()):
                value = self.tableData[row][col]
                self.tableData[row].remove(value)
        self.endRemoveColumns()
        return True

    # ================================= Extras
    def changeData(self, data):
        if data != [] and len(data[0]) is self.columnCount():
            self.tableData = data
            self.reset()
            return True
        else:
            return False

    def changeValue(self, rowIdx, value=[]):
        try:
            if 0 <= rowIdx < self.rowCount():
                self.tableData[rowIdx] = value
                self.reset()
                return True
            else:
                return False
        except:
            return False

    def addNewValue(self, value=[]):
        try:
            self.insertRows(self.rowCount(), 1)
            self.tableData[self.rowCount()-1] = value
            self.reset()
            return True
        except:
            return False

    def removeValue(self, value=[]):
        try:
            if value in self.tableData:
                index = self.tableData.index(value)
                self.removeRows(index, 1)
                self.reset()
            return True
        except:
            return False

    def getItemById(self, rowIdx):
        if 0 <= rowIdx < self.rowCount():
            return self.tableData[rowIdx]
        else:
            return None

    def getIdByItem(self, value=[]):
        try:
            return self.tableData.index(value)
        except:
            return -1

    def rotateItem(self, rowIdxItem1, rowIdxItem2):
        dataCount = self.rowCount()-1
        if 0 <= rowIdxItem1 <= dataCount and 0 <= rowIdxItem2 <= dataCount:
            auxItem = self.tableData[rowIdxItem1]
            self.tableData[rowIdxItem1] = self.tableData[rowIdxItem2]
            self.tableData[rowIdxItem2] = auxItem
            self.reset()
            return True
        else:
            return False
