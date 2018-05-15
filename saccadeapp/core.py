# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import copy
import numpy as np
from psychopy import visual
from saccadeapp import Utils, SaccadeDB


# =============================================================================
# Class: Utils
# =============================================================================
class Configuration(object):
    def __init__(self, db=None, name=u''):
        self.__in_db = False
        self.__database = None
        # -------------------
        self.__name = u'Unnamed'
        self.__tracker = u'eyegaze'
        self.__monitor = u'default'
        self.__screen = 0
        self.__path = Utils.format_path(Utils.get_main_path()+u'/events/')
        # -------------------
        if self.set_database(db=db):
            self.load(name=name)

    # =================================
    @classmethod
    def get_list(cls, db):
        if isinstance(db, SaccadeDB):
            sql = u"""
            select con_name
            from configuration
            order by con_name asc;
            """
            return db.pull_query(query=sql)
        return None

    # =================================
    def set_database(self, db):
        if isinstance(db, SaccadeDB):
            self.__database = db
            return True
        return False

    def in_database(self):
        return self.__in_db

    # -----------------------
    def set_name(self, name):
        name = Utils.format_text(name, lmin=3, lmax=50)
        if self.__database is not None and name != u'':
            sql = u"select * from configuration where con_name='%s';" % name
            mas_res = self.__database.pull_query(query=sql)
            if mas_res is None:
                self.__name = name
                return True
        return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_screen(self, screen):
        screen = Utils.format_int(screen, default=0)
        if 0 <= screen < len(Utils.get_available_screens()):
            self.__screen = screen
            return True
        return False

    def get_screen(self):
        try:
            return Utils.get_available_screens()[self.__screen]
        except IndexError:
            return Utils.get_available_screens()[0]

    # -----------------------
    def set_monitor(self, monitor):
        monitor = Utils.format_text(monitor)
        if monitor in Utils.get_available_monitors():
            self.__monitor = monitor
            return True
        return False

    def get_monitor(self):
        return self.__monitor

    # -----------------------
    def set_tracker(self, tracker):
        tracker = Utils.format_text(tracker)
        if tracker in Utils.get_available_trackers():
            self.__tracker = tracker
            return True
        return False

    def get_tracker_name(self):
        return self.__tracker

    def get_tracker_conf_path(self):
        if self.__tracker in Utils.get_available_trackers():
            return Utils.format_path(Utils.get_file_path()+u'/resources/eyetrackers/'+self.__tracker+u'_config.yaml')
        return u''

    # -----------------------
    def set_events_path(self, experiment_path):
        from os import path
        experiment_path = Utils.format_path(experiment_path)
        if path.isdir(experiment_path):
            self.__path = experiment_path
            return True
        return False

    def get_events_path(self):
        return self.__path

    # =================================
    def load(self, name):
        name = Utils.format_text(name, lmin=3, lmax=50)
        if self.__database is not None and name != u'':
            sql = u"""
            select 
            con_screen, con_monitor, con_tracker, con_path
            from configuration
            where con_name='%s';
            """ % name
            con_res = self.__database.pull_query(query=sql)
            if con_res is not None:
                self.__in_db = True
                self.__name = name
                self.__screen = int(con_res[0, 0])
                self.__monitor = unicode(con_res[0, 1])
                self.__tracker = unicode(con_res[0, 2])
                self.__path = unicode(con_res[0, 3])
                return True
        return False

    def save(self):
        if self.__database is not None and self.__name != u'' and self.__tracker != u'none':
            sql = u"""
            insert or replace into configuration
            (con_name, con_screen, con_tracker, con_monitor, con_path)
            values ('%s', '%d', '%s', '%s', '%s')
            """ % (self.__name, self.__screen, self.__tracker, self.__monitor, self.__path)
            operation_ok = self.__database.push_query(query=sql)
            self.__in_db = operation_ok
            return operation_ok
        return False

    def copy(self, name):
        new_con = copy.deepcopy(self)
        new_con.set_database(db=self.__database)
        new_con.__in_db = False
        name_check = new_con.set_name(name=name)
        return new_con if name_check else None

    def remove(self):
        if self.__in_db:
            sql = u"delete from configuration where con_name='%s';" % self.__name
            operation_ok = self.__database.push_query(query=sql)
            self.__in_db = not operation_ok
            return operation_ok
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
            tracker_path = self.get_tracker_conf_path()
            tracker = yaml.load(open(tracker_path, u'r'))[u'monitor_devices'][0]
            configuration[u'monitor_devices'].append(tracker)
            return configuration
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
        return None


# =============================================================================
# Class type: ItemList
# =============================================================================
class ItemList(object):
    # =================================
    def __init__(self, item_class):
        self.__item_class = item_class
        self.__list = None

    # =================================
    def _item_add(self, item):
        if isinstance(item, self.__item_class):
            itm_num = self._item_number()
            if itm_num is None:
                self.__list = np.array([item], dtype=self.__item_class)
            else:
                self.__list = np.insert(arr=self.__list, obj=itm_num, values=[item], axis=0)
            return True
        return False

    def _item_copy(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            new_itm = self.__list[index].copy()
            return self._item_add(item=new_itm)
        return False

    def _item_delete(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            self.__list = np.delete(arr=self.__list, obj=index, axis=0) if itm_num > 1 else None
            return True
        return False

    def _item_swap(self, index1, index2):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index1 < itm_num and 0 <= index1 < itm_num:
            temp = self.__list[index1]
            self.__list[index1] = self.__list[index2]
            self.__list[index2] = temp
            return True
        return False

    def _item_move_up(self, index):
        return self._item_swap(index, index-1)

    def _item_move_down(self, index):
        return self._item_swap(index, index+1)

    def _item_get_all(self):
        return self.__list

    def _item_get_by_index(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            return self.__list[index]
        return None

    def _item_number(self):
        if self.__list is not None:
            return len(self.__list)
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
        self.__shape = u'square'
        self.__color = u'white'
        self.__image = None

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
        return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_units(self, units):
        units = Utils.format_text(units, lmin=2, lmax=20)
        if units in [u'norm', u'cm', u'deg', u'degFlat', u'degFlatPos', u'pix']:
            self.__units = units
            return True
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
        return False

    def get_position(self):
        return self.__pos

    # -----------------------
    def set_orientation(self, ori):
        ori = Utils.format_float(ori)
        if ori is not None:
            self.__ori = ori
            return True
        return False

    def get_orientation(self):
        return self.__ori

    # -----------------------
    def set_size(self, size):
        size = Utils.format_float(size)
        if size is not None:
            self.__size = size
            return True
        return False

    def get_size(self):
        return self.__size

    # -----------------------
    def set_image(self, image_path):
        from os import path
        from PIL import Image
        image_path = Utils.format_path(image_path)
        if image_path is not u'' and path.isfile(image_path):
            self.__image = Image.open(image_path)
            self.__shape = u'image'
            return True
        return False

    def get_image(self):
        return self.__image

    # -----------------------
    def set_shape(self, shape):
        shape = Utils.format_text(shape, lmin=5, lmax=20)
        if shape in [u'arrow', u'circle', u'cross', u'gauss', u'square']:
            self.__shape = shape
            return True
        return False

    def get_shape(self):
        return self.__shape

    # -----------------------
    def set_color(self, color):
        from psychopy import colors
        color = Utils.format_text(color, lmin=3, lmax=20)
        if colors.isValidColor(color):
            self.__color = color
            return True
        return False

    def get_color(self):
        return self.__color

    # =================================
    def __decode_image(self, encimg):
        from PIL import Image
        from io import BytesIO
        coded = Utils.format_text(encimg)
        if coded == u'':
            self.__image = None
            return
        img_buff = BytesIO()
        img_buff.write(coded.decode(u'base64'))
        self.__shape = u'image'
        self.__image = Image.open(img_buff)

    def __encode_image(self):
        from io import BytesIO
        if self.__image is None:
            return u''
        img_buff = BytesIO()
        self.__image.save(img_buff, u'PNG')
        return img_buff.getvalue().encode(u'base64')

    # =================================
    def load(self, db, exp, tes, fra, com):
        sql = u"""
        select
        com_name, com_units, com_pos_x, com_pos_y, com_orientation, com_size, com_image, com_shape, com_color
        from component
        where exp_code='%s' and tes_index='%d' and fra_index='%d' and com_index='%d';
        """ % (exp, tes, fra, com)
        com_res = db.pull_query(query=sql)
        if com_res is not None:
            self.__name = unicode(com_res[0, 0])
            self.__units = unicode(com_res[0, 1])
            self.__pos = (float(com_res[0, 2]),
                          float(com_res[0, 3]))
            self.__ori = float(com_res[0, 4])
            self.__size = float(com_res[0, 5])
            self.__shape = unicode(com_res[0, 7])
            self.__color = unicode(com_res[0, 8])
            self.__decode_image(unicode(com_res[0, 6]))
            return True
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
        operation_ok = db.push_query(query=sql)
        return operation_ok

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def get_execution(self, win):
        from utils import Switch
        if not isinstance(win, visual.Window):
            return None
        with Switch(self.__shape) as case:
            if case(u'image'):
                return visual.ImageStim(win=win, name=self.__name, image=self.__image,
                                        pos=self.__pos, ori=self.__ori, units=self.__units)
            elif case(u'arrow'):
                return visual.ShapeStim(win=win, name=self.__name, lineColor=self.__color, fillColor=self.__color,
                                        size=self.__size, pos=self.__pos, ori=self.__ori, units=self.__units,
                                        vertices=((1.0, 0.0), (0.6667, 0.1667), (0.6667, 0.0667), (0.0, 0.0667),
                                                  (0.0, -0.0667), (0.6667, -0.0667), (0.6667, -0.1667)))
            else:
                return visual.GratingStim(win=win, name=self.__name, color=self.__color, sf=0,
                                          mask=None if self.__shape == u'square' else self.__shape,
                                          size=self.__size, pos=self.__pos, ori=self.__ori, units=self.__units)

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
        super(Frame, self).__init__(item_class=Component)
        # -------------------
        self.__name = u'Unnamed'
        self.__color = u'black'
        self.__is_task = False
        self.__keys_allowed = u''
        self.__keys_selected = u''
        self.__time = 0.0

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
        return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_color(self, color):
        from psychopy import colors
        color = Utils.format_text(color, lmin=3, lmax=20)
        if colors.isValidColor(color):
            self.__color = color
            return True
        return False

    def get_color(self):
        return self.__color

    # -----------------------
    def set_as_task(self, state):
        self.__is_task = Utils.format_bool(state, default=self.__is_task)
        if self.__is_task:
            self.__time = 0.0
            return True
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
            match = [key for key in keys_sel if key in keys_alw]
            if len(match) == len(keys_sel):
                self.__keys_selected = keys
                return True
            self.__keys_selected = u''
            return True
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
        if fra_res is not None:
            self.__name = unicode(fra_res[0, 0])
            self.__color = unicode(fra_res[0, 1])
            self.__is_task = bool(int(fra_res[0, 2]))
            self.__time = float(fra_res[0, 3])
            self.__keys_allowed = unicode(fra_res[0, 4])
            self.__keys_selected = unicode(fra_res[0, 5])
            self.__load_components(db=db, exp=exp, tes=tes, fra=fra)
            return True
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
        operation_ok = db.push_query(query=sql)
        if operation_ok:
            self.__save_components(db=db, exp=exp, tes=tes, fra=fra)
        return operation_ok

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

    def __save_components(self, db, exp, tes, fra):
        com_num = self.component_number()
        if com_num is not None:
            for index in range(com_num):
                self.component_get_by_index(index=index).save(db=db, exp=exp, tes=tes, fra=fra, com=index)

    # =================================
    def get_execution(self, win):
        if isinstance(win, visual.Window):
            frame = {
                u'is_task':             self.__is_task,
                u'time':                self.__time,
                u'allowed_keys':        self.__keys_allowed.replace(u'space', u' ').split(u','),
                u'correct_keys':        self.__keys_selected.replace(u'space', u' ').split(u','),
                u'correct_keys_str':    self.__keys_selected,
                u'background':          visual.Rect(win=win, width=win.size[0], height=win.size[1], units=u'pix',
                                                    lineColor=self.__color, fillColor=self.__color),
                u'components':          None
            }
            com_num = self.component_number()
            if com_num is not None:
                frame[u'components'] = [component.get_execution(win=win) for component in self.component_get_all()]
            return frame
        return None

    def get_configuration(self):
        frame = {
            u'is_task':         self.__is_task,
            u'time':            self.__time,
            u'allowed_keys':    self.__keys_allowed,
            u'correct_keys':    self.__keys_selected,
            u'background':      self.__color,
            u'components':      None
        }
        com_num = self.component_number()
        if com_num is not None:
            frame[u'components'] = [component.get_configuration() for component in self.component_get_all()]
        return frame


# =============================================================================
# Class: Test (child of ItemList)
# =============================================================================
class Test(ItemList):
    # =================================
    def __init__(self):
        super(Test, self).__init__(item_class=Frame)
        self.__name = u'Unnamed'
        self.__description = u''

    # =================================
    @classmethod
    def get_list(cls, db, exp):
        sql = u"""
        select tes_index, tes_name
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
        return False

    def get_name(self):
        return self.__name

    def set_description(self, text):
        text = Utils.format_text(text, lmin=10)
        if text != u'':
            self.__description = text
            return True
        return False

    def get_description(self):
        return self.__description

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
        if tes_res is not None:
            self.__name = unicode(tes_res[0, 0])
            self.__description = unicode(tes_res[0, 1])
            self.__quantity = int(tes_res[0, 2])
            self.__load_frames(db=db, exp=exp, tes=tes)
            return True
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
        operation_ok = db.push_query(query=sql)
        if operation_ok:
            self.__save_frames(db=db, exp=exp, tes=tes)
        return operation_ok

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

    def __save_frames(self, db, exp, tes):
        fra_num = self.frame_number()
        if fra_num is not None:
            for index in range(fra_num):
                self.frame_get_by_index(index=index).save(db=db, exp=exp, tes=tes, fra=index)

    # =================================
    def get_execution(self, win):
        if isinstance(win, visual.Window):
            test = {
                u'name':        self.__name,
                u'frames':      None,
                u'secuence':    np.full(shape=(self.__quantity, 1), fill_value=1, dtype=int)
            }
            fra_num = self.frame_number()
            if fra_num is not None:
                test[u'frames'] = [frame.get_execution(win=win) for frame in self.frame_get_all()]
            return test
        return None

    def get_configuration(self):
        test = {
            u'name':        self.__name,
            u'repetitions': self.__quantity,
            u'description': self.__description,
            u'frames':      None,
        }
        fra_num = self.frame_number()
        if fra_num is not None:
            test[u'frames'] = [frame.get_configuration() for frame in self.frame_get_all()]
        return test


# =============================================================================
# Class: Experiment (child of ItemList)
# =============================================================================
class Experiment(ItemList):
    # =================================
    def __init__(self, db=None, code=u''):
        super(Experiment, self).__init__(item_class=Test)
        self.__in_db = False
        self.__database = None
        self.__code = u''
        self.__name = u'Unnamed'
        self.__version = u'1.0'
        self.__description = u''
        self.__instruction = u''
        self.__comments = u''
        self.__date_created = u''
        self.__date_updated = u''
        self.__dia_is_active = True
        self.__dia_ask_age = True
        self.__dia_ask_gender = True
        self.__dia_ask_glasses = True
        self.__dia_ask_eye_color = True
        self.__con_need_space = False
        self.__con_is_random = False
        self.__con_is_rest = False
        self.__con_rest_time = 0.0
        self.__con_rest_period = 0
        # -------------------
        if self.set_database(db=db):
            self.load(code=code)

    # =================================
    @classmethod
    def get_list(cls, db):
        sql = u"""
        select exp_code, exp_name, exp_version
        from experiment
        order by exp_name asc, exp_version asc;
        """
        return db.pull_query(query=sql)

    # =================================
    def set_database(self, db):
        if isinstance(db, SaccadeDB):
            self.__database = db
            return True
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
            operation_ok = self.__database.pull_query(query=sql)
            if operation_ok is None:
                self.__code = code
                return True
        return False

    def get_code(self):
        return self.__code

    # -----------------------
    def set_info(self, name, version):
        name = Utils.format_text(name, lmin=3, lmax=50)
        version = Utils.format_text(version, lmin=3, lmax=10)
        if self.__database is not None and name != u'' and version != u'':
            sql = u"select * from experiment where exp_name='%s' and exp_version='%s';" % (name, version)
            operation_ok = self.__database.pull_query(query=sql)
            if operation_ok is None:
                self.__name = name
                self.__version = version
                return True
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
        return False

    def get_description(self):
        return self.__description

    # -----------------------
    def set_comments(self, text):
        text = Utils.format_text(text, lmin=10)
        if text != u'':
            self.__comments = text
            return True
        return False

    def get_comments(self):
        return self.__comments

    # -----------------------
    def set_instruction(self, text):
        text = Utils.format_text(text, lmin=10)
        if text != u'':
            self.__instruction = text
            return True
        return False

    def get_instruction(self):
        return self.__instruction

    # -----------------------
    def set_dialog(self, status, askage=False, askgender=False, askglasses=False, askeyecolor=False):
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
            if exp_res is not None:
                self.__in_db = True
                self.__code = code
                self.__name = unicode(exp_res[0, 0])
                self.__version = unicode(exp_res[0, 1])
                self.__description = unicode(exp_res[0, 2])
                self.__instruction = unicode(exp_res[0, 4])
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
                self.__load_tests()
                return True
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
                    self.__name, self.__version, self.__description, self.__comments, self.__instruction, self.__code,
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
                    self.__code, self.__name, self.__version, self.__description, self.__comments, self.__instruction,
                    self.__code, self.__dia_is_active, self.__dia_ask_age, self.__dia_ask_gender,
                    self.__dia_ask_glasses, self.__dia_ask_eye_color, self.__code, self.__con_need_space,
                    self.__con_is_random, self.__con_is_rest, self.__con_rest_period, self.__con_rest_time
                )
            operation_ok = self.__database.push_query(query=sql)
            self.__in_db = operation_ok
            if operation_ok:
                self.__save_tests()
            return operation_ok
        return False

    def copy(self, code, version):
        new_exp = copy.deepcopy(self)
        new_exp.set_database(db=self.__database)
        new_exp.__in_db = False
        code_check = new_exp.set_code(code=code)
        info_check = new_exp.set_info(name=self.__name, version=version)
        return new_exp if code_check and info_check else None

    def remove(self):
        if self.__in_db:
            print u"Removing expriment with code %s." % self.__code
            sql = u"delete from experiment where exp_code='%s';" % self.__code
            exp_res = self.__database.push_query(query=sql)
            self.__in_db = not exp_res
            return exp_res
        return False

    # =================================
    def __load_tests(self):
        tes_lst = Test.get_list(db=self.__database, exp=self.__code)
        if tes_lst is not None:
            for tes in tes_lst:
                new_tes = Test()
                new_tes.load(db=self.__database, exp=self.__code, tes=int(tes[0]))
                self.test_add(item=new_tes)

    def __save_tests(self):
        sql = u"delete from test where exp_code='%s';" % self.__code
        self.__database.push_query(query=sql)
        tes_num = self.test_number()
        if tes_num is not None:
            for index in range(tes_num):
                self.test_get_by_index(index=index).save(db=self.__database, exp=self.__code, tes=index)

    # =================================
    def get_iohub(self):
        if self.__in_db:
            experiment = {
                u'title':                       self.__name,
                u'code':                        self.__code,
                u'version':                     self.__version,
                u'description':                 self.__description,
                u'display_experiment_dialog':   True,
                u'session_defaults': {
                    u'name':                    u'Session...',
                    u'code':                    0,
                    u'comments':                self.__comments,
                },
                u'display_session_dialog':      True,
                u'session_variable_order':      [u'name', u'code', u'comments'],
                u'ioHub': {
                    u'enable':                  True,
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
        return None

    def get_execution(self, win):
        if isinstance(win, visual.Window) and self.__in_db:
            experiment = {
                u'instruction':     self.__instruction,
                u'space_start':     self.__con_need_space,
                u'rest_active':     self.__con_is_rest,
                u'rest_period':     self.__con_rest_period,
                u'rest_time':       self.__con_rest_time,
                u'test_data':       [],
                u'test_secuence':   []
            }
            tes_num = self.test_number()
            if tes_num is not None:
                experiment[u'test_data'] = []
                experiment[u'test_secuence'] = []
                for index in range(tes_num):
                    test = self.test_get_by_index(index=index)
                    test = test.get_execution(win=win)
                    if test[u'frames'] is not None:
                        experiment[u'test_secuence'].append(index*test[u'secuence'])
                        experiment[u'test_data'].append({
                            u'name':    test[u'name'],
                            u'frames':  test[u'frames']
                        })
                experiment[u'test_secuence'] = np.concatenate(experiment[u'test_secuence'])
                if self.__con_is_random:
                    np.random.shuffle(experiment[u'test_secuence'])
            if experiment[u'test_secuence']:
                return experiment
        return None

    def get_configuration(self):
        if self.__in_db:
            experiment = {
                u'title':                   self.__name,
                u'code':                    self.__code,
                u'version':                 self.__version,
                u'description':             self.__description,
                u'instruction':             self.__instruction,
                u'session_configuration': {
                    u'comments':            self.__comments,
                    u'space_start':         self.__con_need_space,
                    u'randomize':           self.__con_is_random,
                    u'rest': {
                        u'active':          self.__con_is_rest,
                        u'period':          self.__con_rest_period,
                        u'time':            self.__con_rest_time,
                    },
                    u'dialog': {
                        u'active':          self.__dia_is_active,
                        u'ask_age':         self.__dia_ask_age,
                        u'ask_gender':      self.__dia_ask_gender,
                        u'ask_glasses':     self.__dia_ask_glasses,
                        u'ask_eye_color':   self.__dia_ask_eye_color,
                    }
                },
                u'tests':                   None
            }
            tes_num = self.test_number()
            if tes_num is not None:
                experiment[u'tests'] = [test.get_configuration() for test in self.test_get_all()]
            return experiment
        return None
