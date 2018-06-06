# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import numpy as np
import sqlite3 as lite


# =============================================================================
# Class: SaccadeDB
# =============================================================================
class SaccadeDB(object):
    # =================================
    def __init__(self, filepath=u""):
        self.__db_script = Utils.format_path(Utils.get_module_path()+u"/app/resources/database/saccadedb_sqlite.sql")
        self.__db_file = u"saccadedb.sqlite3" if filepath == u"" else filepath
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


# =============================================================================
# Class: Utils
# =============================================================================
class Utils(object):
    # =================================
    @staticmethod
    def format_text(text, lmin=None, lmax=None, var_name=u""):
        try:
            text = unicode(text)
            if lmin is not None and len(text) < lmin:
                raise Exception(var_name+u" string too short.")
            if lmax is not None and len(text) > lmax:
                raise Exception(var_name+u" string too long.")
            return text
        except ValueError:
            raise Exception(var_name+u" can't be converted to string.")

    @staticmethod
    def format_int(value, vmin=None, vmax=None, var_name=u""):
        try:
            value = int(value)
            if vmin is not None and value < vmin:
                raise Exception(var_name+u" value too low.")
            if vmax is not None and value > vmax:
                raise Exception(var_name+u" value too high.")
            return value
        except ValueError:
            raise Exception(var_name+u" numeric value needed.")

    @staticmethod
    def format_float(value, vmin=None, vmax=None, var_name=u""):
        try:
            value = float(value)
            if vmin is not None and value < vmin:
                raise Exception(var_name+u" value too low.")
            if vmax is not None and value > vmax:
                raise Exception(var_name+u" value too high.")
            return value
        except ValueError:
            raise Exception(var_name+u" numeric value needed.")

    @staticmethod
    def format_bool(state, var_name=u""):
        try:
            return bool(state)
        except ValueError:
            raise Exception(var_name+u" needs to be boolean or numeric.")

    # =================================
    @staticmethod
    def is_in_list(item, item_list):
        return any(1 for row in item_list if item in row)

    # =================================
    @staticmethod
    def get_time(date):
        import pytz
        from datetime import datetime as dt
        try:
            gmt0 = pytz.timezone(u"GMT+0")
            cltc = pytz.timezone(u"Chile/Continental")
            date = Utils.format_text(date)
            date = dt.strptime(date, u"%Y-%m-%d %H:%M:%S")
            date = date.replace(tzinfo=gmt0)
            return unicode(date.astimezone(cltc).strftime(u"%Y-%m-%d %H:%M:%S"))
        except ValueError:
            return u"No disponible"

    # =================================
    @staticmethod
    def get_main_path():
        import sys
        from os import path
        return path.dirname(path.realpath(sys.argv[0]))

    @staticmethod
    def get_module_path():
        import imp
        return Utils.format_path(imp.find_module(u"saccadeapp")[1])

    @staticmethod
    def format_path(path):
        import platform
        path = Utils.format_text(text=path)
        is_win = any(platform.win32_ver())
        path = path.replace(u"\\", u"#").replace(u"/", u"#")
        return path.replace(u"#", u"\\") if is_win else path.replace(u"#", u"/")

    # =================================
    @staticmethod
    def get_available_colors():
        import collections
        from psychopy import colors
        color_dict = colors.colorsHex
        color_dict = collections.OrderedDict(sorted(color_dict.items()))
        color_arr = [[unicode(item), color_dict[item]] for item in color_dict]
        return color_arr

    @staticmethod
    def get_available_trackers():
        import glob as gl
        from os import path
        trackers_path = Utils.format_path(Utils.get_module_path()+u"/app/resources/eyetrackers/")
        return [path.basename(item).replace(u"_config.yaml", u"") for item in gl.glob(trackers_path + u'*.yaml')]

    @staticmethod
    def get_available_screens():
        import pyglet
        display = pyglet.window.Display()
        screens = display.get_screens()
        scr_num = 1
        scr_lst = []
        for screen in screens:
            scr_lst.append(u"monitor %d: (w=%s, h=%s)" % (scr_num, screen.width, screen.height))
            scr_num += 1
        return scr_lst

    @staticmethod
    def get_available_monitors():
        from psychopy import monitors
        return monitors.getAllMonitors()

    @staticmethod
    def get_available_units():
        return [u"norm", u"cm", u"deg", u"degFlat", u"degFlatPos", u"pix"]

    @staticmethod
    def get_available_shapes():
        return [u"arrow", u"circle", u"cross", u"gauss", u"square"]

    # =================================
    @staticmethod
    def open_documentation():
        import os
        docu_path = Utils.format_path(Utils.get_main_path()+u"/../docs/saccadeApp_docu.pdf")
        os.startfile(docu_path)

    @staticmethod
    def open_psychopy_monitor_center():
        import threading
        from subprocess import call
        is_open = False
        threads = threading.enumerate()
        for process in threads:
            if process.getName() == u"MonitorCenter":
                is_open = True
        if is_open:
            print u"Error: Monitor Center is already open."
            return False
        print u"Opening Monitor Center..."
        monitor_path = Utils.format_path(Utils.get_module_path()+u"/app/resources/subprocess/monitorCenter.py")
        monitor_thread = threading.Thread(target=lambda: call([u"python", monitor_path]))
        monitor_thread.setName(name=u"MonitorCenter")
        monitor_thread.start()
        return True


# =============================================================================
# Switch-Else
# =============================================================================
class Switch:
    def __init__(self, value):
        self._val = value

    def __enter__(self):
        return self

    def __exit__(self, swt_type, value, traceback):  # Allows traceback to occur
        return False

    def __call__(self, *mconds):
        return self._val in mconds
