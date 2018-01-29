# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import platform
import numpy as np
import sqlite3 as lite
from datetime import datetime, timedelta, tzinfo


# =============================================================================
# Data Base Class
# =============================================================================
class saccadedb(object):
    # ================================= Primary Constructor
    def __init__(self, filepath=u'saccadedb.sqlite3'):
        self.__conn = None
        self.__dbfile = filepath
        self.__script = self._get_script_path()
        # -------------------
        self.connect()

    # ================================= Connection methods
    def connect(self):
        print u"Connecting to DB... "
        if os.path.isfile(self.__dbfile):
            self.__conn = lite.connect(self.__dbfile)
            print u'Connected!'
        else:
            sql = open(self.__script, u'r').read()
            self.__conn = lite.connect(self.__dbfile)
            self.__conn.executescript(sql)
            print u"Database not found. A new one was created."

    def close(self):
        try:
            self.__conn.close()
            print u"Disconnected!"
            return True
        except lite.Error, event:
            print u"Error: %s" % event.args[0]
            return False

    @staticmethod
    def _get_script_path():
        is_win = any(platform.win32_ver())
        os_dir = u'\\resources\\database\\' if is_win else u'/resources/database/'
        return os.path.split(os.path.realpath(__file__))[0] + os_dir + u'saccadedb_sqlite.sql'

    # ================================= Query methods
    def push_query(self, query):       # insert, update, delete
        try:
            self.__conn.executescript(query)
            self.__conn.commit()
            return True
        except lite.Error, event:
            if self.__conn:
                self.__conn.rollback()
            print u"Error: %s" % event.args[0]
            return False

    def pull_query(self, query):       # select
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            result = np.array(result)
            if result.shape[0] > 0:
                return result
            else:
                return None
        except lite.Error, event:
            print u"Error: %s" % event.args[0]
            return None

    # ================================= Get multiple queries
    def __get_queries(self, query):
        try:
            return query.split(u';')
        except:
            return query


# =============================================================================
# Time Adjust Class
# =============================================================================
class time_clt(tzinfo):
    def dst(self, dt):
        start = datetime(year=dt.year, month=4, day=12)     # inicio horario invierno
        end = datetime(year=dt.year, month=8, day=11)       # termino horario invierno
        # -------------------
        dston = start - timedelta(days=start.weekday() + 1)
        dstoff = end - timedelta(days=start.weekday() + 1)
        # -------------------
        if dston <= dt.replace(tzinfo=None) <= dstoff:
            return timedelta(hours=-1)
        else:
            return timedelta(0)

    def tzname(self, dt):
        return u'CLT'

    def utcoffset(self, dt):
        return timedelta(hours=-3) + self.dst(dt)


def time(date):
    try:
        import pytz
        gmt0 = pytz.timezone(u'GMT+0')
        clt = time_clt()
        temp = datetime.strptime(date, u'%Y-%m-%d %H:%M:%S')
        temp = temp.replace(tzinfo=gmt0)
        return unicode(temp.astimezone(clt).strftime(u'%Y-%m-%d %H:%M:%S'))
    except:
        return u'No disponible'
