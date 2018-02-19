# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import copy
import numpy as np
import sqlite3 as lite
from psychopy import visual, colors


# =============================================================================
# Class: Utils
# =============================================================================
class Utils(object):
    # =================================
    def __init__(self):
        pass

    # =================================
    @staticmethod
    def format_text(word, lmin=0, lmax=-1):
        try:
            temp = unicode(word)
            if lmax <= lmin <= len(temp) or lmin <= len(temp) <= lmax:
                return temp
            else:
                return u''
        except ValueError:
            return u''

    @staticmethod
    def format_int(value, vmin=0, default=None):
        try:
            temp = int(value)
            if temp >= vmin:
                return temp
            else:
                return default
        except ValueError:
            return default

    @staticmethod
    def format_float(value, vmin=0.0, default=None):
        try:
            temp = float(value)
            if temp >= vmin:
                return temp
            else:
                return default
        except ValueError:
            return default

    @staticmethod
    def format_bool(state, default=False):
        try:
            temp = bool(state)
            return temp
        except ValueError:
            return default

    @staticmethod
    def format_path(path):
        import platform
        # -------------------
        path = Utils.format_text(path)
        is_win = any(platform.win32_ver())
        # -------------------
        path = path.replace(u'\\', u'#').replace(u'/', u'#')
        return path.replace(u'#', u'\\') if is_win else path.replace(u'#', u'/')

    @staticmethod
    def get_time(date):
        import pytz
        from datetime import datetime as dt
        # -------------------
        try:
            gmt0 = pytz.timezone(u"GMT+0")
            cltc = pytz.timezone(u"Chile/Continental")
            date = Utils.format_text(date)
            date = dt.strptime(date, u'%Y-%m-%d %H:%M:%S')
            date = date.replace(tzinfo=gmt0)
            return unicode(date.astimezone(cltc).strftime(u'%Y-%m-%d %H:%M:%S'))
        except ValueError:
            return u'No disponible'


# =============================================================================
# Class: SaccadeDB
# =============================================================================
class SaccadeDB(object):
    # =================================
    def __init__(self, filepath=u'saccadedb.sqlite3'):
        self.__db_connection = None
        self.__db_file = filepath
        self.__db_script = self.__get_script_path()
        # -------------------
        self.connect()

    # =================================
    @staticmethod
    def __get_script_path():
        path_base = os.path.split(os.path.realpath(__file__))[0]
        path_conf = Utils.format_path(u'/resources/database/')
        return path_base + path_conf + u'saccadedb_sqlite.sql'

    # =================================
    def connect(self):
        print u"Connecting to DB... "
        if os.path.isfile(self.__db_file):
            self.__db_connection = lite.connect(self.__db_file)
            self.__db_connection.executescript(u"pragma recursive_triggers=1; pragma foreign_keys=1;")
            print u'Connected!'
        else:
            sql = open(self.__db_script, u'r').read()
            self.__db_connection = lite.connect(self.__db_file)
            self.__db_connection.executescript(sql)
            print u"Database not found. A new one was created."

    def close(self):
        try:
            self.__db_connection.close()
            print u"Disconnected!"
            return True
        except lite.Error, event:
            print u"Error: %s" % event.args[0]
            return False

    # =================================
    def push_query(self, query):       # insert, update, delete
        try:
            self.__db_connection.executescript(query)
            self.__db_connection.commit()
            return True
        except lite.Error, event:
            if self.__db_connection:
                self.__db_connection.rollback()
            print u"Error: %s" % event.args[0]
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
        except lite.Error, event:
            print u"Error: %s" % event.args[0]
            return None


# =============================================================================
# Class: Utils
# =============================================================================
class Master(object):
    def __init__(self):
        self.__in_db = False
        self.__database = None
        # -------------------
        self.__name = u'Unnamed'
        self.__screen = 0
        self.__tracker = u'none'
        self.__monitor = u'default'
        self.__path = self.__get_base_path()

    # =================================
    @classmethod
    def get_list(cls, db):
        if isinstance(db, SaccadeDB):
            sql = u"""
            select mas_name
            from master
            order by mas_name asc;
            """
            return db.pull_query(query=sql)
        else:
            return None

    # =================================
    @staticmethod
    def get_available_trackers():
        import glob as gl
        # -------------------
        path_base = os.path.split(os.path.realpath(__file__))[0]
        path_conf = Utils.format_path(u'/resources/eyetrackers/')
        path_full = path_base + path_conf
        # -------------------
        return [os.path.basename(item).replace(u'_config.yaml', u'') for item in gl.glob(path_full+u'*.yaml')]

    @staticmethod
    def get_available_screens():
        import pyglet
        # -------------------
        display = pyglet.window.Display()
        screens = display.get_screens()
        # -------------------
        scr_num = 1
        scr_lst = []
        for screen in screens:
            scr_lst.append(u"monitor %d: (w=%s, h=%s)" % (scr_num, screen.width, screen.height))
            scr_num += 1
        # -------------------
        return scr_lst

    @staticmethod
    def get_available_monitors():
        from psychopy import monitors
        # -------------------
        return monitors.getAllMonitors()

    @staticmethod
    def __get_base_path():
        import sys
        # -------------------
        path_base = os.path.dirname(os.path.realpath(sys.argv[0]))
        path_fold = Utils.format_path(u'/events')
        return path_base + path_fold

    # =================================
    def set_database(self, db):
        if isinstance(db, SaccadeDB):
            self.__database = db
            return True
        else:
            return False

    def get_database(self):
        return self.__database

    def is_on_database(self):
        return self.__in_db

    # -----------------------
    def set_name(self, name):
        name = Utils.format_text(name, lmin=3, lmax=50)
        if self.__database is not None and name != u'':
            sql = u"select * from master where mas_name='%s';" % name
            mas_res = self.__database.pull_query(query=sql)
            # ---------------
            if mas_res is None:
                self.__name = name
                return True
            else:
                return False
        else:
            return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_screen(self, screen):
        screen = Utils.format_int(screen, default=0)
        if 0 <= screen < len(self.get_available_screens()):
            self.__screen = screen
            return True
        else:
            return False

    def get_screen(self):
        try:
            return self.get_available_screens()[self.__screen]
        except:
            return self.get_available_screens()[0]

    # -----------------------
    def set_monitor(self, monitor):
        monitor = Utils.format_text(monitor)
        if monitor in self.get_available_monitors():
            self.__monitor = monitor
            return True
        else:
            return False

    def get_monitor(self):
        return self.__monitor

    # -----------------------
    def set_tracker(self, tracker):
        tracker = Utils.format_text(tracker)
        if tracker in self.get_available_trackers():
            self.__tracker = tracker
            return True
        else:
            return False

    def get_tracker_name(self):
        return self.__tracker

    def get_tracker_conf_path(self):
        if self.__tracker in self.get_available_trackers():
            path_base = os.path.split(os.path.realpath(__file__))[0]
            path_conf = Utils.format_path(u'/resources/eyetrackers/')
            return path_base + path_conf + self.__tracker + u'_config.yaml'
        else:
            return u''

    # -----------------------
    def set_experiment_path(self, path):
        # import sys
        # -------------------
        exp_path = Utils.format_text(path, lmin=0, lmax=200)
        if os.path.isdir(exp_path):
            # base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
            # self.__path = os.path.relpath(exp_path, base_path)
            self.__path = exp_path
            return True
        else:
            return False

    def get_experiment_path(self):
        return self.__path

    # =================================
    def load(self, name):
        name = Utils.format_text(name, lmin=3, lmax=50)
        if self.__database is not None and name != u'':
            sql = u"""
            select 
            mas_screen, mas_monitor, mas_tracker, mas_path
            from master
            where mas_name='%s';
            """ % name
            mas_res = self.__database.pull_query(query=sql)
            # ---------------
            if mas_res is not None:
                self.__in_db = True
                self.__name = name
                print u"Configuration profile %s loaded." % name
                # -----------
                self.__screen = int(mas_res[0, 0])
                self.__monitor = unicode(mas_res[0, 1])
                self.__tracker = unicode(mas_res[0, 2])
                self.__path = unicode(mas_res[0, 3])
                # -----------
                return True
            else:
                print u"Configuration profile %s doesn't exists." % name
                return False
        else:
            print u'Error: Database or configuration profile name not configured!'
            return False

    def save(self):
        if self.__database is not None and self.__name != u'' and self.__tracker != u'none':
            sql = u"""
            insert or replace into master
            (mas_name, mas_screen, mas_tracker, mas_monitor, mas_path)
            values ('%s', '%d', '%s', '%s', '%s')
            """ % (self.__name, self.__screen, self.__tracker, self.__monitor, self.__path)
            mas_res = self.__database.push_query(query=sql)
            # ---------------
            if mas_res:
                print u"Configuration profile %s saved." % self.__name
            else:
                print u"Configuration profile %s not saved." % self.__name
            self.__in_db = mas_res
            return mas_res
        else:
            print u"Error: Database or configuration profile identifiers not configured!"
            return False

    def copy(self, name):
        new_mas = copy.deepcopy(self)
        # -------------------
        new_mas.set_database(db=self.__database)
        new_mas.__in_db = False
        # -------------------
        name_check = new_mas.set_name(name=name)
        # -------------------
        if name_check:
            return new_mas
        else:
            return None

    def remove(self):
        if self.__in_db:
            sql = u"delete from master where mas_name='%s';" % self.__name
            mas_res = self.__database.push_query(query=sql)
            # ---------------
            self.__in_db = not mas_res
            return mas_res
        else:
            return False

    # =================================
    def get_iohub(self):
        import yaml
        # -------------------
        if self.__in_db:
            configuration = {
                u'monitor_devices': [
                    {u'Display': {
                        u'name':                            u'display',
                        u'reporting_unit_type':             u'pix',
                        u'device_number':                   self.__screen,
                        u'psychopy_monitor_name':           self.__monitor,
                        u'override_using_psycho_settings':  True,
                    }},
                    {u'Keyboard': {
                        u'name':        u'keyboard',
                        u'enable':      True,
                        u'save_events': True,
                    }},
                    {u'Experiment': {
                        u'name':        u'experimentRuntime',
                        u'enable':      True,
                        u'save_events': True,
                    }}
                ],
                u'data_store': {
                    u'enable':      True,
                }
            }
            # -------------------
            tracker_path = self.get_tracker_conf_path()
            tracker = yaml.load(open(tracker_path, u'r'))[u'monitor_devices'][0]
            configuration[u'monitor_devices'].append(tracker)
            # -------------------
            return configuration
        else:
            return None

    def get_configuration(self):
        if self.__in_db:
            configuration = {
                u'name':            self.__name,
                u'screen':          self.__screen,
                u'tracker':         self.__tracker,
                u'monitor':         self.__monitor,
                u'experiment_path': self.__path,
            }
            return configuration
        else:
            return None


# =============================================================================
# Class type: ItemList
# =============================================================================
class ItemList(object):
    # =================================
    def __init__(self, itemclass):
        self.__item_class = itemclass
        self.__item_array = None

    # =================================
    def _item_add(self, item):
        if isinstance(item, self.__item_class):
            itm_num = self._item_number()
            if itm_num is None:
                self.__item_array = np.array([item], dtype=self.__item_class)
            else:
                self.__item_array = np.insert(arr=self.__item_array, obj=itm_num, values=[item], axis=0)
            return True
        else:
            return False

    def _item_copy(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            new_itm = self.__item_array[index].copy()
            return self._item_add(item=new_itm)
        else:
            return False

    def _item_delete(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            self.__item_array = np.delete(arr=self.__item_array, obj=index, axis=0) if itm_num > 1 else None
            return True
        else:
            return False

    def _item_move_up(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 < index < itm_num:
            temp = self.__item_array[index - 1]
            self.__item_array[index - 1] = self.__item_array[index]
            self.__item_array[index] = temp
            return True
        else:
            return False

    def _item_move_down(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num-1:
            temp = self.__item_array[index + 1]
            self.__item_array[index + 1] = self.__item_array[index]
            self.__item_array[index] = temp
            return True
        else:
            return False

    def _item_get_all(self):
        return self.__item_array

    def _item_get_by_index(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            return self.__item_array[index]
        else:
            return None

    def _item_number(self):
        if self.__item_array is not None:
            return len(self.__item_array)
        else:
            return None


# =============================================================================
# Class: Component
# =============================================================================
class Component(object):
    # =================================
    def __init__(self):
        self.__name = u'Unnamed'
        self.__units = u'deg'
        self.__pos = (0.0, 0.0)
        self.__ori = 0.0
        self.__size = 1.0
        # -------------------
        self.__image = None
        self.__shape = u'square'
        self.__color = u'white'

    # =================================
    @classmethod
    def get_list(cls, db, exp, tes, fra):
        sql = u"""
        select com_index, com_name, com_shape
        from component
        where exp_code='%s' and tes_index='%d' and fra_index='%d'
        order by com_index asc;
        """ % (exp, tes, fra)
        return db.pull_query(query=sql)

    # =================================
    def set_name(self, name):
        name = Utils.format_text(name, lmin=3, lmax=50)
        if name != u'':
            self.__name = name
            return True
        else:
            return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_units(self, units):
        units = Utils.format_text(units, lmin=2, lmax=20)
        if units in [u'norm', u'cm', u'deg', u'degFlat', u'degFlatPos', u'pix']:
            self.__units = units
            return True
        else:
            return False

    def get_units(self):
        return self.__units

    # -----------------------
    def set_position(self, posx, posy):
        posx = Utils.format_float(posx)
        posy = Utils.format_float(posy)
        if posx is not None and posy is not None:
            self.__pos = (posx, posy)
            return True
        else:
            return False

    def get_position(self):
        return self.__pos

    # -----------------------
    def set_orientation(self, ori):
        ori = Utils.format_float(ori)
        if ori is not None:
            self.__ori = ori
            return True
        else:
            return False

    def get_orientation(self):
        return self.__ori

    # -----------------------
    def set_size(self, size):
        size = Utils.format_float(size)
        if size is not None:
            self.__size = size
            return True
        else:
            return False

    def get_size(self):
        return self.__size

    # -----------------------
    def set_image(self, imagepath):
        from PIL import Image
        # -------------------
        imagepath = Utils.format_text(imagepath)
        if imagepath is not u'' and os.path.isfile(imagepath):
            self.__shape = u'image'
            self.__image = Image.open(imagepath)
            return True
        else:
            return False

    def get_image(self):
        return self.__image

    # -----------------------
    def set_shape(self, shape):
        shape = Utils.format_text(shape, lmin=5, lmax=20)
        if shape in [u'arrow', u'circle', u'cross', u'gauss', u'square']:
            self.__shape = shape
            return True
        else:
            return False

    def get_shape(self):
        return self.__shape

    # -----------------------
    def set_color(self, color):
        color = Utils.format_text(color, lmin=3, lmax=20)
        if colors.isValidColor(color):
            self.__color = color
            return True
        else:
            return False

    def get_color(self):
        return self.__color

    # =================================
    def __decode_image(self, encimg):
        from PIL import Image
        from io import BytesIO
        # -------------------
        coded = Utils.format_text(encimg)
        if coded != u'':
            img_buff = BytesIO()
            img_buff.write(coded.decode(u'base64'))
            # -----------
            self.__shape = u'image'
            self.__image = Image.open(img_buff)
        else:
            self.__image = None

    def __encode_image(self):
        from io import BytesIO
        # -------------------
        if self.__image is not None:
            img_buff = BytesIO()
            self.__image.save(img_buff, u'PNG')
            return img_buff.getvalue().encode(u'base64')
        else:
            return u''

    # =================================
    def load(self, db, exp, tes, fra, com):
        sql = u"""
        select
        com_name, com_units, com_pos_x, com_pos_y, com_orientation, com_size, com_image, com_shape, com_color
        from component
        where exp_code='%s' and tes_index='%d' and fra_index='%d' and com_index='%d';
        """ % (exp, tes, fra, com)
        com_res = db.pull_query(query=sql)
        # -------------------
        if com_res is not None:
            print u"Exp %s, Tes %d, Fra %d: Component %d loaded." % (exp, tes, fra, com)
            # ---------------
            self.__name = unicode(com_res[0, 0])
            self.__units = unicode(com_res[0, 1])
            self.__pos = (float(com_res[0, 2]),
                          float(com_res[0, 3]))
            self.__ori = float(com_res[0, 4])
            self.__size = float(com_res[0, 5])
            self.__shape = unicode(com_res[0, 7])
            self.__color = unicode(com_res[0, 8])
            # ---------------
            self.__decode_image(unicode(com_res[0, 6]))
            # ---------------
            return True
        else:
            print u"Exp %s, Tes %d, Fra %d: Component %d doesn't exists." % (exp, tes, fra, com)
            return False

    def save(self, db, exp, tes, fra, com):
        sql = u"""
        insert into component
        (exp_code, tes_index, fra_index, com_index, 
        com_name, com_units, com_pos_x, com_pos_y, com_orientation, com_size, 
        com_image, com_shape, com_color)
        values ('%s', '%d', '%d', '%d', '%s', '%s', '%f', '%f', '%f', '%f', '%s', '%s', '%s');
        """ % (
            exp, tes, fra, com,
            self.__name, self.__units, self.__pos[0], self.__pos[1], self.__ori, self.__size,
            self.__encode_image(), self.__shape, self.__color
        )
        com_res = db.push_query(query=sql)
        # ---------------
        if com_res:
            print u"Exp %s, Tes %d, Fra %d: Component %d saved." % (exp, tes, fra, com)
        else:
            print u"Exp %s, Tes %d, Fra %d: Component %d not saved." % (exp, tes, fra, com)
        # ---------------
        return com_res

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def get_execution(self, win):
        if isinstance(win, visual.Window):
            if self.__shape == u'image':
                return visual.ImageStim(win=win, name=self.__name, image=self.__image,
                                        pos=self.__pos, ori=self.__ori, units=self.__units)
            elif self.__shape == u'arrow':
                return visual.ShapeStim(win=win, name=self.__name, lineColor=self.__color, fillColor=self.__color,
                                        size=self.__size, pos=self.__pos, ori=self.__ori, units=self.__units,
                                        vertices=((1.0, 0.0), (0.6667, 0.1667), (0.6667, 0.0667), (0.0, 0.0667),
                                                  (0.0, -0.0667), (0.6667, -0.0667), (0.6667, -0.1667)))
            else:
                return visual.GratingStim(win=win, name=self.__name, color=self.__color, sf=0,
                                          mask=None if self.__shape == u'square' else self.__shape,
                                          size=self.__size, pos=self.__pos, ori=self.__ori, units=self.__units)
        else:
            print u"Error: 'win' must be a psychopy visual.Window instance."
            return None

    def get_configuration(self):
        component = {
            u'name':        self.__name,
            u'units':       self.__units,
            u'position':    self.__pos,
            u'orientation': self.__ori,
            u'size':        self.__size,
            u'image':       self.__encode_image(),
            u'shape':       self.__shape,
            u'color':       self.__color
        }
        return component


# =============================================================================
# Class: Frame (child of ItemList)
# =============================================================================
class Frame(ItemList):
    # =================================
    def __init__(self):
        super(Frame, self).__init__(itemclass=Component)
        # -------------------
        self.__name = u'Unnamed'
        self.__color = u'black'
        self.__is_task = False
        self.__keys_allowed = u''
        self.__keys_selected = u''
        self.__time = 0.5

    # =================================
    @classmethod
    def get_list(cls, db, exp, tes):
        sql = u"""
        select fra_index, fra_name
        from frame
        where exp_code='%s' and tes_index='%d'
        order by fra_index asc;
        """ % (exp, tes)
        return db.pull_query(query=sql)

    # =================================
    def set_name(self, name):
        name = Utils.format_text(name, lmin=3, lmax=20)
        if name != u'':
            self.__name = name
            return True
        else:
            return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_color(self, color):
        color = Utils.format_text(color, lmin=3, lmax=20)
        if colors.isValidColor(color):
            self.__color = color
            return True
        else:
            return False

    def get_color(self):
        return self.__color

    # -----------------------
    def set_as_task(self, state):
        self.__is_task = Utils.format_bool(state, default=self.__is_task)
        if self.__is_task:
            self.__time = 0.0
            return True
        else:
            self.__keys_allowed = u''
            self.__keys_selected = u''
            return False

    def get_state(self):
        return self.__is_task

    # -----------------------
    def set_time(self, value):
        value = Utils.format_float(value)
        if not self.__is_task and value is not None:
            self.__time = value
            return True
        else:
            self.__time = 0.0
            return False

    def get_time(self):
        return self.__time

    # -----------------------
    def set_keys_allowed(self, keys):
        keys = Utils.format_text(keys).replace(unicode(u' '), unicode(u''))
        if self.__is_task and keys != u'':
            self.__keys_allowed = keys
            return True
        else:
            self.__keys_allowed = u''
            return False

    def get_keys_allowed(self):
        return self.__keys_allowed

    # -----------------------
    def set_keys_selected(self, keys):
        keys = Utils.format_text(keys).replace(unicode(u' '), unicode(u''))
        keys.replace(u" ", u"")
        if self.__is_task and self.__keys_allowed != u'' and keys != u'':
            keys_alw = self.__keys_allowed.split(u',')
            keys_sel = keys.split(u',')
            # ---------------
            match = [key for key in keys_sel if key in keys_alw]
            if len(match) == len(keys_sel):
                self.__keys_selected = keys
                return True
            else:
                self.__keys_selected = u''
                return True
        else:
            self.__keys_selected = u''
            return False

    def get_keys_selected(self):
        return self.__keys_selected

    # =================================
    def component_add(self, item):
        return self._item_add(item=item)

    def component_copy(self, index):
        return self._item_copy(index=index)

    def component_delete(self, index):
        return self._item_delete(index=index)

    def component_move_up(self, index):
        return self._item_move_up(index=index)

    def component_move_down(self, index):
        return self._item_move_down(index=index)

    def component_get_by_index(self, index):
        return self._item_get_by_index(index=index)

    def component_get_all(self):
        return self._item_get_all()

    def component_number(self):
        return self._item_number()

    # =================================
    def load(self, db, exp, tes, fra):
        sql = u"""
        select
        fra_name, fra_color, fra_is_task, fra_time, fra_keys_allowed, fra_keys_selected
        from frame
        where exp_code='%s' and tes_index='%d' and fra_index='%d';
        """ % (exp, tes, fra)
        fra_res = db.pull_query(query=sql)
        # -------------------
        if fra_res is not None:
            print u"Exp %s, Tes %d: Frame %d loaded." % (exp, tes, fra)
            # ---------------
            self.__name = unicode(fra_res[0, 0])
            self.__color = unicode(fra_res[0, 1])
            self.__is_task = bool(int(fra_res[0, 2]))
            self.__time = float(fra_res[0, 3])
            self.__keys_allowed = unicode(fra_res[0, 4])
            self.__keys_selected = unicode(fra_res[0, 5])
            # ---------------
            self.__load_components(db=db, exp=exp, tes=tes, fra=fra)
            # ---------------
            return True
        else:
            print u"Exp %s, Tes %d: Frame %d doesn't exists." % (exp, tes, fra)
            return False

    def save(self, db, exp, tes, fra):
        sql = u"""
        insert into frame
        (exp_code, tes_index, fra_index, 
        fra_name, fra_color, fra_is_task, fra_time, fra_keys_allowed, fra_keys_selected)
        values ('%s', '%d', '%d', '%s', '%s', '%x', '%f', '%s', '%s');
        """ % (
            exp, tes, fra,
            self.__name, self.__color, self.__is_task, self.__time, self.__keys_allowed, self.__keys_selected
        )
        fra_res = db.push_query(query=sql)
        # -------------------
        if fra_res:
            print u"Exp %s, Tes %d: Frame %d saved. Saving components..." % (exp, tes, fra)
            self.__save_components(db=db, exp=exp, tes=tes, fra=fra)
        else:
            print u"Exp %s, Tes %d: Frame %d not saved." % (exp, tes, fra)
        # -------------------
        return fra_res

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def __load_components(self, db, exp, tes, fra):
        com_lst = Component.get_list(db=db, exp=exp, tes=tes, fra=fra)
        if com_lst is not None:
            for com in com_lst:
                new_com = Component()
                new_com.load(db=db, exp=exp, tes=int(tes), fra=int(fra), com=int(com[0]))
                self.component_add(item=new_com)
        else:
            print u"Exp %s, Tes %d: Frame %d don't have any component saved on the DB." % (exp, tes, fra)

    def __save_components(self, db, exp, tes, fra):
        com_num = self.component_number()
        if com_num is not None:
            for index in range(com_num):
                self.component_get_by_index(index=index).save(db=db, exp=exp, tes=tes, fra=fra, com=index)
        else:
            print u"Exp %s, Tes %d: Frame %d don't have any component to be saved." % (exp, tes, fra)

    # =================================
    def get_execution(self, win):
        if isinstance(win, visual.Window):
            com_num = self.component_number()
            if com_num is not None:
                components = [component.get_execution(win=win) for component in self.component_get_all()]
            else:
                components = None
            # ---------------
            back = visual.Rect(win=win, width=win.size[0], height=win.size[1], units=u'pix',
                               lineColor=self.__color, fillColor=self.__color)
            # ---------------
            frame = {
                u'is_task':             self.__is_task,
                u'time':                self.__time,
                u'allowed_keys':        self.__keys_allowed.replace(u'space', u' ').split(u','),
                u'correct_keys':        self.__keys_selected.replace(u'space', u' ').split(u','),
                u'correct_keys_str':    self.__keys_selected,
                u'background':          back,
                u'components':          components
            }
            # ---------------
            return frame
        else:
            print u"Error: 'win' must be a psychopy visual.Window instance."
            return None

    def get_configuration(self):
        com_num = self.component_number()
        if com_num is not None:
            components = [component.get_configuration() for component in self.component_get_all()]
        else:
            components = None
        # ---------------
        frame = {
            u'is_task':         self.__is_task,
            u'time':            self.__time,
            u'allowed_keys':    self.__keys_allowed,
            u'correct_keys':    self.__keys_selected,
            u'background':      self.__color,
            u'components':      components,
        }
        # ---------------
        return frame


# =============================================================================
# Class: Test (child of ItemList)
# =============================================================================
class Test(ItemList):
    # =================================
    def __init__(self):
        super(Test, self).__init__(itemclass=Frame)
        # -------------------
        self.__name = u'Unnamed'
        self.__description = u''
        self.__quantity = 1

    # =================================
    @classmethod
    def get_list(cls, db, exp):
        sql = u"""
        select tes_index, tes_name, tes_quantity
        from test
        where exp_code='%s'
        order by tes_index asc;
        """ % exp
        return db.pull_query(query=sql)

    # =================================
    def set_name(self, name):
        name = Utils.format_text(name, lmin=3, lmax=50)
        if name != u'':
            self.__name = name
            return True
        else:
            return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_description(self, text):
        text = Utils.format_text(text, lmin=10)
        if text != u'':
            self.__description = text
            return True
        else:
            return False

    def get_description(self):
        return self.__description

    # -----------------------
    def set_quantity(self, value):
        value = Utils.format_int(value, vmin=1)
        if value is not None:
            self.__quantity = value
            return True
        else:
            return False

    def get_quantity(self):
        return self.__quantity

    # =================================
    def frame_add(self, item):
        return self._item_add(item=item)

    def frame_copy(self, index):
        return self._item_copy(index=index)

    def frame_delete(self, index):
        return self._item_delete(index=index)

    def frame_move_up(self, index):
        return self._item_move_up(index=index)

    def frame_move_down(self, index):
        return self._item_move_down(index=index)

    def frame_get_by_index(self, index):
        return self._item_get_by_index(index=index)

    def frame_get_all(self):
        return self._item_get_all()

    def frame_number(self):
        return self._item_number()

    # =================================
    def load(self, db, exp, tes):
        sql = u"""
        select
        tes_name, tes_description, tes_quantity
        from test
        where exp_code='%s' and tes_index='%d';
        """ % (exp, tes)
        tes_res = db.pull_query(query=sql)
        # -------------------
        if tes_res is not None:
            print u"Exp %s: Test %d loaded." % (exp, tes)
            # ---------------
            self.__name = unicode(tes_res[0, 0])
            self.__description = unicode(tes_res[0, 1])
            self.__quantity = int(tes_res[0, 2])
            # ---------------
            self.__load_frames(db=db, exp=exp, tes=tes)
            # ---------------
            return True
        else:
            print u"Exp %s: Test %d doesn't exists." % (exp, tes)
            return False

    def save(self, db, exp, tes):
        sql = u"""
        insert into test
        (exp_code, tes_index, tes_name, tes_description, tes_quantity) 
        values ('%s', '%d', '%s', '%s', '%d');
        """ % (
            exp, tes,
            self.__name, self.__description, self.__quantity
        )
        tes_res = db.push_query(query=sql)
        # -------------------
        if tes_res:
            print u"Exp %s: Test %d saved. Saving frames..." % (exp, tes)
            self.__save_frames(db=db, exp=exp, tes=tes)
        else:
            print u"Exp %s: Test %d not saved." % (exp, tes)
        # -------------------
        return tes_res

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def __load_frames(self, db, exp, tes):
        fra_lst = Frame.get_list(db=db, exp=exp, tes=tes)
        if fra_lst is not None:
            for fra in fra_lst:
                new_fra = Frame()
                new_fra.load(db=db, exp=exp, tes=int(tes), fra=int(fra[0]))
                self.frame_add(item=new_fra)
        else:
            print u"Exp %s: Test %d don't have any frame saved on the DB." % (exp, tes)

    def __save_frames(self, db, exp, tes):
        fra_num = self.frame_number()
        if fra_num is not None:
            for index in range(fra_num):
                self.frame_get_by_index(index=index).save(db=db, exp=exp, tes=tes, fra=index)
        else:
            print u"Exp %s: Test %d don't have any frame to be saved." % (exp, tes)

    # =================================
    def get_execution(self, win):
        if isinstance(win, visual.Window):
            fra_num = self.frame_number()
            if fra_num is not None:
                frames = [frame.get_execution(win=win) for frame in self.frame_get_all()]
                test = {
                    u'name':        self.__name,
                    u'secuence':    np.full(shape=(self.__quantity, 1), fill_value=1, dtype=int),
                    u'frames':      frames
                }
                return test
            else:
                return None
            # ---------------
        else:
            print u"Error: 'win' must be a psychopy visual.Window instance."
            return None

    def get_configuration(self):
        fra_num = self.frame_number()
        if fra_num is not None:
            frames = [frame.get_configuration() for frame in self.frame_get_all()]
            test = {
                u'name': self.__name,
                u'repetitions': self.__quantity,
                u'description': self.__description,
                u'frames': frames,
            }
            return test
        else:
            return None


# =============================================================================
# Class: Experiment (child of ItemList)
# =============================================================================
class Experiment(ItemList):
    # =================================
    def __init__(self):
        super(Experiment, self).__init__(itemclass=Test)
        # -------------------
        self.__in_db = False
        self.__database = None
        # -------------------
        self.__code = u''
        self.__name = u'Unnamed'
        self.__version = u''
        self.__description = u''
        self.__instructions = u''
        self.__comments = u''
        # -------------------
        self.__date_created = u'Not available'
        self.__date_updated = u'Not available'
        # -------------------
        self.__dia_is_active = True
        self.__dia_ask_age = True
        self.__dia_ask_gender = True
        self.__dia_ask_glasses = True
        self.__dia_ask_eye_color = True
        # -------------------
        self.__con_need_space = False
        self.__con_is_random = False
        self.__con_is_rest = False
        self.__con_rest_time = 0.0
        self.__con_rest_period = 0

    # =================================
    @classmethod
    def get_experiment_list(cls, db):
        sql = u"""
        select exp_code, exp_name, exp_version
        from experiment
        order by exp_name asc;
        """
        return db.pull_query(query=sql)

    # =================================
    def set_database(self, db):
        if isinstance(db, SaccadeDB):
            self.__database = db
            return True
        else:
            return False

    def get_database(self):
        return self.__database

    def is_on_database(self):
        return self.__in_db

    # -----------------------
    def set_code(self, code):
        code = Utils.format_text(code, lmin=3, lmax=10)
        if self.__database is not None and code != u'':
            sql = u"select * from experiment where exp_code='%s';" % code
            exp_res = self.__database.pull_query(query=sql)
            # ---------------
            if exp_res is None:
                self.__code = code
                return True
            else:
                return False
        else:
            return False

    def get_code(self):
        return self.__code

    # -----------------------
    def set_info(self, name, version):
        name = Utils.format_text(name, lmin=3, lmax=50)
        version = Utils.format_text(version, lmin=3, lmax=10)
        if self.__database is not None and name != u'' and version != u'':
            sql = u"select * from experiment where exp_name='%s' and exp_version='%s';" % (name, version)
            exp_res = self.__database.pull_query(query=sql)
            # ---------------
            if exp_res is None:
                self.__name = name
                self.__version = version
                return True
            else:
                return False
        else:
            return False

    def get_name(self):
        return self.__name

    def get_version(self):
        return self.__version

    # -----------------------
    def set_descripton(self, text):
        text = Utils.format_text(text, lmin=10)
        if text != u'':
            self.__description = text
            return True
        else:
            return False

    def get_description(self):
        return self.__description

    # -----------------------
    def set_comments(self, text):
        text = Utils.format_text(text, lmin=10)
        if text != u'':
            self.__comments = text
            return True
        else:
            return False

    def get_comments(self):
        return self.__comments

    # -----------------------
    def set_instruction(self, text):
        text = Utils.format_text(text, lmin=10)
        if text != u'':
            self.__instructions = text
            return True
        else:
            return False

    def get_instruction(self):
        return self.__instructions

    # -----------------------
    def set_dialog(self, status, askage, askgender, askglasses, askeyecolor):
        self.__dia_is_active = Utils.format_bool(status, default=self.__dia_is_active)
        self.__dia_ask_age = Utils.format_bool(askage, default=self.__dia_ask_age)
        self.__dia_ask_gender = Utils.format_bool(askgender, default=self.__dia_ask_gender)
        self.__dia_ask_glasses = Utils.format_bool(askglasses, default=self.__dia_ask_glasses)
        self.__dia_ask_eye_color = Utils.format_bool(askeyecolor, default=self.__dia_ask_eye_color)

    def is_dialog_active(self):
        return self.__dia_is_active

    def is_ask_age(self):
        return self.__dia_ask_age

    def is_ask_gender(self):
        return self.__dia_ask_gender

    def is_ask_glasses(self):
        return self.__dia_ask_glasses

    def is_ask_eye_color(self):
        return self.__dia_ask_eye_color

    # -----------------------
    def set_space_start(self, status):
        self.__con_need_space = Utils.format_bool(status, default=self.__con_need_space)

    def is_space_start(self):
        return self.__con_need_space

    # -----------------------
    def set_random(self, status):
        self.__con_is_random = Utils.format_bool(status, default=self.__con_is_random)

    def is_random(self):
        return self.__con_is_random

    # -----------------------
    def set_rest_conf(self, status, period, time):
        status = Utils.format_bool(status, default=self.__con_is_rest)
        period = Utils.format_int(period, default=-0)
        time = Utils.format_float(time, default=-0.0)
        if status and period > 0 and time > 0.0:
            self.__con_is_rest = status
            self.__con_rest_period = period
            self.__con_rest_time = time
            return True
        else:
            return False

    def is_rest(self):
        return self.__con_is_rest

    def get_rest_period(self):
        return self.__con_rest_period

    def get_rest_time(self):
        return self.__con_rest_time

    # =================================
    def test_add(self, item):
        return self._item_add(item=item)

    def test_copy(self, index):
        return self._item_copy(index=index)

    def test_delete(self, index):
        return self._item_delete(index=index)

    def test_move_up(self, index):
        return self._item_move_up(index=index)

    def test_move_down(self, index):
        return self._item_move_down(index=index)

    def test_get_by_index(self, index):
        return self._item_get_by_index(index=index)

    def test_get_all(self):
        return self._item_get_all()

    def test_number(self):
        return self._item_number()

    # =================================
    def load(self, code):
        code = Utils.format_text(code, lmin=3, lmax=10)
        if self.__database is not None and code != u'':
            sql = u"""
            select
            exp.exp_name, exp.exp_version, exp.exp_description, exp.exp_instructions, exp.exp_comments, 
            exp.exp_date_creation, exp.exp_date_update, 
            dia.dia_is_active, dia.dia_ask_age, dia.dia_ask_gender, dia.dia_ask_glasses, dia.dia_ask_eye_color, 
            con.con_need_space, con.con_is_random, con.con_is_rest, con.con_rest_period, con.con_rest_time 
            from experiment as exp
            inner join exp_dia as dia on exp.exp_code=dia.exp_code
            inner join exp_con as con on exp.exp_code=con.exp_code
            where exp.exp_code='%s';
            """ % code
            exp_res = self.__database.pull_query(query=sql)
            # ---------------
            if exp_res is not None:
                self.__in_db = True
                self.__code = code
                print u"Experiment %s loaded." % self.__code
                # -----------
                self.__name = unicode(exp_res[0, 0])
                self.__version = unicode(exp_res[0, 1])
                self.__description = unicode(exp_res[0, 2])
                self.__instructions = unicode(exp_res[0, 4])
                self.__comments = unicode(exp_res[0, 3])
                self.__date_created = Utils.get_time(exp_res[0, 5])
                self.__date_updated = Utils.get_time(exp_res[0, 6])
                self.__dia_is_active = bool(int(exp_res[0, 7]))
                self.__dia_ask_age = bool(int(exp_res[0, 8]))
                self.__dia_ask_gender = bool(int(exp_res[0, 9]))
                self.__dia_ask_glasses = bool(int(exp_res[0, 10]))
                self.__dia_ask_eye_color = bool(int(exp_res[0, 11]))
                self.__con_need_space = bool(int(exp_res[0, 12]))
                self.__con_is_random = bool(int(exp_res[0, 13]))
                self.__con_is_rest = bool(int(exp_res[0, 14]))
                self.__con_rest_period = int(exp_res[0, 15])
                self.__con_rest_time = float(exp_res[0, 16])
                # -----------
                self.__load_tests()
                # -----------
                return True
            else:
                print u"Experiment %s doesn't exists." % self.__code
                return False
        else:
            print u'Error: Database or experiment code not configured!'
            return False

    def save(self):
        if self.__database is not None and self.__code != u'' and self.__name != u'':
            if self.__in_db:
                sql = u"""
                update experiment set
                exp_name='%s', exp_version='%s', exp_description='%s', exp_comments='%s', exp_instructions='%s'
                where exp_code='%s';
                update exp_dia set 
                dia_is_active='%x', dia_ask_age='%x', dia_ask_gender='%x', dia_ask_glasses='%x', dia_ask_eye_color='%x'
                where exp_code='%s';
                update exp_con set 
                con_need_space='%x', con_is_random='%x', con_is_rest='%x', con_rest_period='%d', con_rest_time='%f'
                where exp_code='%s';
                """ % (
                    self.__name, self.__version, self.__description, self.__comments, self.__instructions, self.__code,
                    self.__dia_is_active, self.__dia_ask_age, self.__dia_ask_gender, self.__dia_ask_glasses,
                    self.__dia_ask_eye_color, self.__code, self.__con_need_space, self.__con_is_random,
                    self.__con_is_rest, self.__con_rest_period, self.__con_rest_time, self.__code
                )
            else:
                sql = u"""
                insert into experiment 
                (exp_code, exp_name, exp_version, exp_description, exp_comments, exp_instructions)
                values ('%s', '%s', '%s', '%s', '%s', '%s');
                insert into exp_dia
                (exp_code, dia_is_active, dia_ask_age, dia_ask_gender, dia_ask_glasses, dia_ask_eye_color)
                values ('%s', '%x', '%x', '%x', '%x', '%x');
                insert into exp_con
                (exp_code, con_need_space, con_is_random, con_is_rest, con_rest_period, con_rest_time)
                values ('%s', '%x', '%x', '%x', '%d', '%f');
                """ % (
                    self.__code, self.__name, self.__version, self.__description, self.__comments, self.__instructions,
                    self.__code, self.__dia_is_active, self.__dia_ask_age, self.__dia_ask_gender,
                    self.__dia_ask_glasses, self.__dia_ask_eye_color, self.__code, self.__con_need_space,
                    self.__con_is_random, self.__con_is_rest, self.__con_rest_period, self.__con_rest_time
                )
            exp_res = self.__database.push_query(query=sql)
            # ---------------
            if exp_res:
                print u"Experiment %s saved. Saving tests..." % self.__code
                self.__save_tests()
            else:
                print u"Experiment %s not saved." % self.__code
            # ---------------
            self.__in_db = exp_res
            return exp_res
        else:
            print u"Error: Database or experiment basic identifiers not configured!"
            return False

    def copy(self, code, version):
        new_exp = copy.deepcopy(self)
        # -------------------
        new_exp.set_database(db=self.__database)
        new_exp.__in_db = False
        # -------------------
        code_check = new_exp.set_code(code=code)
        info_check = new_exp.set_info(name=self.__name, version=version)
        # -------------------
        if code_check and info_check:
            return new_exp
        else:
            return None

    def remove(self):
        if self.__in_db:
            sql = u"delete from experiment where exp_code='%s';" % self.__code
            exp_res = self.__database.push_query(query=sql)
            # ---------------
            self.__in_db = not exp_res
            return exp_res
        else:
            return False

    # =================================
    def __load_tests(self):
        tes_lst = Test.get_list(db=self.__database, exp=self.__code)
        if tes_lst is not None:
            for tes in tes_lst:
                new_tes = Test()
                new_tes.load(db=self.__database, exp=self.__code, tes=int(tes[0]))
                self.test_add(item=new_tes)
        else:
            print u"Experiment %s don't have any test saved on the DB." % self.__code

    def __save_tests(self):
        sql = u"delete from test where exp_code='%s';" % self.__code
        self.__database.push_query(query=sql)
        # -------------------
        tes_num = self.test_number()
        if tes_num is not None:
            for index in range(tes_num):
                self.test_get_by_index(index=index).save(db=self.__database, exp=self.__code, tes=index)
        else:
            print u"Experiment %s don't have any test to be saved." % self.__code

    # =================================
    def get_iohub(self, unixstamp):
        if self.__in_db:
            experiment = {
                u'title':           self.__name,
                u'code':            self.__code,
                u'version':         self.__version,
                u'description':     self.__description,
                u'display_experiment_dialog': True,
                # -----------
                u'session_defaults': {
                    u'name':        u'Session...',
                    u'code':        unixstamp,
                    u'comments':    self.__comments,
                },
                u'display_session_dialog': True,
                u'session_variable_order': [u'name', u'code', u'comments'],
                # -----------
                u'ioHub': {
                    u'enable':  True,
                },
            }
            if self.__dia_is_active:
                experiment[u'session_defaults'][u'user_variables'] = {}
                if self.__dia_ask_age:
                    experiment[u'session_defaults'][u'user_variables'][u'participant_age'] = u'Unknown'
                    experiment[u'session_variable_order'].append(u'participant_age')
                if self.__dia_ask_gender:
                    experiment[u'session_defaults'][u'user_variables'][u'participant_gender'] = [u'Male', u'Female']
                    experiment[u'session_variable_order'].append(u'participant_gender')
                if self.__dia_ask_glasses:
                    experiment[u'session_defaults'][u'user_variables'][u'glasses'] = [u'Yes', u'No']
                    experiment[u'session_defaults'][u'user_variables'][u'contacts'] = [u'Yes', u'No']
                    experiment[u'session_variable_order'].append(u'glasses')
                    experiment[u'session_variable_order'].append(u'contacts')
                if self.__dia_ask_eye_color:
                    experiment[u'session_defaults'][u'user_variables'][u'eye_color'] = u'Unknown'
                    experiment[u'session_variable_order'].append(u'eye_color')

            return experiment
        else:
            print u"Error: To execute a experiment you need to ensure that the experiment is saved on the DB."
            return None

    def get_execution(self, win):
        if isinstance(win, visual.Window) and self.__in_db:
            tes_num = self.test_number()
            if tes_num is not None:
                test_list = []
                test_data = []
                for index in range(tes_num):
                    test = self.test_get_by_index(index=index)
                    test = test.get_execution(win=win)
                    if test is not None:
                        test_list.append(index*test[u'secuence'])
                        test_data.append({
                            u'name':    test[u'name'],
                            u'frames':  test[u'frames']
                        })
                # -----------
                test_list = np.concatenate(test_list)
                if self.__con_is_random:
                    np.random.shuffle(test_list)
                # -----------
                experiment = {
                    u'instruction':     self.__instructions,
                    u'space_start':     self.__con_need_space,
                    u'rest_active':     self.__con_is_rest,
                    u'rest_period':     self.__con_rest_period,
                    u'rest_time':       self.__con_rest_time,
                    u'test_secuence':   test_list,
                    u'test_data':       test_data,
                }
                # -----------
                return experiment
            else:
                return None
        else:
            print u"Error: To execute a experiment you need to ensure that:" \
                  u"\n\t- win is instance of pysychopy visual.Window." \
                  u"\n\t- the experiment is saved on the DB."
            return None

    def get_configuration(self):
        if self.__in_db:
            tes_num = self.test_number()
            if tes_num is not None:
                tests = [test.get_configuration() for test in self.test_get_all()]
            else:
                tests = None
            # ---------------
            configuration = {
                u'experiment': {
                    u'title':           self.__name,
                    u'code':            self.__code,
                    u'version':         self.__version,
                    u'description':     self.__description,
                    u'instruction':     self.__instructions,
                    u'session_configuration': {
                        u'comments':    self.__comments,
                        u'space_start': self.__con_need_space,
                        u'randomize':   self.__con_is_random,
                        u'rest': {
                            u'active':  self.__con_is_rest,
                            u'period':  self.__con_rest_period,
                            u'time':    self.__con_rest_time,
                        },
                        u'dialog': {
                            u'active':          self.__dia_is_active,
                            u'ask_age':         self.__dia_ask_age,
                            u'ask_gender':      self.__dia_ask_gender,
                            u'ask_glasses':     self.__dia_ask_glasses,
                            u'ask_eye_color':   self.__dia_ask_eye_color,
                        }
                    },
                    u'tests': tests
                }
            }
            # ---------------
            return configuration
        else:
            return None
