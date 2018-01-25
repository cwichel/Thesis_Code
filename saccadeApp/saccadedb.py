# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import sqlite3 as lite


# =============================================================================
# Class
# =============================================================================
class saccadedb:
    # ================================= Primary Constructor
    def __init__(self, filepath=u'saccadedb.sqlite3'):
        self._conn = None
        self._dbfile = filepath
        self._sqlscript = os.path.split(os.path.realpath(__file__))[0] + u'/resources/saccadedb_sqlite.sql'
        # =========
        self.connect()

    # ================================= Connection methods
    def connect(self):
        print u"Connecting to DB... "
        if os.path.isfile(self._dbfile):
            self._conn = lite.connect(self._dbfile)
            print u'Connected!'
        else:
            sqlcommand = open(self._sqlscript, u'r').read()
            self._conn = lite.connect(self._dbfile)
            self._conn.executescript(sqlcommand)
            print u"Database not found. A new one was created."

    def close(self):
        try:
            self._conn.close()
            print u"Disconnected!"
            return True
        except lite.Error, event:
            print u"Error: %s" % event.args[0]
            return False

    # ================================= Query methods
    def push_query(self, query=None):       # insert, update, delete
        if query is not None:
            try:
                cursor = self._conn.cursor()
                cursor.execute(query)
                self._conn.commit()
                return True
            except lite.Error, event:
                if self._conn:
                    self._conn.rollback()
                print u"Error: %s" % event.args[0]
                return False
        else:
            u"Error: Query has <None> type"
            return False

    def pull_query(self, query=None):       # select
        if query is not None:
            try:
                cursor = self._conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
            except lite.Error, event:
                print u"Error: %s" % event.args[0]
                return None
        else:
            u"Error: Query has <None> type"
            return None
