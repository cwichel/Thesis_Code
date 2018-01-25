# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import platform as pt
from PyQt4 import QtGui
import ConfigParser as cp

# =============================================================================
# ID Definitions
# =============================================================================
TEST_TYPE = u'.tst'
EXPS_TYPE = u'.exp'
# =================
NOT_VALID_CHARS = [u'', u'.', u'..']


# =============================================================================
# Config Files Handler
# =============================================================================
class confHandler(cp.ConfigParser):
    def __init__(self):
        cp.ConfigParser.__init__(self)

    # ================================= File Handler
    def openConf(self, fileName):
        fileName = unicode(fileName)
        if os.path.isfile(fileName):
            fileItem = open(fileName)
            self.readfp(fileItem)
            fileItem.close()
            return True
        else:
            return False

    def saveConf(self, fileName, isRW=True):
        fileName = unicode(fileName)
        isFile = os.path.isfile(fileName)
        if not isFile or (isFile and isRW):
            fileItem = open(fileName, 'w')
            self.write(fileItem)
            fileItem.close()
            return True
        else:
            return False

    # ================================= Data Handler
    def getSections(self):
        sections = self.sections()
        if sections:
            return sections
        else:
            return []

    def getValue(self, section, option, mode=None):
        if mode is int:
            return self.getint(section, option)
        elif mode is float:
            return self.getfloat(section, option)
        elif mode is bool:
            return self.getboolean(section, option)
        else:
            return self.get(section, option)

    def setValue(self, section, option, value):
        try:
            sections = self.getSections()
            if section in sections:
                self.set(section, option, value)
            else:
                self.add_section(section)
                self.set(section, option, value)
            return True
        except:
            return False

    # ================================= Children
    def getConf(self, fileName=u''):
        pass

    def putConf(self, fileName=u''):
        pass


# =============================================================================
# Config File Class
# =============================================================================
class confFile(confHandler):
    def __init__(self):
        confHandler.__init__(self)
        # ==============
        self.fileName = u'./saccadeApp.ini'
        # ==============
        if pt.system() is 'Windows':
            self.secConf = u'ConfigWindows'
        else:
            self.secConf = u'ConfigUnix'
        # ==============
        self.testDir = u''
        self.expsDir = u''
        # ==============
        self.getConfig()

    # =================================
    def getConfig(self, filename=u''):
        # ==============
        if self.openConf(fileName=self.fileName) and self.secConf in self.getSections():
            self.testDir = self.getValue(self.secConf, u'testDir', mode=str)
            self.expsDir = self.getValue(self.secConf, u'expsDir', mode=str)
        else:
            self.testDir = u'Tests/'
            self.expsDir = u'Experiments/'
            self.putConfig()
        # ==============
        if not os.path.isdir(self.testDir):
            os.mkdir(self.testDir)
        if not os.path.isdir(self.expsDir):
            os.mkdir(self.expsDir)

    def putConfig(self, filename=u''):
        self.setValue(self.secConf, u'testDir', self.testDir)
        self.setValue(self.secConf, u'expsDir', self.expsDir)
        # ==============
        self.saveConf(fileName=self.fileName, isRW=True)


# =============================================================================
# Test File Class
# =============================================================================
class testFileConf(confHandler):
    def __init__(self, fileName=u''):
        confHandler.__init__(self)
        # ==============
        self.fileName = fileName
        # ==============
        self.imagData = []
        self.extraFlag = False
        self.extraImag = u''
        self.extraKeys = []
        self.extraCAns = u''
        # ==============
        if self.fileName is not u'':
            self.getConf()

    # =================================
    def getConf(self, fileName=u''):
        # ==============
        if fileName is not u'':
            self.fileName = fileName
        # ==============
        if self.fileName is not u'' and self.openConf(fileName=self.fileName):
            self.imagData = self.getImagData()
            self.extraFlag = self.getValue(u'finalSel', u'extraFlag', mode=bool)
            self.extraImag = self.getValue(u'finalSel', u'extraImag', mode=str)
            self.extraKeys = self.getExtraKeys()
            self.extraCAns = self.getValue(u'finalSel', u'extraCAns', mode=str)
            return True
        else:
            return False

    def putConf(self, fileName=u''):
        # ==============
        if fileName is not u'':
            self.fileName = fileName
        # ==============
        self.setValue(u'mainTest', u'imagData', self.setImagData())
        self.setValue(u'finalSel', u'extraFlag', self.extraFlag)
        self.setValue(u'finalSel', u'extraImag', self.extraImag)
        self.setValue(u'finalSel', u'extraKeys', self.setExtraKeys())
        self.setValue(u'finalSel', u'extraCAns', self.extraCAns)
        # ==============
        return self.saveConf(fileName=self.fileName, isRW=True)

    # =================================
    def setImagData(self):
        if self.imagData:
            auxStr = u''
            for line in self.imagData:
                auxStr += u'\n%s\t%s' % tuple([line[0], line[1]])
            return auxStr
        else:
            return u''

    def setExtraKeys(self):
        if self.extraKeys:
            auxStr = u''
            for key in self.extraKeys:
                auxStr += u'%s;' % key
            return auxStr
        else:
            return u''

    # =================================
    def getImagData(self):
        auxStr = self.getValue(u'mainTest', u'imagData', mode=str)
        if auxStr is not u'':
            auxOut = []
            auxArr = auxStr.split(u'\n')
            for line in auxArr:
                try:
                    auxLne = line.split(u'\t')
                    auxOut.append([auxLne[0], float(auxLne[1])])
                except:
                    pass
            return auxOut
        else:
            return []

    def getExtraKeys(self):
        auxStr = self.getValue(u'finalSel', u'extraKeys', mode=str)
        if auxStr is not u'':
            auxOut = []
            auxArr = auxStr.split(u';')
            for line in auxArr:
                if line is not u'':
                    auxOut.append(line)
            return auxOut
        else:
            return []


# =============================================================================
# Experiment File Class
# =============================================================================
class expsFileConf(confHandler):
    def __init__(self, fileName=u''):
        confHandler.__init__(self)
        # ==============
        self.fileName = fileName
        # ==============
        self.testData = []
        self.randFlag = False
        self.restFlag = False
        self.restTest = 0
        self.restTime = 0.0
        # ==============
        if self.fileName is not u'':
            self.getConf()

    # =================================
    def getConf(self, fileName=u''):
        # ==============
        if fileName is not u'':
            self.fileName = fileName
        # ==============
        if self.fileName is not u'' and self.openConf(fileName=self.fileName):
            self.testData = self.getTestData()
            self.randFlag = self.getValue(u'testSort', u'randFlag', mode=bool)
            self.restFlag = self.getValue(u'testRest', u'restFlag', mode=bool)
            self.restTest = self.getValue(u'testRest', u'restTest', mode=int)
            self.restTime = self.getValue(u'testRest', u'restTime', mode=float)
            return True
        else:
            return False

    def putConf(self, fileName=u''):
        # ==============
        if fileName is not u'':
            self.fileName = fileName
        # ==============
        self.setValue(u'mainExps', u'testData', self.setTestData())
        self.setValue(u'testSort', u'randFlag', self.randFlag)
        self.setValue(u'testRest', u'restFlag', self.restFlag)
        self.setValue(u'testRest', u'restTest', self.restTest)
        self.setValue(u'testRest', u'restTime', self.restTime)
        # ==============
        return self.saveConf(fileName=self.fileName, isRW=True)

    # =================================
    def setTestData(self):
        if self.testData:
            auxStr = u''
            for line in self.testData:
                auxStr += u'\n%s\t%s' % tuple([line[0], line[1]])
            return auxStr
        else:
            return u''

    # =================================
    def getTestData(self):
        auxStr = self.getValue(u'mainExps', u'testData', mode=str)
        if auxStr is not u'':
            auxOut = []
            auxArr = auxStr.split(u'\n')
            for line in auxArr:
                try:
                    auxLne = line.split(u'\t')
                    auxOut.append([auxLne[0], float(auxLne[1])])
                except:
                    pass
            return auxOut
        else:
            return []


# =============================================================================
# Experiment File Class
# =============================================================================
def getFilePath(path, ext, newName=u'', oldName=u'', isRW=False):
    newName = unicode(newName) if newName is not None else u''
    oldName = unicode(oldName) if oldName is not None else u''
    auxName = oldName
    newPath = None
    # ==============
    isFirst = True
    isReady = False
    # ==============
    while not isReady:
        if isFirst and newName != u'':
            isFirst = False
            isOk = True
        else:
            isFirst = False
            newName, isOk = QtGui.QInputDialog.getText(None, u'New file name', u'Insert new file name:', text=auxName)
            newName = unicode(newName)
        # ==============
        if isOk:
            newPath = unicode(path + u'/' + newName + ext)
            isNewPathOk, isNewPathExist = isPathAvailable(newPath)
            # ==============
            if isNewPathOk and newName not in NOT_VALID_CHARS and len(newName) >= 4:
                if isRW and isNewPathExist and newName != oldName:
                    print u'Error: This file name affects not-involved files.'
                    QtGui.QMessageBox.about(None, u'Error!', u'This file name affects\nnot-involved files')
                elif not isRW and isNewPathExist:
                    print u'Error: Cannot copy to a existing file.'
                    QtGui.QMessageBox.about(None, u'Error!', u'Cannot copy to a existing file')
                else:
                    isReady = True
            else:
                if len(newName) < 4:
                    print u'Error: file name too short'
                    QtGui.QMessageBox.about(None, u'Error!', u'Please use a name larger\nthan 4 letters.')
                else:
                    print u'Error: Bad file name'
                    QtGui.QMessageBox.about(None, u'Error!', u'Bad file name')
            # ==============
            auxName = newName
        else:
            print u'Operation cancelled.'
            newName = None
            newPath = None
            isReady = True
    # ==============
    return newName, newPath


def isPathAvailable(path):
    # Return: [nameOk, exists]
    if not os.path.isfile(path):
        try:
            auxFile = open(path, 'w')
            auxFile.close()
            os.remove(path)
            return True, False
        except:
            return False, False
    else:
        return True, True
    pass
