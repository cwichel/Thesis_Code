# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================


# =============================================================================
# Methods
# =============================================================================
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


def format_bool(state, var_name=u""):
    try:
        return bool(state)
    except ValueError:
        raise Exception(var_name+u" needs to be boolean or numeric.")


# =================================
def is_in_list(item, item_list):
    return any(1 for row in item_list if item in row)


# =================================
def get_time(date):
    import pytz
    from datetime import datetime as dt
    try:
        gmt0 = pytz.timezone(u"GMT+0")
        cltc = pytz.timezone(u"Chile/Continental")
        date = format_text(date)
        date = dt.strptime(date, u"%Y-%m-%d %H:%M:%S")
        date = date.replace(tzinfo=gmt0)
        return unicode(date.astimezone(cltc).strftime(u"%Y-%m-%d %H:%M:%S"))
    except ValueError:
        return u"No disponible"


# =================================
def get_main_path():
    import sys
    from os import path
    return path.dirname(path.realpath(sys.argv[0]))


def get_module_path():
    import imp
    return format_path(imp.find_module(u"saccadeapp")[1])


def format_path(path):
    import platform
    path = format_text(text=path)
    is_win = any(platform.win32_ver())
    path = path.replace(u"\\", u"#").replace(u"/", u"#")
    return path.replace(u"#", u"\\") if is_win else path.replace(u"#", u"/")


# =================================
def get_available_colors():
    import collections
    from psychopy import colors
    color_dict = colors.colorsHex
    color_dict = collections.OrderedDict(sorted(color_dict.items()))
    color_arr = [[unicode(item), color_dict[item]] for item in color_dict]
    return color_arr


def get_available_trackers():
    import glob as gl
    from os import path
    trackers_path = format_path(get_module_path()+u"/api/resources/eyetrackers/")
    return [path.basename(item).replace(u"_config.yaml", u"") for item in gl.glob(trackers_path + u'*.yaml')]


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


def get_available_monitors():
    from psychopy import monitors
    return monitors.getAllMonitors()


def get_available_units():
    return [u"norm", u"cm", u"deg", u"degFlat", u"degFlatPos", u"pix"]


def get_available_shapes():
    return [u"arrow", u"circle", u"cross", u"gauss", u"square"]


# =================================
def open_documentation():
    import os
    docu_path = format_path(get_main_path()+u"/../docs/saccadeApp_docu.pdf")
    os.startfile(docu_path)


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
    monitor_path = format_path(get_module_path()+u"/api/resources/subprocess/monitorCenter.py")
    monitor_thread = threading.Thread(target=lambda: call([u"python", monitor_path]))
    monitor_thread.setName(name=u"MonitorCenter")
    monitor_thread.start()
    return True
