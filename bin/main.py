# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import sys
from PyQt4 import QtGui
from saccadeapp import SaccadeApp

# =============================================================================
# Main: Use example
# =============================================================================
if __name__ == u"__main__":
    app = QtGui.QApplication(sys.argv)
    exe = SaccadeApp()
    exe.show()
    sys.exit(app.exec_())
