# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import numpy as np
import sqlite3 as lite
from .utils import get_module_path, format_path


# =============================================================================
# Class: SaccadeDB
# =============================================================================
class SaccadeDB(object):
    # =================================
    def __init__(self, path=u""):
        self.__db_script = format_path(get_module_path()+u"/app/resources/database/saccadedb_sqlite.sql")
        self.__db_file = u"saccadedb.sqlite3" if path == u"" else path
        self.__db_connection = None
        self.connect()

    # =================================
    def connect(self):
        from os import path
        if path.isfile(self.__db_file):
            self.__db_connection = lite.connect(self.__db_file)
            self.__db_connection.executescript(u"pragma recursive_triggers=1; pragma foreign_keys=1;")
            print u"Connected!"
        else:
            sql = open(self.__db_script, u'r').read()
            self.__db_connection = lite.connect(self.__db_file)
            self.__db_connection.executescript(sql)
            print u"Database not found. A new one was created."

    def close(self):
        try:
            self.__db_connection.close()
            return True
        except lite.Error as error:
            print u"Error: %s" % error.message
            return False

    # =================================
    def push_query(self, query):       # insert, update, delete
        try:
            self.__db_connection.executescript(query)
            self.__db_connection.commit()
            return True
        except lite.Error as error:
            print u"Error: %s" % error.message
            if self.__db_connection:
                self.__db_connection.rollback()
            return False

    def pull_query(self, query):       # select
        try:
            cursor = self.__db_connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            result = np.array(result)
            if result.shape[0] > 0:
                return result
            else:
                return None
        except lite.Error as error:
            print u"Error: %s" % error.message
            return None
