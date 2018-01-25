# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from lib import *


# =============================================================================
# Main Loop
# =============================================================================
if __name__ == '__main__':
    # app = QtGui.QApplication(sys.argv)
    # exe = mainWindow()
    # exe.show()
    # sys.exit(app.exec_())
    test = saccadedb()

    #test.push_query(u"insert into test (tes_code, tes_title, tes_version) values ('1235', 'test1', 'v1.1')")
    res = test.pull_query(u"select * from test where tes_code='1234'")

    print res[0, 2]

    test.close()
