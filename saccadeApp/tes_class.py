# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import numpy as np
from psychopy import visual, colors
from saccadedb import saccadedb as sdb


# =============================================================================
# Classes
# =============================================================================
class Test:
    # ================================= Primary Constructor
    def __init__(self, db=sdb):
        self.__database = db
        # ========= Test info on DB
        self.__tes_code = None
        self.__tes_title = None
        self.__tes_version = None
        self.__tes_description = None
        # ========= Test frames
        self.__fra_time = []
        self.__fra_task = None

    # ================================= DB
    def is_code(self, code=None):
        if code is not None:
            query = u"select count(tes_code) from test where tes_code='%s'" % code
            res = np.asarray(self.__database.pull_query(query))
            return False if res[0] == 0 else True
        else:
            print u"Error: Code has <None> type"
            return True

    def is_base(self, title=None, version=None):
        if title is not None and version is not None:
            query = u"select count(tes_code) from test where tes_title='%s' and tes_version='%s'" % tuple([title, version])
            res = np.asarray(self.__database.pull_query(query))
            return False if res[0] == 0 else True
        else:
            print u"Error: title and version has to be different to <None> type"
            return True

    # ================================= Basic methods
    def set_database(self, db=sdb):
        if db.__class__ == sdb.__class__:
            self.__database = db
        else:
            print u"Error: db has to be instance of class <saccadedb>"

    def set_code(self, code):
        if not self.is_code(code=code):
            self.__tes_code = unicode(code)

    def set_info(self, title, version):
        if not self.is_base(title=title, version=version):
            self.__tes_title = unicode(title)
            self.__tes_version = unicode(version)

    def set_description(self, description):
        if description is not None:
            self.__tes_description = unicode(description)
        else:
            print u"Error: description has to be different to <None> type"

    def get_database(self):
        return self.__database

    def get_code(self):
        return self.__tes_code

    def get_title(self):
        return self.__tes_title

    def get_version(self):
        return self.__tes_version

    def get_description(self):
        return self.__tes_description

    # ================================= Basic methods


