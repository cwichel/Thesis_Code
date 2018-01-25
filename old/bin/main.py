# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import sys
from PyQt4 import QtGui
from lib.saccadeApp import mainWindow

# =============================================================================
# Main Loop
# =============================================================================
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    exe = mainWindow()
    exe.show()
    sys.exit(app.exec_())