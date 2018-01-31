# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import copy
import numpy as np
from psychopy import visual, colors
from saccadeApp import saccadedb, time


# =============================================================================
# Class: Utils
# =============================================================================
class Utils(object):
    # =================================
    def __init__(self):
        pass

    # =================================
    @staticmethod
    def ftext(word, lmin=0, lmax=-1):
        try:
            temp = unicode(word)
            if lmax <= lmin <= len(temp) or lmin <= len(temp) <= lmax:
                return temp
            else:
                return u''
        except ValueError:
            return u''

    @staticmethod
    def fint(value, vmin=0, default=None):
        try:
            temp = int(value)
            if temp >= vmin:
                return temp
            else:
                return default
        except ValueError:
            return default

    @staticmethod
    def ffloat(value, vmin=0.0, default=None):
        try:
            temp = float(value)
            if temp >= vmin:
                return temp
            else:
                return default
        except ValueError:
            return default

    @staticmethod
    def fbool(state, default=False):
        try:
            temp = bool(state)
            return temp
        except ValueError:
            return default


# =============================================================================
# Class type: ItemList
# =============================================================================
class ItemList(object):
    # =================================
    def __init__(self, itemclass):
        self._item_cls = itemclass
        self._item_arr = None

    # =================================
    def _item_add(self, item):
        if isinstance(item, self._item_cls):
            itm_num = self._item_number()
            if itm_num is None:
                self._item_arr = np.array([item], dtype=self._item_cls)
            else:
                self._item_arr = np.insert(arr=self._item_arr, obj=itm_num, values=[item], axis=0)
            return True
        else:
            return False

    def _item_copy(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            new_itm = self._item_arr[index].copy()
            return self._item_add(item=new_itm)
        else:
            return False

    def _item_delete(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            self._item_arr = np.delete(arr=self._item_arr, obj=index, axis=0) if itm_num > 1 else None
            return True
        else:
            return False

    def _item_move_up(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 < index < itm_num:
            temp = self._item_arr[index-1]
            self._item_arr[index-1] = self._item_arr[index]
            self._item_arr[index] = temp
            return True
        else:
            return False

    def _item_move_down(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num-1:
            temp = self._item_arr[index+1]
            self._item_arr[index+1] = self._item_arr[index]
            self._item_arr[index] = temp
            return True
        else:
            return False

    def _item_get_by_index(self, index):
        itm_num = self._item_number()
        if itm_num is not None and 0 <= index < itm_num:
            return self._item_arr[index]
        else:
            return None

    def _item_number(self):
        if self._item_arr is not None:
            return len(self._item_arr)
        else:
            return None


# =============================================================================
# Class: Component
# =============================================================================
class Component(object):
    # =================================
    def __init__(self):
        self.__name = u'unnamed'
        self.__unit = u'deg'
        self.__pos = (0.0, 0.0)
        self.__ori = 0.0
        self.__size = 0.0
        # -------------------
        self.__fimg = False
        self.__imag = None
        self.__shpe = u'square'
        self.__colr = u'white'

    # =================================
    @classmethod
    def get_list(cls, db, exp, tes, fra):
        sql = u"""
        select com_indx, com_name, com_shpe
        from component
        where exp_code='%s' and tes_indx='%d' and fra_indx='%d'
        order by com_indx asc
        """ % (exp, tes, fra)
        return db.pull_query(query=sql)

    # =================================
    def set_name(self, name):
        name = Utils.ftext(name, lmin=3)
        if name != u'':
            self.__name = name
            return True
        else:
            return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_units(self, units):
        units = Utils.ftext(units)
        if units in [u'norm', u'cm', u'deg', u'degFlat', u'degFlatPos', u'pix']:
            self.__unit = units
            return True
        else:
            return False

    def get_units(self):
        return self.__unit

    # -----------------------
    def set_pos(self, posx, posy):
        posx = Utils.ffloat(posx)
        posy = Utils.ffloat(posy)
        if posx is not None and posy is not None:
            self.__pos = (posx, posy)
            return True
        else:
            return False

    def get_pos(self):
        return self.__pos

    # -----------------------
    def set_orientation(self, ori):
        ori = Utils.ffloat(ori)
        if ori is not None:
            self.__ori = ori
            return True
        else:
            return False

    def get_orientation(self):
        return self.__ori

    # -----------------------
    def set_size(self, size):
        size = Utils.ffloat(size)
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
        imagepath = Utils.ftext(imagepath)
        if imagepath is not u'' and os.path.isfile(imagepath):
            self.__fimg = True
            self.__shpe = u'image'
            self.__imag = Image.open(imagepath)
            return True
        else:
            return False

    def get_image(self):
        return self.__imag

    # -----------------------
    def set_shape(self, shape):
        shape = Utils.ftext(shape)
        if shape in [u'arrow', u'circle', u'cross', u'gauss', u'square']:
            self.__fimg = False
            self.__shpe = shape
            return True
        else:
            return False

    def get_shape(self):
        return self.__shpe

    # -----------------------
    def set_color(self, color):
        color = Utils.ftext(color)
        if colors.isValidColor(color):
            self.__colr = color
            return True
        else:
            return False

    def get_color(self):
        return self.__colr

    # =================================
    def __decode_image(self, encimg):
        from PIL import Image
        from io import BytesIO
        # -------------------
        coded = Utils.ftext(encimg)
        if coded != u'':
            try:
                img_buff = BytesIO()
                img_buff.write(coded.decode(u'base64'))
                # -----------
                self.__fimg = True
                self.__imag = Image.open(img_buff)
            except:
                return False
        else:
            return False

    def __encode_image(self):
        from io import BytesIO
        # -------------------
        if self.__imag is not None:
            img_buff = BytesIO()
            self.__imag.save(img_buff, u'PNG')
            return img_buff.getvalue().encode(u'base64')
        else:
            return u''

    # =================================
    def load(self, db, exp, tes, fra, com):
        sql = u"""
        select
        com_name, com_unit, com_posx, com_posy, com_orie, com_size, com_fimg, com_imag, com_shpe, com_colr
        from component
        where exp_code='%s' and tes_indx='%d' and fra_indx='%d' and com_indx='%d'
        """ % (exp, tes, fra, com)
        com_res = db.pull_query(query=sql)
        # -------------------
        if com_res is not None:
            print u"Exp %s, Tes %d, Fra %d: Component %d loaded." % (exp, tes, fra, com)
            # ---------------
            self.__name = unicode(com_res[0, 0])
            self.__unit = unicode(com_res[0, 1])
            self.__pos = (float(com_res[0, 2]),
                          float(com_res[0, 3]))
            self.__ori = float(com_res[0, 4])
            self.__size = float(com_res[0, 5])
            self.__fimg = bool(int(com_res[0, 6]))
            self.__imag = self.__decode_image(unicode(com_res[0, 7]))
            self.__shpe = unicode(com_res[0, 8])
            self.__colr = unicode(com_res[0, 9])
            # ---------------
            return True
        else:
            print u"Exp %s, Tes %d, Fra %d: Component %d doesn't exists." % (exp, tes, fra, com)
            return False

    def save(self, db, exp, tes, fra, com):
        sql = u"""
        insert into component
        (exp_code, tes_indx, fra_indx, com_indx, 
        com_name, com_unit, com_posx, com_posy, com_orie, com_size, 
        com_fimg, com_imag, com_shpe, com_colr)
        values ('%s', '%d', '%d', '%d', '%s', '%s', '%f', '%f', '%f', '%f', '%x', '%s', '%s', '%s')
        """ % (
            exp, tes, fra, com,
            self.__name, self.__unit, self.__pos[0], self.__pos[1], self.__ori, self.__size,
            self.__fimg, self.__encode_image(), self.__shpe, self.__colr
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


# =============================================================================
# Class: Frame (child of ItemList)
# =============================================================================
class Frame(ItemList):
    # =================================
    def __init__(self):
        super(Frame, self).__init__(itemclass=Component)
        # -------------------
        self.__name = u'unnamed'
        self.__colr = u'black'
        self.__task = False
        self.__time = 0.0
        self.__keya = u''
        self.__keys = u''

    # =================================
    @classmethod
    def get_list(cls, db, exp, tes):
        sql = u"""
        select fra_indx, fra_name
        from frame
        where exp_code='%s' and tes_indx='%d'
        order by fra_indx asc
        """ % (exp, tes)
        return db.pull_query(query=sql)

    # =================================
    def set_name(self, name):
        name = Utils.ftext(name, lmin=3)
        if name != u'':
            self.__name = name
            return True
        else:
            return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_color(self, color):
        color = Utils.ftext(color)
        if colors.isValidColor(color):
            self.__colr = color
            return True
        else:
            return False

    def get_color(self):
        return self.__colr

    # -----------------------
    def set_as_task(self, state):
        self.__task = Utils.fbool(state, default=self.__task)
        if self.__task:
            self.__time = 0.0
            return True
        else:
            self.__keya = u''
            self.__keys = u''
            return False

    def get_state(self):
        return self.__task

    # -----------------------
    def set_time(self, value):
        value = Utils.ffloat(value)
        if not self.__task and value is not None:
            self.__time = value
            return True
        else:
            self.__time = 0.0
            return False

    def get_time(self):
        return self.__time

    # -----------------------
    def set_keys_allowed(self, keys):
        keys = Utils.ftext(keys).replace(unicode(u' '), unicode(u''))
        if self.__task and keys != u'':
            self.__keya = keys
            return True
        else:
            self.__keya = u''
            return False

    def get_keys_allowed(self):
        return self.__keya

    # -----------------------
    def set_keys_selected(self, keys):
        keys = Utils.ftext(keys).replace(unicode(u' '), unicode(u''))
        keys.replace(u" ", u"")
        if self.__task and self.__keya != u'' and keys != u'':
            keys_alw = self.__keya.split(u',')
            keys_sel = keys.split(u',')
            # ---------------
            match = [key for key in keys_sel if key in keys_alw]
            if len(match) == len(keys_sel):
                self.__keys = keys
                return True
            else:
                self.__keys = u''
                return True
        else:
            self.__keys = u''
            return False

    def get_keys_selected(self):
        return self.__keys

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
        return self._item_arr

    def component_number(self):
        return self._item_number()

    # =================================
    def load(self, db, exp, tes, fra):
        sql = u"""
        select
        fra_name, fra_colr, fra_task, fra_time, fra_keya, fra_keys
        from frame
        where exp_code='%s' and tes_indx='%d' and fra_indx='%d'
        """ % (exp, tes, fra)
        fra_res = db.pull_query(query=sql)
        # -------------------
        if fra_res is not None:
            print u"Exp %s, Tes %d: Frame %d loaded." % (exp, tes, fra)
            # ---------------
            self.__name = unicode(fra_res[0, 0])
            self.__colr = unicode(fra_res[0, 1])
            self.__task = bool(int(fra_res[0, 2]))
            self.__time = float(fra_res[0, 3])
            self.__keya = unicode(fra_res[0, 4])
            self.__keys = unicode(fra_res[0, 5])
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
        (exp_code, tes_indx, fra_indx, 
        fra_name, fra_colr, fra_task, fra_time, fra_keya, fra_keys)
        values ('%s', '%d', '%d', '%s', '%s', '%x', '%f', '%s', '%s')
        """ % (
            exp, tes, fra,
            self.__name, self.__colr, self.__task, self.__time, self.__keya, self.__keys
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
                new_com.load(db=db, exp=exp, tes=tes, fra=fra, com=com[0])
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


# =============================================================================
# Class: Test (child of ItemList)
# =============================================================================
class Test(ItemList):
    # =================================
    def __init__(self):
        super(Test, self).__init__(itemclass=Frame)
        # -------------------
        self.__name = u'unnamed'
        self.__desc = u''
        self.__reps = 0

    # =================================
    @classmethod
    def get_list(cls, db, exp):
        sql = u"""
        select tes_indx, tes_name, tes_reps
        from test
        where exp_code='%s'
        order by tes_indx asc
        """ % exp
        return db.pull_query(query=sql)

    # =================================
    def set_name(self, name):
        name = Utils.ftext(name, lmin=3)
        if name != u'':
            self.__name = name
            return True
        else:
            return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_description(self, text):
        text = Utils.ftext(text)
        if text != u'':
            self.__desc = text
            return True
        else:
            return False

    def get_description(self):
        return self.__desc

    # -----------------------
    def set_repetitions(self, value):
        value = Utils.fint(value, vmin=1)
        if value is not None:
            self.__reps = value
            return True
        else:
            return False

    def get_repetitions(self):
        return self.__reps

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
        return self._item_arr

    def frame_number(self):
        return self._item_number()

    # =================================
    def load(self, db, exp, tes):
        sql = u"""
        select
        tes_name, tes_desc, tes_reps
        from test
        where exp_code='%s' and tes_indx='%d'
        """ % (exp, tes)
        tes_res = db.pull_query(query=sql)
        # -------------------
        if tes_res is not None:
            print u"Exp %s: Test %d loaded." % (exp, tes)
            # ---------------
            self.__name = unicode(tes_res[0, 0])
            self.__desc = unicode(tes_res[0, 1])
            self.__reps = int(tes_res[0, 2])
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
        (exp_code, tes_indx, tes_name, tes_desc, tes_reps) 
        values ('%s', '%d', '%s', '%s', '%d')
        """ % (
            exp, tes,
            self.__name, self.__desc, self.__reps
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
                new_fra.load(db=db, exp=exp, tes=tes, fra=fra[0])
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
        self.__name = u'unnamed'
        self.__vers = u''
        self.__comm = u''
        self.__desc = u''
        # -------------------
        self.__datc = u'Not available'
        self.__datu = u'Not available'
        # -------------------
        self.__dia_fact = True
        self.__dia_fage = True
        self.__dia_fgen = True
        self.__dia_fgla = True
        self.__dia_feye = True
        # -------------------
        self.__con_fspc = False
        self.__con_frnd = False
        self.__con_frst = False
        self.__con_reps = 0
        self.__con_time = 0.0

    # =================================
    @classmethod
    def get_experiment_list(cls, db):
        sql = u"""
        select exp_code, exp_name, exp_vers
        from experiment
        order by exp_name asc
        """
        return db.pull_query(query=sql)

    # =================================
    def set_database(self, db):
        if isinstance(db, saccadedb):
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
        code = Utils.ftext(code, lmin=3, lmax=10)
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
        name = Utils.ftext(name, lmin=3, lmax=50)
        version = Utils.ftext(version, lmin=3, lmax=10)
        if self.__database is not None and name != u'' and version != u'':
            sql = u"select * from experiment where exp_name='%s' and exp_vers='%s';" % (name, version)
            exp_res = self.__database.pull_query(query=sql)
            # ---------------
            if exp_res is None:
                self.__name = name
                self.__vers = version
                return True
            else:
                return False
        else:
            return False

    def get_name(self):
        return self.__name

    def get_version(self):
        return self.__vers

    # -----------------------
    def set_descripton(self, text):
        text = Utils.ftext(text)
        if text != u'':
            self.__desc = text
            return True
        else:
            return False

    def get_description(self):
        return self.__desc

    # -----------------------
    def set_comment(self, text):
        text = Utils.ftext(text)
        if text != u'':
            self.__comm = text
            return True
        else:
            return False

    def get_comment(self):
        return self.__comm

    # -----------------------
    def set_dialog(self, status, askage, askgender, askglasses, askeyecolor):
        self.__dia_fact = Utils.fbool(status, default=self.__dia_fact)
        self.__dia_fage = Utils.fbool(askage, default=self.__dia_fage)
        self.__dia_fgen = Utils.fbool(askgender, default=self.__dia_fgen)
        self.__dia_fgla = Utils.fbool(askglasses, default=self.__dia_fgla)
        self.__dia_feye = Utils.fbool(askeyecolor, default=self.__dia_feye)

    def is_dialog_active(self):
        return self.__dia_fact

    def is_ask_age(self):
        return self.__dia_fage

    def is_ask_gender(self):
        return self.__dia_fgen

    def is_ask_glasses(self):
        return self.__dia_fgla

    def is_ask_eye_color(self):
        return self.__dia_feye

    # -----------------------
    def set_space_start(self, status):
        self.__con_fspc = Utils.fbool(status, default=self.__con_fspc)

    def is_space_start(self):
        return self.__con_fspc

    # -----------------------
    def set_random(self, status):
        self.__con_frnd = Utils.fbool(status, default=self.__con_frnd)

    def is_random(self):
        return self.__con_frnd

    # -----------------------
    def set_rest_conf(self, status, period, time):
        status = Utils.fbool(status, default=self.__con_frst)
        period = Utils.fint(period, default=-0)
        time = Utils.ffloat(time, default=-0.0)
        if status and period > 0 and time > 0.0:
            self.__con_frst = status
            self.__con_reps = period
            self.__con_time = time
            return True
        else:
            return False

    def is_rest(self):
        return self.__con_frst

    def get_rest_period(self):
        return self.__con_reps

    def get_rest_time(self):
        return self.__con_time

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
        return self._item_arr

    def test_number(self):
        return self._item_number()

    # =================================
    def load(self, code):
        code = Utils.ftext(code, lmin=3, lmax=10)
        if self.__database is not None and code != u'':
            sql = u"""
            select
            exp.exp_name, exp.exp_vers, exp.exp_desc, exp.exp_comm, exp.exp_datc, exp_datu, 
            dia.dia_fact, dia.dia_fage, dia.dia_fgen, dia.dia_fgla, dia.dia_feye, 
            con.con_fspc, con.con_frnd, con.con_frst, con.con_reps, con.con_time 
            from experiment as exp
            inner join exp_dia as dia on exp.exp_code=dia.exp_code
            inner join exp_con as con on exp.exp_code=con.exp_code
            where exp.exp_code='%s'
            """ % code
            exp_res = self.__database.pull_query(query=sql)
            # ---------------
            if exp_res is not None:
                self.__in_db = True
                self.__code = code
                print u"Experiment %s loaded." % self.__code
                # -----------
                self.__name = unicode(exp_res[0, 0])
                self.__vers = unicode(exp_res[0, 1])
                self.__desc = unicode(exp_res[0, 2])
                self.__comm = unicode(exp_res[0, 3])
                self.__datc = time(exp_res[0, 4])
                self.__datu = time(exp_res[0, 5])
                self.__dia_fact = bool(int(exp_res[0, 6]))
                self.__dia_fage = bool(int(exp_res[0, 7]))
                self.__dia_fgen = bool(int(exp_res[0, 8]))
                self.__dia_fgla = bool(int(exp_res[0, 9]))
                self.__dia_feye = bool(int(exp_res[0, 10]))
                self.__con_fspc = bool(int(exp_res[0, 11]))
                self.__con_frnd = bool(int(exp_res[0, 12]))
                self.__con_frst = bool(int(exp_res[0, 13]))
                self.__con_reps = int(exp_res[0, 14])
                self.__con_time = float(exp_res[0, 15])
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
                exp_name='%s', exp_vers='%s', exp_desc='%s', exp_comm='%s'
                where exp_code='%s';
                update exp_dia set 
                dia_fact='%x', dia_fage='%x', dia_fgen='%x', dia_fgla='%x', dia_feye='%x'
                where exp_code='%s';
                update exp_con set 
                con_fspc='%x', con_frnd='%x', con_frst='%x', con_reps='%d', con_time='%f'
                where exp_code='%s';
                """ % (
                    self.__name, self.__vers, self.__desc, self.__comm, self.__code,
                    self.__dia_fact, self.__dia_fage, self.__dia_fgen, self.__dia_fgla, self.__dia_feye, self.__code,
                    self.__con_fspc, self.__con_frnd, self.__con_frst, self.__con_reps, self.__con_time, self.__code
                )
            else:
                sql = u"""
                insert into experiment 
                (exp_code, exp_name, exp_vers, exp_desc, exp_comm)
                values ('%s', '%s', '%s', '%s', '%s');
                insert into exp_dia
                (exp_code, dia_fact, dia_fage, dia_fgen, dia_fgla, dia_feye)
                values ('%s', '%x', '%x', '%x', '%x', '%x');
                insert into exp_con
                (exp_code, con_fspc, con_frnd, con_frst, con_reps, con_time)
                values ('%s', '%x', '%x', '%x', '%d', '%f');
                """ % (
                    self.__code, self.__name, self.__vers, self.__desc, self.__comm,
                    self.__code, self.__dia_fact, self.__dia_fage, self.__dia_fgen, self.__dia_fgla, self.__dia_feye,
                    self.__code, self.__con_fspc, self.__con_frnd, self.__con_frst, self.__con_reps, self.__con_time
                )
            exp_res = self.__database.push_query(query=sql)
            # ---------------
            if exp_res:
                print u"Experiment %s saved. Saving tests..." % self.__code
                self.__save_tests()
            else:
                print u"Experiment %s not saved." % self.__code
            # ---------------
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

    # =================================
    def __load_tests(self):
        tes_lst = Test.get_list(db=self.__database, exp=self.__code)
        if tes_lst is not None:
            for tes in tes_lst:
                new_tes = Test()
                new_tes.load(db=self.__database, exp=self.__code, tes=tes[0])
                self.test_add(item=new_tes)
        else:
            print u"Experiment %s don't have any test saved on the DB." % self.__code

    def __save_tests(self):
        sql = u"delete from test where exp_code='%s'" % self.__code
        self.__database.push_query(query=sql)
        # -------------------
        tes_num = self.test_number()
        if tes_num is not None:
            for index in range(tes_num):
                self.test_get_by_index(index=index).save(db=self.__database, exp=self.__code, tes=index)
        else:
            print u"Experiment %s don't have any test to be saved." % self.__code
