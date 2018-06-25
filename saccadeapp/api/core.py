# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import copy
from psychopy import visual
from .utils import *
from .saccadedb import SaccadeDB


# =============================================================================
# Class: Configuration
# =============================================================================
class Configuration(object):
    def __init__(self, db=None, name=u""):
        self.__in_db = False
        self.__database = None
        # -------------------
        self.__name = u"Unnamed"
        self.__tracker = u"eyegaze"
        self.__monitor = u"default"
        self.__screen = 0
        self.__path = format_path(get_main_path()+u"/events/")
        # -------------------
        if self.set_database(db=db) and name != u"":
            self.load(name=name)

    # =================================
    @staticmethod
    def get_list(db):
        if isinstance(db, SaccadeDB):
            sql = u"""
            select con_name
            from configuration
            order by con_name asc;
            """
            item_list = db.pull_query(query=sql)
            if item_list is not None:
                return [item for item in item_list]
        return []

    # =================================
    def set_database(self, db):
        if isinstance(db, SaccadeDB):
            self.__database = db
            return True
        return False

    def get_database(self):
        return self.__database

    def in_database(self):
        return self.__in_db

    # -----------------------
    def set_name(self, name):
        name = format_text(text=name, lmin=3, lmax=50, var_name=u"name")
        if self.__database:
            sql = u"select * from configuration where con_name='{0}';".format(name)
            mas_res = self.__database.pull_query(query=sql)
            if mas_res is None:
                self.__name = name
                return True
        return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_screen(self, screen):
        screen_num = len(get_available_screens())
        self.__screen = format_int(value=screen, vmin=0, vmax=screen_num, var_name=u"screen")
        return True

    def get_screen(self):
        try:
            return get_available_screens()[self.__screen]
        except IndexError:
            return get_available_screens()[0]

    # -----------------------
    def set_monitor(self, monitor):
        monitor = format_text(text=monitor, var_name=u"monitor")
        if monitor in get_available_monitors():
            self.__monitor = monitor
            return True
        return False

    def get_monitor(self):
        return self.__monitor

    # -----------------------
    def set_tracker(self, tracker):
        tracker = format_text(text=tracker, var_name=u"tracker")
        if tracker in get_available_trackers():
            self.__tracker = tracker
            return True
        return False

    def get_tracker_name(self):
        return self.__tracker

    def get_tracker_conf_path(self):
        if self.__tracker in get_available_trackers():
            base_path = format_path(get_module_path()+u"/api/resources/eyetrackers/")
            return base_path+self.__tracker+u"_config.yaml"
        return u""

    # -----------------------
    def set_events_path(self, path):
        import os
        path = format_path(path)
        if not os.path.isdir(path):
            os.mkdir(path)
        if os.path.isdir(path):
            self.__path = path
            return True
        return False

    def get_events_path(self):
        return self.__path

    # =================================
    def load(self, name):
        name = format_text(text=name, lmin=3, lmax=50, var_name=u"name")
        if self.__database:
            sql = u"""
            select 
            con_screen, con_monitor, con_tracker, con_path
            from configuration
            where con_name='{0}';
            """.format(name)
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
        if self.__database:
            sql = u"""
            insert or replace into configuration
            (con_name, con_screen, con_tracker, con_monitor, con_path)
            values ('{0}', '{1}', '{2}', '{3}', '{4}')
            """.format(self.__name, self.__screen, self.__tracker, self.__monitor, self.__path)
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
            sql = u"delete from configuration where con_name='{0}';".format(self.__name)
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
                u"monitor_devices": [
                    {u"Display": {
                        u"name":                            u"display",
                        u"reporting_unit_type":             u"pix",
                        u"device_number":                   self.__screen,
                        u"psychopy_monitor_name":           self.__monitor,
                        u"override_using_psycho_settings":  True,
                    }},
                    {u"Keyboard": {
                        u"name":        u"keyboard",
                        u"enable":      True,
                        u"save_events": True,
                    }},
                    {u"Experiment": {
                        u"name":        u"experimentRuntime",
                        u"enable":      True,
                        u"save_events": True,
                    }}
                ],
                u"data_store": {
                    u"enable":      True,
                }
            }
            tracker_path = self.get_tracker_conf_path()
            tracker = yaml.load(open(tracker_path, u"r"))[u"monitor_devices"][0]
            configuration[u"monitor_devices"].append(tracker)
            return configuration
        return None

    def get_configuration(self):
        if self.__in_db:
            configuration = {
                u"name":            self.__name,
                u"screen":          self.__screen,
                u"tracker":         self.__tracker,
                u"monitor":         self.__monitor,
                u"experiment_path": self.__path,
            }
            return configuration
        return None


# =============================================================================
# Class type: ItemList
# =============================================================================
class ItemList(object):
    # =================================
    def __init__(self, item_class):
        self._class = item_class
        self._item_dat = []

    # =================================
    def item_add(self, item):
        if isinstance(item, self._class) and self.check_item_name(item.get_name()) == -1:
            self._item_dat.append(item)
            return True
        return False

    def item_copy(self, item_id, new_name):
        if 0 <= item_id < self.get_items_length():
            new_name = format_text(text=new_name, var_name=u"copy name")
            if new_name is not None and self.check_item_name(new_name) == -1:
                new_item = self._item_dat[item_id].copy()
                new_item.set_name(name=new_name)
                return self.item_add(item=new_item)
        return False

    def item_remove(self, item_id):
        if 0 <= item_id < self.get_items_length():
            self._item_dat.pop(item_id)
            return True
        return False

    def item_replace(self, item_id, new_item):
        if 0 <= item_id < self.get_items_length():
            item_popped = self._item_dat.pop(item_id)
            if isinstance(new_item, self._class) and self.check_item_name(new_item.get_name()) == -1:
                self._item_dat.insert(item_id, new_item)
                return True
            self._item_dat.insert(item_id, item_popped)
            return False

    def item_swap(self, item1_id, item2_id):
        data_len = self.get_items_length()
        if 0 <= item1_id < data_len and 0 <= item2_id < data_len:
            temp = self._item_dat[item1_id]
            self._item_dat[item1_id] = self._item_dat[item2_id]
            self._item_dat[item2_id] = temp
            return True
        return False

    def get_items(self):
        return self._item_dat

    def get_item(self, item_id):
        if 0 <= item_id < self.get_items_length():
            return self._item_dat[item_id]
        return None

    def check_item_name(self, item_name):
        try:
            return self.get_items_str().index(item_name)
        except ValueError:
            return -1

    def get_items_str(self):
        return [item.get_name() for item in self._item_dat]

    def get_items_length(self):
        return len(self._item_dat)


# =============================================================================
# Class type: ItemListSequence
# =============================================================================
class ItemListSequence(ItemList):
    # =================================
    def __init__(self, item_class):
        super(ItemListSequence, self).__init__(item_class=item_class)
        self._item_seq = []

    # =================================
    def item_remove(self, item_id):
        if 0 <= item_id < self.get_items_length():
            item = self._item_dat[item_id]
            self._item_seq = [seq for seq in self._item_seq if seq[0] is not item]
            self._item_dat.pop(item_id)
            return True
        return False

    def item_replace(self, item_id, new_item):
        if 0 <= item_id < self.get_items_length():
            item_popped = self._item_dat.pop(item_id)
            if isinstance(new_item, self._class) and self.check_item_name(new_item.get_name()) == -1:
                self._item_dat.insert(item_id, new_item)
                self._item_seq = [[new_item, seq[1]] if seq[0] == item_popped else seq for seq in self._item_seq]
                return True
            self._item_dat.insert(item_id, item_popped)
            return False

    # =================================
    def sequence_add(self, item_id, quantity):
        quantity = format_int(quantity)
        if 0 <= item_id < self.get_items_length() and quantity is not None:
            self._item_seq.append([self._item_dat[item_id], quantity])
            return True
        return False

    def sequence_edit(self, index, item_id, quantity):
        quantity = format_int(quantity)
        if 0 <= index < self.get_sequence_length() and 0 <= item_id < self.get_items_length() and quantity is not None:
            self._item_seq[index] = [self._item_dat[item_id], quantity]
            return True
        return False

    def sequence_remove(self, index):
        if 0 <= index < self.get_sequence_length():
            self._item_seq.pop(index)
            return True
        return False

    def sequence_swap(self, index1, index2):
        itm_num = self.get_sequence_length()
        if 0 <= index1 < itm_num and 0 <= index2 < itm_num:
            temp = self._item_seq[index1]
            self._item_seq[index1] = self._item_seq[index2]
            self._item_seq[index2] = temp
            return True
        return False

    def get_sequence(self):
        return self._item_seq

    def get_sequence_item(self, index):
        seq_len = self.get_sequence_length()
        if 0 <= index < seq_len:
            return self._item_seq[index]
        return None

    def get_sequence_str(self):
        return [[item[0].get_name(), item[1]] for item in self._item_seq]

    def get_sequence_length(self):
        return len(self._item_seq)


# =============================================================================
# Class: Component
# =============================================================================
class Component(object):
    # =================================
    def __init__(self):
        self.__name = u"Unnamed"
        self.__units = u"deg"
        self.__pos = (0.0, 0.0)
        self.__rot = 0.0
        self.__size = 1.0
        self.__shape = u"square"
        self.__color = u"white"
        self.__image = None

    def __deepcopy__(self, memo):
        com_copy = Component()
        com_copy.set_name(name=self.__name)
        com_copy.set_units(units=self.__units)
        com_copy.set_position(posx=self.__pos[0], posy=self.__pos[1])
        com_copy.set_rotation(rot=self.__rot)
        com_copy.set_size(size=self.__size)
        com_copy.set_shape(shape=self.__shape)
        com_copy.set_color(color=self.__color)
        com_copy.set_image(image=self.__image)
        return com_copy

    # =================================
    @staticmethod
    def get_list(db, exp, tes, fra):
        if isinstance(db, SaccadeDB):
            sql = u"""
            select com_index, com_name, com_shape
            from component
            where exp_code='{0}' and tes_index='{1}' and fra_index='{2}'
            order by com_index asc;
            """.format(exp, tes, fra)
            item_list = db.pull_query(query=sql)
            if item_list is not None:
                return [[int(item[0]), item[1], item[2]] for item in item_list]
        return []

    # =================================
    def set_name(self, name):
        self.__name = format_text(text=name, lmin=3, lmax=50, var_name=u"name")
        return True

    def get_name(self):
        return self.__name

    # -----------------------
    def set_units(self, units):
        units = format_text(text=units, lmin=2, lmax=20, var_name=u"units")
        if units in get_available_units():
            self.__units = units
            return True
        return False

    def get_units(self):
        return self.__units

    # -----------------------
    def set_position(self, posx, posy):
        posx = format_float(value=posx, vmin=-9999.0, vmax=9999.0, var_name=u"position (x)")
        posy = format_float(value=posy, vmin=-9999.0, vmax=9999.0, var_name=u"position (y)")
        self.__pos = (posx, posy)
        return True

    def get_position(self):
        return self.__pos

    # -----------------------
    def set_rotation(self, rot):
        rot = format_float(value=rot, vmin=-360.0, vmax=360.0, var_name=u"rotation")
        self.__rot = rot
        return True

    def get_rotation(self):
        return self.__rot

    # -----------------------
    def set_size(self, size):
        size = format_float(value=size, vmin=0.0, vmax=9999.0, var_name=u"size")
        self.__size = size
        return True

    def get_size(self):
        return self.__size

    # -----------------------
    def set_image(self, image):
        from os import path
        from PIL import Image
        if image is None:
            return False
        if isinstance(image, Image.Image):
            self.__image = image
            self.__shape = u"image"
            return True
        elif image != u"" and path.isfile(path=image):
            self.__image = Image.open(image)
            self.__shape = u"image"
            return True
        return False

    def remove_image(self):
        self.__image = None

    def get_image(self):
        return self.__image

    # -----------------------
    def set_shape(self, shape):
        shape = format_text(text=shape, lmin=5, lmax=20, var_name=u"shape")
        if shape in get_available_shapes():
            self.__shape = shape
            return True
        return False

    def get_shape(self):
        return self.__shape

    # -----------------------
    def set_color(self, color):
        from psychopy import colors
        color = format_text(text=color, lmin=3, lmax=20, var_name=u"shape color")
        if colors.isValidColor(color):
            self.__color = color
            return True
        return False

    def get_color(self):
        return self.__color

    # =================================
    def __decode_image(self, enc_img):
        from PIL import Image
        from io import BytesIO
        coded = format_text(text=enc_img, var_name=u"encoded image")
        if coded == u"":
            self.__image = None
        else:
            img_buff = BytesIO()
            img_buff.write(coded.decode(u"base64"))
            self.__shape = u"image"
            self.__image = Image.open(img_buff)

    def __encode_image(self):
        from io import BytesIO
        if self.__image is None:
            return u""
        img_buff = BytesIO()
        self.__image.save(img_buff, u"PNG")
        return img_buff.getvalue().encode(u"base64")

    # =================================
    def load(self, db, exp, tes, fra, com):
        sql = u"""
        select
        com_name, com_units, com_pos_x, com_pos_y, com_rotation, com_size, com_image, com_shape, com_color
        from component
        where exp_code='{0}' and tes_index='{1}' and fra_index='{2}' and com_index='{3}';
        """.format(exp, tes, fra, com)
        com_res = db.pull_query(query=sql)
        if com_res is not None:
            self.__name = unicode(com_res[0, 0])
            self.__units = unicode(com_res[0, 1])
            self.__pos = (float(com_res[0, 2]),
                          float(com_res[0, 3]))
            self.__rot = float(com_res[0, 4])
            self.__size = float(com_res[0, 5])
            self.__shape = unicode(com_res[0, 7])
            self.__color = unicode(com_res[0, 8])
            self.__decode_image(enc_img=unicode(com_res[0, 6]))
            return True
        return False

    def save(self, db, exp, tes, fra, com):
        sql = u"""
        insert into component
        (exp_code, tes_index, fra_index, com_index, 
        com_name, com_units, com_pos_x, com_pos_y, com_rotation, com_size, 
        com_image, com_shape, com_color)
        values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}');
        """.format(
            exp, tes, fra, com,
            self.__name, self.__units, self.__pos[0], self.__pos[1], self.__rot, self.__size,
            self.__encode_image(), self.__shape, self.__color
        )
        operation_ok = db.push_query(query=sql)
        return operation_ok

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def get_execution(self, win):
        from switch import Switch
        if not isinstance(win, visual.Window):
            return None
        with Switch(self.__shape) as case:
            if case(u"image"):
                return visual.ImageStim(win=win, name=self.__name, image=self.__image,
                                        pos=self.__pos, ori=self.__rot, units=self.__units)
            elif case(u"arrow"):
                return visual.ShapeStim(win=win, name=self.__name, lineColor=self.__color, fillColor=self.__color,
                                        size=self.__size, pos=self.__pos, ori=self.__rot, units=self.__units,
                                        vertices=((1.0, 0.0), (0.6667, 0.1667), (0.6667, 0.0667), (0.0, 0.0667),
                                                  (0.0, -0.0667), (0.6667, -0.0667), (0.6667, -0.1667)))
            else:
                return visual.GratingStim(win=win, name=self.__name, color=self.__color, sf=0,
                                          mask=None if self.__shape == u"square" else self.__shape,
                                          size=self.__size, pos=self.__pos, ori=self.__rot, units=self.__units)

    def get_configuration(self):
        component = {
            u"name":        self.__name,
            u"units":       self.__units,
            u"position":    self.__pos,
            u"rotation":    self.__rot,
            u"size":        self.__size,
            u"image":       self.__encode_image(),
            u"shape":       self.__shape,
            u"color":       self.__color
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
        self.__name = u"Unnamed"
        self.__color = u"black"
        self.__is_task = False
        self.__keys_allowed = u""
        self.__keys_correct = u""
        self.__time = 0.0

    # =================================
    @staticmethod
    def get_list(db, exp, tes):
        if isinstance(db, SaccadeDB):
            sql = u"""
            select fra_index, fra_name
            from frame
            where exp_code='{0}' and tes_index='{1}'
            order by fra_index asc;
            """.format(exp, tes)
            item_list = db.pull_query(query=sql)
            if item_list is not None:
                return [[int(item[0]), item[1]] for item in item_list]
        return []

    # =================================
    def set_name(self, name):
        self.__name = format_text(text=name, lmin=3, lmax=50, var_name=u"name")
        return True

    def get_name(self):
        return self.__name

    # -----------------------
    def set_color(self, color):
        from psychopy import colors
        color = format_text(text=color, lmin=3, lmax=20, var_name=u"background")
        if colors.isValidColor(color):
            self.__color = color
            return True
        return False

    def get_color(self):
        return self.__color

    # -----------------------
    def set_as_task(self, state):
        self.__is_task = format_bool(state=state, var_name=u"task selection")
        if self.__is_task:
            self.__time = 0.0
            return True
        self.__keys_allowed = u""
        self.__keys_correct = u""
        return False

    def is_task(self):
        return self.__is_task

    # -----------------------
    def set_time(self, value):
        if not self.__is_task:
            self.__time = format_float(value=value, vmin=0.0, vmax=9999.0, var_name=u"time")
            return True
        return False

    def get_time(self):
        return self.__time

    # -----------------------
    def set_keys_allowed(self, keys):
        if self.__is_task:
            keys = format_text(text=keys, var_name=u"allowed keys").replace(unicode(u" "), unicode(u""))
            self.__keys_allowed = keys
            return True
        return False

    def get_keys_allowed(self):
        return self.__keys_allowed

    # -----------------------
    def set_keys_correct(self, keys):
        if self.__is_task and self.__keys_allowed != u"":
            keys = format_text(text=keys, var_name=u"selected keys").replace(unicode(u" "), unicode(u""))
            allowed = self.__keys_allowed.split(u",")
            selected = keys.split(u",")
            key_match = [key for key in selected if key in allowed]
            if len(key_match) == len(selected):
                self.__keys_correct = keys
                return True
        return False

    def get_keys_correct(self):
        return self.__keys_correct

    # =================================
    def load(self, db, exp, tes, fra):
        sql = u"""
        select
        fra_name, fra_color, fra_is_task, fra_time, fra_keys_allowed, fra_keys_correct
        from frame
        where exp_code='{0}' and tes_index='{1}' and fra_index='{2}';
        """.format(exp, tes, fra)
        fra_res = db.pull_query(query=sql)
        if fra_res is not None:
            self.__name = unicode(fra_res[0, 0])
            self.__color = unicode(fra_res[0, 1])
            self.__is_task = bool(int(fra_res[0, 2]))
            self.__time = float(fra_res[0, 3])
            self.__keys_allowed = unicode(fra_res[0, 4])
            self.__keys_correct = unicode(fra_res[0, 5])
            self.__load_components(db=db, exp=exp, tes=tes, fra=fra)
            return True
        return False

    def save(self, db, exp, tes, fra):
        sql = u"""
        insert into frame
        (exp_code, tes_index, fra_index, 
        fra_name, fra_color, fra_is_task, fra_time, fra_keys_allowed, fra_keys_correct)
        values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5:x}', '{6}', '{7}', '{8}');
        """.format(
            exp, tes, fra,
            self.__name, self.__color, self.__is_task, self.__time, self.__keys_allowed, self.__keys_correct
        )
        operation_ok = db.push_query(query=sql)
        if operation_ok:
            self.__save_components(db=db, exp=exp, tes=tes, fra=fra)
        return operation_ok

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def __load_components(self, db, exp, tes, fra):
        component_list = Component.get_list(db=db, exp=exp, tes=tes, fra=fra)
        if component_list is not None:
            for component in component_list:
                new_component = Component()
                new_component.load(db=db, exp=exp, tes=int(tes), fra=int(fra), com=int(component[0]))
                self.item_add(item=new_component)

    def __save_components(self, db, exp, tes, fra):
        for component in self._item_dat:
            index = self._item_dat.index(component)
            component.save(db=db, exp=exp, tes=tes, fra=fra, com=index)

    # =================================
    def get_execution(self, win):
        if not isinstance(win, visual.Window):
            return None
        frame = {
            u"name":                self.__name,
            u"is_task":             self.__is_task,
            u"time":                self.__time,
            u"allowed_keys":        self.__keys_allowed.replace(u"space", u" ").split(u","),
            u"correct_keys":        self.__keys_correct.replace(u"space", u" ").split(u","),
            u"correct_keys_str":    self.__keys_correct,
            u"background":          visual.Rect(win=win, width=win.size[0], height=win.size[1], units=u"pix",
                                                lineColor=self.__color, fillColor=self.__color),
            u"components":          [item.get_execution(win=win) for item in self._item_dat]
        }
        return frame

    def get_configuration(self):
        frame = {
            u"name":            self.__name,
            u"is_task":         self.__is_task,
            u"time":            self.__time,
            u"allowed_keys":    self.__keys_allowed,
            u"correct_keys":    self.__keys_correct,
            u"background":      self.__color,
            u"components":      [item.get_configuration() for item in self._item_dat]
        }
        return frame


# =============================================================================
# Class: Test (child of ItemList)
# =============================================================================
class Test(ItemList):
    # =================================
    def __init__(self):
        super(Test, self).__init__(item_class=Frame)
        self.__name = u"Unnamed"
        self.__description = u""

    # =================================
    @staticmethod
    def get_list(db, exp):
        if isinstance(db, SaccadeDB):
            sql = u"""
            select tes_index, tes_name
            from test
            where exp_code='{0}'
            order by tes_index asc;
            """.format(exp)
            item_list = db.pull_query(query=sql)
            if item_list is not None:
                return [[int(item[0]), item[1]] for item in item_list]
        return []

    # =================================
    def set_name(self, name):
        self.__name = format_text(text=name, lmin=3, lmax=50, var_name=u"name")
        return True

    def get_name(self):
        return self.__name

    def set_description(self, text):
        self.__description = format_text(text=text, var_name=u"description")
        return True

    def get_description(self):
        return self.__description

    # =================================
    def load(self, db, exp, tes):
        sql = u"""
        select
        tes_name, tes_description
        from test
        where exp_code='{0}' and tes_index='{1}';
        """.format(exp, tes)
        tes_res = db.pull_query(query=sql)
        if tes_res is not None:
            self.__name = unicode(tes_res[0, 0])
            self.__description = unicode(tes_res[0, 1])
            self.__load_frames(db=db, exp=exp, tes=tes)
            return True
        return False

    def save(self, db, exp, tes):
        sql = u"""
        insert into test
        (exp_code, tes_index, tes_name, tes_description) 
        values ('{0}', '{1}', '{2}', '{3}');
        """.format(
            exp, tes,
            self.__name, self.__description
        )
        operation_ok = db.push_query(query=sql)
        if operation_ok:
            self.__save_frames(db=db, exp=exp, tes=tes)
        return operation_ok

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def __load_frames(self, db, exp, tes):
        frame_list = Frame.get_list(db=db, exp=exp, tes=tes)
        if frame_list is not None:
            for frame in frame_list:
                new_frame = Frame()
                new_frame.load(db=db, exp=exp, tes=int(tes), fra=int(frame[0]))
                self.item_add(item=new_frame)

    def __save_frames(self, db, exp, tes):
        for frame in self._item_dat:
            index = self._item_dat.index(frame)
            frame.save(db=db, exp=exp, tes=tes, fra=index)

    # =================================
    def get_execution(self, win):
        if not isinstance(win, visual.Window):
            return None
        test = {
            u"name":        self.__name,
            u"frames":      [item.get_execution(win=win) for item in self._item_dat]
        }
        return test

    def get_configuration(self):
        test = {
            u"name":        self.__name,
            u"description": self.__description,
            u"frames":      [item.get_configuration() for item in self._item_dat],
        }
        return test


# =============================================================================
# Class: Experiment (child of ItemList)
# =============================================================================
class Experiment(ItemListSequence):
    # =================================
    def __init__(self, db=None, code=u""):
        super(Experiment, self).__init__(item_class=Test)
        self.__in_db = False
        self.__database = None
        # -------------------
        self.__date_created = u""
        self.__date_updated = u""
        # -------------------
        self.__code = u""
        self.__name = u"Unnamed"
        self.__version = u"1.0"
        self.__description = u""
        self.__instructions = u""
        self.__comments = u""
        # -------------------
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
        self.__test_sequence = None
        # -------------------
        if self.set_database(db=db) and code != u"":
            self.load(code=code)

    # =================================
    @staticmethod
    def get_list(db):
        if isinstance(db, SaccadeDB):
            sql = u"""
            select exp_code, exp_name, exp_version, exp_date_creation, exp_date_update
            from experiment
            order by exp_name asc, exp_version asc;
            """
            item_list = db.pull_query(query=sql)
            if item_list is not None:
                return [[item[0], [item[1], item[2]], [item[3], item[4]]] for item in item_list]
        return []

    # =================================
    def set_database(self, db):
        if isinstance(db, SaccadeDB):
            self.__database = db
            return True
        return False

    def get_database(self):
        return self.__database

    def in_database(self):
        return self.__in_db

    # -----------------------
    def set_code(self, code):
        code = format_text(text=code, lmin=3, lmax=10, var_name=u"code")
        if self.__database:
            sql = u"select * from experiment where exp_code='{0}';".format(code)
            operation_ok = self.__database.pull_query(query=sql)
            if operation_ok is None:
                self.__code = code
                return True
        return False

    def get_code(self):
        return self.__code

    # -----------------------
    def set_info(self, name, version):
        name = format_text(text=name, lmin=3, lmax=50, var_name=u"name")
        version = format_text(text=version, lmin=3, lmax=10, var_name=u"version")
        if self.__database:
            sql = u"select * from experiment where exp_name='{0}' and exp_version='{1}';".format(name, version)
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
        self.__description = format_text(text=text, var_name=u"description")
        return True

    def get_description(self):
        return self.__description

    # -----------------------
    def set_comments(self, text):
        self.__comments = format_text(text=text, lmax=50, var_name=u"comments")
        return True

    def get_comments(self):
        return self.__comments

    # -----------------------
    def set_instructions(self, text):
        self.__instructions = format_text(text=text, var_name=u"instructions")
        return True

    def get_instructions(self):
        return self.__instructions

    # -----------------------
    def set_dialog(self, status, askage=False, askgender=False, askglasses=False, askeyecolor=False):
        self.__dia_is_active = format_bool(state=status, var_name=u"dialog state")
        self.__dia_ask_age = format_bool(state=askage, var_name=u"ask age state")
        self.__dia_ask_gender = format_bool(state=askgender, var_name=u"ask gender state")
        self.__dia_ask_glasses = format_bool(state=askglasses, var_name=u"ask glasses state")
        self.__dia_ask_eye_color = format_bool(state=askeyecolor, var_name=u"ask eye color state")
        return True

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
        self.__con_need_space = format_bool(state=status, var_name=u"use space status")
        return True

    def is_space_start(self):
        return self.__con_need_space

    # -----------------------
    def set_random(self, status):
        self.__con_is_random = format_bool(state=status, var_name=u"use random sequence status")
        return True

    def is_random(self):
        return self.__con_is_random

    # -----------------------
    def set_rest_conf(self, status, period=1, time=1.0):
        self.__con_is_rest = format_bool(state=status, var_name=u"include rest status")
        self.__con_rest_period = format_int(value=period, vmin=1, vmax=9999, var_name=u"rest period")
        self.__con_rest_time = format_float(value=time, vmin=1.0, vmax=9999.0, var_name=u"rest_time")
        return True

    def is_rest(self):
        return self.__con_is_rest

    def get_rest_period(self):
        return self.__con_rest_period

    def get_rest_time(self):
        return self.__con_rest_time

    # =================================
    def load(self, code):
        code = format_text(text=code, lmin=3, lmax=10, var_name=u"code")
        if self.__database:
            sql = u"""
            select
            exp.exp_name, exp.exp_version, exp.exp_description, exp.exp_instructions, exp.exp_comments, 
            exp.exp_date_creation, exp.exp_date_update, 
            dia.dia_is_active, dia.dia_ask_age, dia.dia_ask_gender, dia.dia_ask_glasses, dia.dia_ask_eye_color, 
            con.con_need_space, con.con_is_random, con.con_is_rest, con.con_rest_period, con.con_rest_time 
            from experiment as exp
            inner join exp_dia as dia on exp.exp_code=dia.exp_code
            inner join exp_con as con on exp.exp_code=con.exp_code
            where exp.exp_code='{0}';
            """.format(code)
            exp_res = self.__database.pull_query(query=sql)
            if exp_res is not None:
                self.__in_db = True
                self.__code = code
                self.__name = unicode(exp_res[0, 0])
                self.__version = unicode(exp_res[0, 1])
                self.__description = unicode(exp_res[0, 2])
                self.__instructions = unicode(exp_res[0, 3])
                self.__comments = unicode(exp_res[0, 4])
                self.__date_created = get_time(exp_res[0, 5])
                self.__date_updated = get_time(exp_res[0, 6])
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
        if self.__database is not None and self.__code != u"" and self.__name != u"":
            if self.__in_db:
                sql = u"""
                update experiment set
                exp_name='{1}', exp_version='{2}', exp_description='{3}', exp_instructions='{4}', exp_comments='{5}' 
                where exp_code='{0}';
                update exp_dia set 
                dia_is_active='{6:x}', dia_ask_age='{7:x}', dia_ask_gender='{8:x}', dia_ask_glasses='{9:x}', 
                dia_ask_eye_color='{10:x}'
                where exp_code='{0}';
                update exp_con set 
                con_need_space='{11:x}', con_is_random='{12:x}', con_is_rest='{13:x}', con_rest_period='{14}', 
                con_rest_time='{15}'
                where exp_code='{0}';
                """.format(
                    self.__code, self.__name, self.__version, self.__description, self.__instructions, self.__comments,
                    self.__dia_is_active, self.__dia_ask_age, self.__dia_ask_gender, self.__dia_ask_glasses,
                    self.__dia_ask_eye_color, self.__con_need_space, self.__con_is_random, self.__con_is_rest,
                    self.__con_rest_period, self.__con_rest_time
                )
            else:
                sql = u"""
                insert into experiment 
                (exp_code, exp_name, exp_version, exp_description, exp_comments, exp_instructions)
                values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');
                insert into exp_dia
                (exp_code, dia_is_active, dia_ask_age, dia_ask_gender, dia_ask_glasses, dia_ask_eye_color)
                values ('{0}', '{6:x}', '{7:x}', '{8:x}', '{9:x}', '{10:x}');
                insert into exp_con
                (exp_code, con_need_space, con_is_random, con_is_rest, con_rest_period, con_rest_time)
                values ('{0}', '{11:x}', '{12:x}', '{13:x}', '{14}', '{15}');
                """.format(
                    self.__code, self.__name, self.__version, self.__description, self.__comments, self.__instructions,
                    self.__dia_is_active, self.__dia_ask_age, self.__dia_ask_gender, self.__dia_ask_glasses,
                    self.__dia_ask_eye_color, self.__con_need_space, self.__con_is_random, self.__con_is_rest,
                    self.__con_rest_period, self.__con_rest_time
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
            sql = u"delete from experiment where exp_code='{0}';".format(self.__code)
            exp_res = self.__database.push_query(query=sql)
            self.__in_db = not exp_res
            return exp_res
        return False

    # =================================
    def __load_tests(self):
        test_list = Test.get_list(db=self.__database, exp=self.__code)
        if not test_list:
            return
        for test in test_list:
            new_test = Test()
            new_test.load(db=self.__database, exp=self.__code, tes=int(test[0]))
            self.item_add(item=new_test)
        sql = u"""
        select tes_index, tes_quantity 
        from exp_seq
        where exp_code='{0}'
        order by seq_index asc;
        """.format(self.__code)
        seq_res = self.__database.pull_query(query=sql)
        if seq_res is not None:
            for item in seq_res:
                self.sequence_add(int(item[0]), int(item[1]))

    def __save_tests(self):
        self.__database.push_query(query=u"delete from test where exp_code='{0}';".format(self.__code))
        if not self._item_dat:
            return
        for test in self._item_dat:
            index = self._item_dat.index(test)
            test.save(db=self.__database, exp=self.__code, tes=index)
        seq_index = 0
        sql = u"""
        insert into exp_seq 
        (exp_code, tes_index, seq_index, tes_quantity)
        values ('{0}', '{1}', '{2}', '{3}');
        """
        for item in self._item_seq:
            tes_index = self._item_dat.index(item[0])
            self.__database.push_query(query=sql.format(self.__code, tes_index, seq_index, item[1]))
            seq_index += 1

    # =================================
    def get_iohub(self):
        if self.__in_db:
            experiment = {
                u"title":                       self.__name,
                u"code":                        self.__code,
                u"version":                     self.__version,
                u"description":                 self.__description,
                u"display_experiment_dialog":   True,
                u"session_defaults": {
                    u"name":                    u"Session...",
                    u"code":                    0,
                    u"comments":                self.__comments,
                },
                u"display_session_dialog":      True,
                u"session_variable_order":      [u"name", u"code", u"comments"],
                u"ioHub": {
                    u"enable":                  True,
                },
            }
            if self.__dia_is_active:
                experiment[u"session_defaults"][u"user_variables"] = {}
                if self.__dia_ask_age:
                    experiment[u"session_defaults"][u"user_variables"][u"participant_age"] = u"Unknown"
                    experiment[u"session_variable_order"].append(u"participant_age")
                if self.__dia_ask_gender:
                    experiment[u"session_defaults"][u"user_variables"][u"participant_gender"] = [u"Male", u"Female"]
                    experiment[u"session_variable_order"].append(u"participant_gender")
                if self.__dia_ask_glasses:
                    experiment[u"session_defaults"][u"user_variables"][u"glasses"] = [u"Yes", u"No"]
                    experiment[u"session_defaults"][u"user_variables"][u"contacts"] = [u"Yes", u"No"]
                    experiment[u"session_variable_order"].append(u"glasses")
                    experiment[u"session_variable_order"].append(u"contacts")
                if self.__dia_ask_eye_color:
                    experiment[u"session_defaults"][u"user_variables"][u"eye_color"] = u"Unknown"
                    experiment[u"session_variable_order"].append(u"eye_color")
            return experiment
        return None

    def get_execution(self, win):
        import numpy as np
        if not (isinstance(win, visual.Window) and self.__in_db):
            return None
        experiment = {
            u"instructions":    self.__instructions,
            u"space_start":     self.__con_need_space,
            u"rest": {
                u"active":      self.__con_is_rest,
                u"period":      self.__con_rest_period,
                u"time":        self.__con_rest_time,
            },
            u"test_data":       [item.get_execution(win=win) for item in self._item_dat],
            u"test_sequence":   []
        }
        for item in self._item_seq:
            test = item[0]
            quantity = item[1]
            if test.get_items():
                index = self._item_dat.index(test)
                experiment[u"test_sequence"].append(index*np.full(shape=(quantity, 1), fill_value=1, dtype=int))
        experiment[u"test_sequence"] = np.concatenate(experiment[u"test_sequence"])
        if self.__con_is_random:
            np.random.shuffle(experiment[u"test_sequence"])
        return experiment

    def get_configuration(self):
        if self.__in_db:
            experiment = {
                u"title":                   self.__name,
                u"code":                    self.__code,
                u"version":                 self.__version,
                u"description":             self.__description,
                u"instructions":            self.__instructions,
                u"session_configuration": {
                    u"comments":            self.__comments,
                    u"space_start":         self.__con_need_space,
                    u"randomize":           self.__con_is_random,
                    u"rest": {
                        u"active":          self.__con_is_rest,
                        u"period":          self.__con_rest_period,
                        u"time":            self.__con_rest_time,
                    },
                    u"dialog": {
                        u"active":          self.__dia_is_active,
                        u"ask_age":         self.__dia_ask_age,
                        u"ask_gender":      self.__dia_ask_gender,
                        u"ask_glasses":     self.__dia_ask_glasses,
                        u"ask_eye_color":   self.__dia_ask_eye_color,
                    }
                },
                u"tests":                   [item.get_configuration() for item in self._item_dat],
                u"sequence":                [[self._item_dat.index(item[0]), item[1]] for item in self._item_seq]
            }
            return experiment
        return None
