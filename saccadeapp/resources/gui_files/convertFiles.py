# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import glob as gl
import platform as pt


# =============================================================================
# Utility
# =============================================================================
def convertFiles(inputPath, outputPath):
    this_os = pt.system()
    if this_os is 'Windows':
        dilim = u'\\'
    else:
        dilim = u'/'

    inputs = gl.glob(inputPath + dilim + u'*.ui')

    for item in inputs:
        idxFld = len(inputPath)
        idxExt = item.find(u'.ui')
        outAux = outputPath + item[idxFld:idxExt] + u'.py'

        bash = u'pyuic4 -o %s %s' % tuple([outAux, item])
        print bash
        os.system(bash)


# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':
    convertFiles(u'ui_files', u'py_files')
