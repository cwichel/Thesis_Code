# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import platform
import numpy as np
import sqlite3 as lite


# =============================================================================
# Class
# =============================================================================
class saccadedb:
    # ================================= Primary Constructor
    def __init__(self, filepath=u'saccadedb.sqlite3'):
        self.__conn = None
        self.__dbfile = filepath
        # =========
        iswin = any(platform.win32_ver())
        sqlpath = u'\\resources\\database\\' if iswin else u'/resources/database/'
        self.__sqlscript = os.path.split(os.path.realpath(__file__))[0] + sqlpath + u'saccadedb_sqlite.sql'
        # =========
        self.connect()

    # ================================= Connection methods
    def connect(self):
        print u"Connecting to DB... "
        if os.path.isfile(self.__dbfile):
            self.__conn = lite.connect(self.__dbfile)
            print u'Connected!'
        else:
            query = open(self.__sqlscript, u'r').read()
            self.__conn = lite.connect(self.__dbfile)
            self.__conn.executescript(query)
            print u"Database not found. A new one was created."

    def close(self):
        try:
            self.__conn.close()
            print u"Disconnected!"
            return True
        except lite.Error, event:
            print u"Error: %s" % event.args[0]
            return False

    # ================================= Query methods
    def push_query(self, query=None):       # insert, update, delete
        if query is not None:
            try:
                cursor = self.__conn.cursor()
                cursor.execute(query)
                self.__conn.commit()
                return True
            except lite.Error, event:
                if self.__conn:
                    self.__conn.rollback()
                print u"Error: %s" % event.args[0]
                return False
        else:
            u"Error: Query has <None> type"
            return False

    def pull_query(self, query=None):       # select
        if query is not None:
            try:
                cursor = self.__conn.cursor()
                cursor.execute(query)
                result = np.array(cursor.fetchall())
                if result.shape[0] > 0:
                    return result
                else:
                    return None
            except lite.Error, event:
                print u"Error: %s" % event.args[0]
                return None
        else:
            u"Error: Query has <None> type"
            return None