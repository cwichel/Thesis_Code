# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import copy
import numpy as np
from PIL import Image
from psychopy import visual, colors
from saccadeApp import saccadedb, time


# =============================================================================
# Constants
# =============================================================================
MIN_COD_LEN = 2
MAX_COD_LEN = 10
MIN_VER_LEN = 2
MAX_VER_LEN = 10
MIN_TIT_LEN = 5
MAX_TIT_LEN = 100


def get_unicode(word, w_min=0, w_max=None, default=u''):
    if isinstance(w_max, int):
        if isinstance(word, (unicode, str)) and w_min <= len(word) <= w_max:
            return unicode(word)
        else:
            return default
    else:
        if isinstance(word, (unicode, str)) and w_min <= len(word):
            return unicode(word)
        else:
            return default


def get_integer(value, default=0):
    if isinstance(value, (int, long, float)):
        return int(value)
    else:
        return default


def get_float(value, default=0.0):
    if isinstance(value, (int, long, float)):
        return float(value)
    else:
        return default


def get_boolean(state, default=False):
    if isinstance(state, (bool, int)):
        return bool(state)
    else:
        return default


# =============================================================================
# Experiment Class
# =============================================================================
class experiment(object):
    def __init__(self):
        self.__in_db = False
        self.__database = None
        # -------------------
        self.__code = None
        self.__title = None
        self.__version = None
        self.__comment = None
        self.__description = None
        # -------------------
        self.__date_create = None
        self.__date_update = None
        # -------------------
        self.__dia_enable = True
        self.__dia_ask_age = True
        self.__dia_ask_gender = True
        self.__dia_ask_glasses = True
        self.__dia_ask_eye_color = True
        # -------------------
        self.__space_start = False
        self.__is_rand = False
        self.__is_rest = False
        self.__rest_test = 0
        self.__rest_time = 0.0
        # -------------------
        self.__test_arr = None

    @property
    def description(self):
        exp_desc = u"""
        #=======================================#
        Experiment:
            - on database   : %s.
            - date (cre/upd): %s / %s
            -------------------------------------
            - code          : %s.
            - title         : %s.
            - version       : %s.
            -------------------------------------
            - description   : %s.
            - comments      : %s.
            -------------------------------------
            - dialog        : %s.
                - age       : %s.
                - gender    : %s.
                - glasses   : %s.
                - eye color : %s.                
            -------------------------------------
            - space to start: %s.
            - random        : %s.
            - rest          : %s.
                - period    : %d.  
                - time      : %f.
            -------------------------------------
        """ % (
            self.__in_db, self.__date_create, self.__date_update,
            self.__code, self.__title, self.__version,
            self.__description, self.__comment,
            self.__dia_enable,
            self.__dia_ask_age, self.__dia_ask_gender, self.__dia_ask_glasses, self.__dia_ask_eye_color,
            self.__space_start, self.__is_rand,
            self.__is_rest,
            self.__rest_test, self.__rest_time
            )
        # -------------------
        tes_cnt = self.test_count()
        if tes_cnt is not None:
            exp_tes = u"""
            - test number   : %d.
                    code        quantity
            """ % tes_cnt
            exp_desc += exp_tes
            # ---------------
            exp_tes_iter = u"""
                    %s          %d
            """
            for index in range(tes_cnt):
                item = self.test_get(index)
                exp_desc += exp_tes_iter % (item[0].get_code(), item[1])
        else:
            exp_desc += u"""
            - Test list not available!!
            """

        return exp_desc

    # =================================
    def load(self, code):
        code = get_unicode(code, MIN_COD_LEN, MAX_COD_LEN)
        # ------------------
        if self.__database is not None and code is not None:
            sql = u"""
            select
            exp.exp_title, exp.exp_version, exp.exp_comment, exp.exp_description, exp.exp_date_create, 
            exp.exp_date_update, dia.dia_enable, dia.dia_ask_age, dia.dia_ask_gender, dia.dia_ask_glasses, 
            dia.dia_ask_eye_color, con.con_space_start, con.con_is_rand, con.con_is_rest, con.con_rest_test, 
            con.con_rest_time 
            from experiment as exp
            inner join exp_dia as dia on exp.exp_code=dia.exp_code
            inner join exp_con as con on exp.exp_code=con.exp_code
            where exp.exp_code='%s'
            """ % code
            # ---------------
            res = self.__database.pull_query(query=sql)
            # ---------------
            if res is not None:
                self.__code = code
                self.__in_db = True
                self.__title = unicode(res[0, 0])
                self.__version = unicode(res[0, 1])
                self.__comment = unicode(res[0, 2])
                self.__description = unicode(res[0, 3])
                self.__date_create = time(res[0, 4])
                self.__date_update = time(res[0, 5])
                self.__dia_enable = bool(int(res[0, 6]))
                self.__dia_ask_age = bool(int(res[0, 7]))
                self.__dia_ask_gender = bool(int(res[0, 8]))
                self.__dia_ask_glasses = bool(int(res[0, 9]))
                self.__dia_ask_eye_color = bool(int(res[0, 10]))
                self.__space_start = bool(int(res[0, 11]))
                self.__is_rand = bool(int(res[0, 12]))
                self.__is_rest = bool(int(res[0, 13]))
                self.__rest_test = int(res[0, 14])
                self.__rest_time = float(res[0, 15])
                # -----------
                self.__test_load()
                # -----------
                return True
            else:
                return False
        else:
            return False

    def save(self):
        if self.__database is not None and self.__code is not None and self.__title is not None:
            if self.__in_db:
                sql = u"""
                update experiment set 
                exp_title='%s', exp_version='%s', exp_description='%s', exp_comment='%s'
                where exp_code='%s';
                update exp_dia set 
                dia_enable='%x', dia_ask_age='%x', dia_ask_gender='%x', dia_ask_glasses='%x', dia_ask_eye_color='%x'
                where exp_code='%s';
                update exp_con set 
                con_space_start='%x', con_is_rand='%x', con_is_rest='%x', con_rest_test='%d', con_rest_time='%f'
                where exp_code='%s';
                """
                sql %= (
                    self.__title, self.__version, self.__description, self.__comment, self.__code,
                    self.__dia_enable, self.__dia_ask_age, self.__dia_ask_gender, self.__dia_ask_glasses,
                    self.__dia_ask_eye_color, self.__code,
                    self.__space_start, self.__is_rand, self.__is_rest, self.__rest_test, self.__rest_time, self.__code
                )
            else:
                sql = u"""
                insert into experiment 
                (exp_code, exp_title, exp_version, exp_description, exp_comment)
                values ('%s', '%s', '%s', '%s', '%s');
                insert into exp_dia
                (exp_code, dia_enable, dia_ask_age, dia_ask_gender, dia_ask_glasses, dia_ask_eye_color)
                values ('%s', '%x', '%x', '%x', '%x', '%x');
                insert into exp_con
                (exp_code, con_space_start, con_is_rand, con_is_rest, con_rest_test, con_rest_time)
                values ('%s', '%x', '%x', '%x', '%d', '%f');
                """
                sql %= (
                    self.__code, self.__title, self.__version, self.__description, self.__comment,
                    self.__code, self.__dia_enable, self.__dia_ask_age, self.__dia_ask_gender, self.__dia_ask_glasses,
                    self.__dia_ask_eye_color,
                    self.__code, self.__space_start, self.__is_rand, self.__is_rest, self.__rest_test, self.__rest_time
                )
            # ---------------
            exp_res = self.__database.push_query(query=sql)
            self.__in_db = exp_res
            # ---------------
            tes_res = self.__test_save() if exp_res else False
            # ---------------
            return tes_res
        else:
            return False

    def copy(self, code, version):
        new_exp = copy.deepcopy(self)
        new_exp.__in_db = False
        # -------------------
        new_exp.set_database(db=self.__database)
        # -------------------
        new_cod_check = new_exp.set_code(code=code)
        new_tit_check = new_exp.set_info(title=self.__title, version=version)
        # -------------------
        if new_cod_check and new_tit_check:
            return new_exp
        else:
            return None

    def remove(self):
        if self.__database and self.__in_db:
            sql = u"delete from experiment where exp_code='%s'" % self.__code
            exp_res = self.__database.push_query(query=sql)
            return exp_res
        else:
            return False

    # =================================
    def set_database(self, db):
        if isinstance(db, saccadedb):
            self.__database = db
            return True
        else:
            return False

    def set_code(self, code):
        code = get_unicode(code, MIN_COD_LEN, MAX_COD_LEN)
        # ------------------
        if self.__database is not None and code is not None:
            sql = u"select * from experiment where exp_code='%s'" % code
            # ---------------
            res = self.__database.pull_query(query=sql)
            # ---------------
            if res is None:
                self.__code = code
                return True
            else:
                return False
        else:
            return False

    def set_info(self, title, version):
        title = get_unicode(title, MIN_TIT_LEN, MAX_TIT_LEN)
        version = get_unicode(version, MIN_VER_LEN, MAX_VER_LEN)
        # ------------------
        if self.__database is not None and title is not None and version is not None:
            sql = u"select * from experiment where exp_title='%s' and exp_version='%s'" % (title, version)
            # ---------------
            res = self.__database.pull_query(query=sql)
            # ---------------
            if res is None:
                self.__title = title
                self.__version = version
                return True
            else:
                return False
        else:
            return False

    def set_comment(self, comment):
        self.__comment = get_unicode(comment)

    def set_description(self, description):
        self.__description = get_unicode(description)

    def set_dialog(self, isactive, askage, askgender, askglasses, askeyecolor):
        self.__dia_enable = get_boolean(isactive, default=self.__dia_enable)
        self.__dia_ask_age = get_boolean(askage, default=self.__dia_ask_age)
        self.__dia_ask_gender = get_boolean(askgender, default=self.__dia_ask_gender)
        self.__dia_ask_glasses = get_boolean(askglasses, default=self.__dia_ask_glasses)
        self.__dia_ask_eye_color = get_boolean(askeyecolor, default=self.__dia_ask_eye_color)

    def set_space_start(self, isactive):
        self.__space_start = get_boolean(isactive, default=self.__space_start)

    def set_random(self, isactive):
        self.__is_rand = get_boolean(isactive, default=self.__is_rand)

    def set_rest(self, isactive, period, resttime):
        self.__is_rest = get_boolean(isactive, default=self.__is_rest)
        self.__rest_test = get_integer(period)
        self.__rest_time = get_float(resttime)

    # -----------------------
    def get_database(self):
        return self.__database

    def get_code(self):
        return self.__code

    def get_title(self):
        return self.__title

    def get_version(self):
        return self.__version

    def get_comment(self):
        return self.__comment

    def get_description(self):
        return self.__description

    def is_dialog(self):
        return self.__dia_enable

    def is_dialog_ask_age(self):
        return self.__dia_ask_age

    def is_dialog_ask_gender(self):
        return self.__dia_ask_gender

    def is_dialog_ask_glasses(self):
        return self.__dia_ask_glasses

    def is_dialog_ask_eye_color(self):
        return self.__dia_ask_eye_color

    def is_space_start(self):
        return self.__space_start

    def is_random(self):
        return self.__is_rand

    def is_rest(self):
        return self.__is_rest

    def get_rest_period(self):
        return self.__rest_test

    def get_rest_time(self):
        return self.__rest_time

    def is_on_db(self):
        return self.__in_db

    # =================================
    def test_new(self, item, reps):
        reps = get_integer(reps)
        if isinstance(item, test) and reps > 0:
            tes_cnt = self.test_count()
            if tes_cnt is None:
                self.__test_arr = np.array([item, reps], dtype=object)
            else:
                self.__test_arr = np.vstack((self.__test_arr, np.array([item, reps], dtype=object)))
            return True
        else:
            return False

    def test_remove(self, index):
        tes_cnt = self.test_count()
        if tes_cnt is not None and 0 <= index < tes_cnt:
            self.__test_arr = np.delete(arr=self.__test_arr, obj=index, axis=0) if tes_cnt > 1 else None
            return True
        else:
            return False

    def test_move_up(self, index):
        tes_cnt = self.test_count()
        if tes_cnt is not None and 0 < index < tes_cnt:
            temp = self.__test_arr[index-1, :]
            self.__test_arr[index-1, :] = self.__test_arr[index]
            self.__test_arr[index] = temp
            return True
        else:
            return False

    def test_move_down(self, index):
        tes_cnt = self.test_count()
        if tes_cnt is not None and 0 <= index < tes_cnt-1:
            temp = self.__test_arr[index+1, :]
            self.__test_arr[index+1, :] = self.__test_arr[index]
            self.__test_arr[index] = temp
            return True
        else:
            return False

    def test_get_all(self):
        return self.__test_arr

    def test_get(self, index):
        tes_cnt = self.test_count()
        if tes_cnt is not None and 0 <= index < tes_cnt:
            if tes_cnt == 1 and index == 0:
                return self.__test_arr
            else:
                return self.__test_arr[index, :]
        else:
            return None

    def test_count(self):
        if self.__test_arr is not None:
            shape = self.__test_arr.shape
            count = shape[0] if len(shape) > 1 else 1
            return count
        else:
            return None

    # =================================
    def __test_load(self):
        if self.__database is not None and self.__in_db:
            sql = u"""
            select tes_code, exp_tes_quantity 
            from exp_tes 
            where exp_code='%s' 
            order by exp_tes_id asc
            """ % self.__code
            tes_res = self.__database.pull_query(query=sql)
            # ---------------
            if tes_res is not None:
                for index in tes_res:
                    new_tes = test()
                    new_tes.set_database(db=self.__database)
                    new_tes.load(code=index[0])
                    self.test_new(item=new_tes, reps=index[1])

    def __test_save(self):
        if self.__database is not None and self.__in_db:
            sql = u"delete from exp_tes where exp_code='%s'" % self.__code
            self.__database.push_query(query=sql)
            # ---------------
            tes_cnt = self.test_count()
            if tes_cnt is not None:
                sql = u"""
                insert into exp_tes
                (tes_code, exp_code, exp_tes_id, exp_tes_quantity)
                values ('%s', '%s', '%d', '%d')
                """
                for index in range(tes_cnt):
                    sql %= (self.__test_arr[index, 0].get_code(), self.__code, index, self.__test_arr[index, 1])
                    self.__database.push_query(query=sql)
            # ---------------
            return True
        else:
            return False


# =============================================================================
# Test Class
# =============================================================================
class test(object):
    def __init__(self):
        self.__in_db = False
        self.__database = None
        # -------------------
        self.__code = None
        self.__title = None
        self.__version = None
        self.__description = None
        # -------------------
        self.__date_create = None
        self.__date_update = None
        # -------------------
        self.__frame_arr = None

    @property
    def description(self):
        tes_desc = u"""
        ===============================
        Test:
            - on database   : %s.
            - date (cre/upd): %s / %s
            -------------------------------------
            - code          : %s.
            - title         : %s.
            - version       : %s.
            -------------------------------------
            - description   : %s.
            -------------------------------------
        """ % (
            self.__in_db, self.__date_create, self.__date_update,
            self.__code, self.__title, self.__version,
            self.__description,
            )
        # -------------------
        fra_cnt = self.frame_count()
        if fra_cnt is not None:
            tes_fra = u"""
            - frame number  : %d.
            """ % fra_cnt
            tes_desc += tes_fra

        return tes_desc

    # =================================
    def load(self, code):
        code = get_unicode(code, MIN_COD_LEN, MAX_COD_LEN)
        # -------------------
        if self.__database is not None and code is not u'':
            sql = u"""
            select 
            tes_title, tes_version, tes_description, tes_date_create, tes_date_update
            from test where tes_code='%s'
            """ % code
            # ---------------
            res = self.__database.pull_query(query=sql)
            # ---------------
            if res is not None:
                self.__code = code
                self.__in_db = True
                self.__title = unicode(res[0, 0])
                self.__version = unicode(res[0, 1])
                self.__description = unicode(res[0, 2])
                self.__date_create = time(res[0, 3])
                self.__date_update = time(res[0, 4])
                # -----------
                self.__frame_load()
                # -----------
                return True
            else:
                return False
        else:
            return False

    def save(self):
        if self.__database is not None and self.__code is not None and self.__title is not None:
            if self.__in_db:
                sql = u"""
                update test
                set tes_title='%s', tes_version='%s', tes_description='%s'
                where tes_code='%s'
                """
                sql %= (
                    self.__title, self.__version, self.__description, self.__code
                )
            else:
                sql = u"""
                insert into test 
                (tes_code, tes_title, tes_version, tes_description)
                values ('%s','%s','%s','%s')
                """
                sql %= (
                    self.__code, self.__title, self.__version, self.__description
                )
            # ---------------
            tes_res = self.__database.push_query(query=sql)
            self.__in_db = tes_res
            # ---------------
            fra_res = self.__frame_save() if tes_res else False
            # ---------------
            return fra_res
        else:
            return False

    def copy(self, code, version):
        new_tes = copy.deepcopy(self)
        new_tes.__in_db = False
        # ------------------
        new_tes.set_database(db=self.__database)
        # ------------------
        new_cod_check = new_tes.set_code(code=code)
        new_inf_check = new_tes.set_info(title=self.__title, version=version)
        # ------------------
        if new_cod_check and new_inf_check:
            return new_tes
        else:
            return None

    def remove(self):
        if self.__database and self.__in_db:
            sql = u"delete from test where tes_code='%s'" % self.__code
            tes_res = self.__database.push_query(query=sql)
            return tes_res
        else:
            return False

    # =================================
    def set_database(self, db):
        if isinstance(db, saccadedb):
            self.__database = db
            return True
        else:
            return False

    def set_code(self, code):
        code = get_unicode(code, MIN_COD_LEN, MAX_COD_LEN)
        # ------------------
        if self.__database is not None and code is not u'':
            sql = u"select * from test where tes_code='%s'" % code
            # ---------------
            res = self.__database.pull_query(query=sql)
            # ---------------
            if res is None:
                self.__code = code
                return True
            else:
                return False
        else:
            return False

    def set_info(self, title, version):
        title = get_unicode(title, MIN_TIT_LEN, MAX_TIT_LEN)
        version = get_unicode(version, MIN_VER_LEN, MAX_VER_LEN)
        # ------------------
        if self.__database is not None and title is not u'' and version is not u'':
            sql = u"select * from test where tes_title='%s' and tes_version='%s'" % (title, version)
            # ---------------
            res = self.__database.pull_query(query=sql)
            # ---------------
            if res is None:
                self.__title = title
                self.__version = version
                return True
            else:
                return False
        else:
            return False

    def set_description(self, description):
        self.__description = get_unicode(description)

    def get_database(self):
        return self.__database

    def get_code(self):
        return self.__code

    def get_title(self):
        return self.__title

    def get_version(self):
        return self.__version

    def get_description(self):
        return self.__description

    def is_on_db(self):
        return self.__in_db

    # =================================
    def frame_new(self, item):
        if isinstance(item, frame):
            fra_cnt = self.frame_count()
            if fra_cnt is None:
                self.__frame_arr = np.array([item], dtype=object)
            else:
                self.__frame_arr = np.insert(arr=self.__frame_arr, obj=fra_cnt, values=[item], axis=0)
            return True
        else:
            return False

    def frame_remove(self, index):
        fra_cnt = self.frame_count()
        if fra_cnt is not None and 0 <= index < fra_cnt:
            self.__frame_arr = np.delete(arr=self.__frame_arr, obj=index, axis=0) if fra_cnt > 1 else None
            return True
        else:
            return False

    def frame_move_up(self, index):
        fra_cnt = self.frame_count()
        if fra_cnt is not None and 0 < index < fra_cnt:
            temp = self.__frame_arr[index-1]
            self.__frame_arr[index-1] = self.__frame_arr[index]
            self.__frame_arr[index] = temp
            return True
        else:
            return False

    def frame_move_down(self, index):
        fra_cnt = self.frame_count()
        if fra_cnt is not None and 0 <= index < fra_cnt-1:
            temp = self.__frame_arr[index+1]
            self.__frame_arr[index+1] = self.__frame_arr[index]
            self.__frame_arr[index] = temp
            return True
        else:
            return False

    def frame_get_all(self):
        return self.__frame_arr

    def frame_get(self, index):
        fra_cnt = self.frame_count()
        if fra_cnt is not None and 0 <= index < fra_cnt:
            return self.__frame_arr[index]
        else:
            return None

    def frame_count(self):
        if self.__frame_arr is not None:
            return len(self.__frame_arr)
        else:
            return None

    # =================================
    def __frame_load(self):
        if self.__database is not None and self.__in_db:
            sql = u"""
            select fra_id
            from tes_frame
            where tes_code='%s'
            order by tes_code asc
            """ % self.__code
            fra_res = self.__database.pull_query(query=sql)
            # ---------------
            if fra_res is not None:
                for index in fra_res:
                    new_fra = frame()
                    new_fra.load(db=self.__database, tes=self.__code, fra=index[0])
                    self.frame_new(item=new_fra)

    def __frame_save(self):
        if self.__database is not None and self.__in_db:
            sql = u"delete from tes_frame where tes_code='%s'" % self.__code
            self.__database.push_query(query=sql)
            # ---------------
            fra_cnt = self.frame_count()
            if fra_cnt is not None:
                for index in range(fra_cnt):
                    self.__frame_arr[index].save(db=self.__database, tes=self.__code, fra=index)
            # ---------------
            return True
        else:
            return False


# =============================================================================
# Frame Class
# =============================================================================
class frame(object):
    def __init__(self):
        self.__color = u'black'
        self.__is_task = False
        self.__time = 0.0
        self.__key_all = None
        self.__key_sel = None
        # -------------------
        self.__obj_arr = None

    @property
    def description(self):
        fra_desc = u"""
        #=======================================#
        Frame:
            - color         : %s.
            - is task       : %s.
            -------------------------------------
            - time          : %f.
            -------------------------------------
            - keys allowed  : %s.
            - keys correct  : %s.
            -------------------------------------
        """ % (
            self.__color, self.__is_task,
            self.__time,
            self.__key_all, self.__key_sel,
            )
        # --------------
        obj_cnt = self.object_count()
        if obj_cnt is not None:
            fra_obj = u"""
            - object number : %d.
            """ % obj_cnt
            fra_desc += fra_obj

        return fra_desc

    # =================================
    def load(self, db, tes, fra):
        db_check = isinstance(db, saccadedb)
        fra_id = get_integer(fra)
        tes_code = get_unicode(tes)
        # -------------------
        if db_check:
            sql = u"""
            select 
            fra.fra_color, fra.fra_is_task, tas.tas_key_all, tas.tas_key_sel, tim.tim_time
            from tes_frame as fra
            inner join tes_fra_task as tas on fra.tes_code = tas.tes_code and fra.fra_id = tas.fra_id
            inner join tes_fra_time as tim on fra.tes_code = tim.tes_code and fra.fra_id = tim.fra_id
            where fra.tes_code='%s' and fra.fra_id='%d'
            """ % (tes_code, fra_id)
            # ---------------
            res = db.pull_query(query=sql)
            # ---------------
            if res is not None:
                self.__color = unicode(res[0, 0])
                self.__is_task = bool(int(res[0, 1]))
                self.__key_all = unicode(res[0, 2])
                self.__key_sel = unicode(res[0, 3])
                self.__time = float(res[0, 4])
                # -----------
                self.__object_load(db=db, tes=tes_code, fra=fra_id)
                # -----------
                return True
            else:
                return False
        else:
            return False

    def save(self, db, tes, fra):
        db_check = isinstance(db, saccadedb)
        fra_id = get_integer(fra)
        tes_code = get_unicode(tes)
        # -------------------
        if db_check:
            sql = u"""
            insert into tes_frame
            (tes_code, fra_id, fra_color, fra_is_task)
            values ('%s', '%d', '%s', '%x');
            insert into tes_fra_task
            (tes_code, fra_id, tas_key_all, tas_key_sel) 
            values ('%s', '%d', '%s', '%s');
            insert into  tes_fra_time
            (tes_code, fra_id, tim_time) 
            values ('%s', '%d', '%f');
            """
            sql %= (
                tes_code, fra_id, self.__color, self.is_task(),
                tes_code, fra_id, self.__key_all, self.__key_sel,
                tes_code, fra_id, self.__time
            )
            # ---------------
            fra_res = db.push_query(query=sql)
            # ---------------
            obj_res = self.__object_save(db=db, tes=tes_code, fra=fra_id) if fra_res else False
            # ---------------
            return obj_res
        else:
            return False

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def set_color(self, color):
        color = get_unicode(color)
        if color is not None and colors.isValidColor(color):
            self.__color = color

    def set_as_task(self, isactive):
        self.__is_task = get_boolean(isactive, default=self.__is_task)

    def set_time(self, time):
        self.__time = get_float(time)

    def set_keys_allowed(self, keys):
        self.__key_all = get_unicode(keys)

    def set_keys_selected(self, keys):
        self.__key_sel = get_unicode(keys)

    def get_color(self):
        return self.__color

    def is_task(self):
        return self.__is_task

    def get_time(self):
        return self.__time

    def get_keys_allowed(self):
        return self.__key_all

    def get_keys_selected(self):
        return self.__key_sel

    # =================================
    def object_new(self, item):
        if isinstance(item, frame_object):
            obj_cnt = self.object_count()
            if obj_cnt is None:
                self.__obj_arr = np.array([item], dtype=object)
            else:
                self.__obj_arr = np.insert(arr=self.__obj_arr, obj=obj_cnt, values=[item], axis=0)
            return True
        else:
            return False

    def object_remove(self, index):
        obj_cnt = self.object_count()
        if obj_cnt is not None and 0 <= index < obj_cnt:
            self.__obj_arr = np.delete(arr=self.__obj_arr, obj=index, axis=0) if obj_cnt > 1 else None
            return True
        else:
            return False

    def object_move_up(self, index):
        obj_cnt = self.object_count()
        if obj_cnt is not None and 0 < index < obj_cnt:
            temp = self.__obj_arr[index-1]
            self.__obj_arr[index-1] = self.__obj_arr[index]
            self.__obj_arr[index] = temp
            return True
        else:
            return False

    def object_move_down(self, index):
        obj_cnt = self.object_count()
        if obj_cnt is not None and 0 <= index < obj_cnt-1:
            temp = self.__obj_arr[index+1]
            self.__obj_arr[index+1] = self.__obj_arr[index]
            self.__obj_arr[index] = temp
            return True
        else:
            return False

    def object_get_all(self):
        return self.__obj_arr

    def object_get(self, index):
        obj_cnt = self.object_count()
        if obj_cnt is not None and 0 <= index < obj_cnt:
            return self.__obj_arr[index]
        else:
            return None

    def object_count(self):
        if self.__obj_arr is not None:
            return len(self.__obj_arr)
        else:
            return None

    # =================================
    def __object_load(self, db, tes, fra):
        db_check = isinstance(db, saccadedb)
        fra_id = get_integer(fra)
        tes_code = get_unicode(tes)
        # -------------------
        if db_check:
            sql = u"""
            select obj_id 
            from tes_fra_object
            where tes_code='%s' and fra_id='%d'
            order by obj_id asc
            """ % (tes_code, fra_id)
            obj_res = db.pull_query(query=sql)
            # ---------------
            if obj_res is not None:
                for index in obj_res:
                    new_obj = frame_object()
                    new_obj.load(db=db, tes=tes_code, fra=fra_id, obj=index[0])
                    self.object_new(item=new_obj)

    def __object_save(self, db, tes, fra):
        db_check = isinstance(db, saccadedb)
        fra_id = get_integer(fra)
        tes_code = get_unicode(tes)
        # -------------------
        if db_check:
            sql = u"delete from tes_fra_object where tes_code='%s' and fra_id='%d'" % (tes_code, fra_id)
            db.push_query(query=sql)
            # ---------------
            obj_cnt = self.object_count()
            if obj_cnt is not None:
                for index in range(obj_cnt):
                    self.__obj_arr[index].save(db=db, tes=tes_code, fra=fra_id, obj=index)
            # ---------------
            return True
        else:
            return False

    # =================================
    def get_frame(self, win=visual.Window):
        obj_cnt = self.object_count()
        if obj_cnt is not None:
            return [item.get_figure(win=win) for item in self.__obj_arr]
        else:
            return None


# =============================================================================
# Object Class
# =============================================================================
class frame_object(object):
    def __init__(self):
        self.__name = None
        self.__units = u'degFlat'
        self.__pos = (0.0, 0.0)
        self.__ori = 0.0
        self.__size = 0.0
        # -------------------
        self.__is_img = False
        self.__image = None
        self.__shape = u'square'
        self.__color = u'white'

    @property
    def description(self):
        description = u"""
        #=======================================#
        Object:
            - name          : %s
            - units         : %s
            - position      : (%f, %f)
            - orientation   : %f
            - size          : %f
            -------------------------------------
            - is image      : %s
            - image loaded  : %s
            -------------------------------------
            - shape         : %s 
            - color         : %s
        """ % (
            self.__name, self.__units, self.__pos[0], self.__pos[1], self.__ori, self.__size,
            self.__is_img, self.__image is not None,
            self.__shape, self.__color
            )

        return description

    # =================================
    def load(self, db, tes, fra, obj):
        db_check = isinstance(db, saccadedb)
        fra_id = get_integer(fra)
        obj_id = get_integer(obj)
        tes_code = get_unicode(tes)
        # -------------------
        if db_check:
            sql = u"""
            select
            obj_name, obj_units, obj_posx, obj_posy, obj_ori, obj_size, obj_is_img, obj_image, obj_shape, obj_color
            from tes_fra_object
            where tes_code='%s' and fra_id='%d' and obj_id='%d'
            """ % (tes_code, fra_id, obj_id)
            # ---------------
            res = db.pull_query(query=sql)
            # ---------------
            if res is not None:
                self.__name = unicode(res[0, 0])
                self.__units = unicode(res[0, 1])
                self.__pos = (float(res[0, 2]),
                              float(res[0, 3]))
                self.__ori = float(res[0, 4])
                self.__size = float(res[0, 5])
                self.__is_img = bool(int(res[0, 6]))
                self.__image = self.decode_image(res[0, 7])
                self.__shape = unicode(res[0, 8])
                self.__color = unicode(res[0, 9])
                # -----------
                return True
            else:
                return False
        else:
            return False

    def save(self, db, tes, fra, obj):
        db_check = isinstance(db, saccadedb)
        fra_id = get_integer(fra)
        obj_id = get_integer(obj)
        tes_code = get_unicode(tes)
        # -------------------
        if db_check:
            sql = u"""
            insert into tes_fra_object
            (tes_code, fra_id, obj_id, 
            obj_name, obj_units, obj_posx, obj_posy, obj_ori, obj_size,
            obj_is_img, obj_image, 
            obj_shape, obj_color)
            values ('%s', '%d', '%d', '%s', '%s', '%f', '%f', '%f', '%f', '%x', '%s', '%s', '%s')
            """
            sql %= (
                tes_code, fra_id, obj_id,
                self.__name, self.__units, self.__pos[0], self.__pos[1], self.__ori, self.__size,
                self.__is_img, self.encode_image(),
                self.__shape, self.__color
            )
            # ---------------
            obj_res = db.push_query(query=sql)
            # ---------------
            return obj_res
        else:
            return False

    def copy(self):
        return copy.deepcopy(self)

    # =================================
    def decode_image(self, encimg):
        from io import BytesIO as bio
        # -------------------
        encimg = get_unicode(encimg)
        if encimg is not u'':
            img_buff = bio()
            img_buff.write(encimg.decode(u'base64'))
            # ---------------
            image = Image.open(img_buff)
            return image
        else:
            return None

    def encode_image(self):
        from io import BytesIO as bio
        # -------------------
        if self.__image is not None:
            img_buff = bio()
            self.__image.save(img_buff, u'PNG')
            return img_buff.getvalue().encode(u'base64')
        else:
            return u''

    # =================================
    def set_name(self, name):
        self.__name = get_unicode(name)

    def set_units(self, units):
        units = get_unicode(units)
        if units in [u'norm', u'cm', u'deg', u'degFlat', u'degFlatPos', u'pix']:
            self.__units = units
        else:
            self.__units = u'degFlat'

    def set_position(self, posx, posy):
        self.__pos = (get_float(posx), get_float(posy))

    def set_orientation(self, ori):
        self.__ori = get_float(ori)

    def set_size(self, size):
        self.__size = get_float(size)

    def set_is_image(self, isactive):
        self.__is_img = get_boolean(isactive)

    def set_image(self, imgpath):
        imgpath = get_unicode(imgpath)
        if imgpath is not u'' and os.path.isfile(imgpath):
            self.__is_img = True
            self.__image = Image.open(imgpath)

    def set_shape(self, shape):
        shape = get_unicode(shape)
        if shape in [u'arrow', u'circle', u'cross', u'gauss', u'square']:
            self.__shape = shape

    def set_color(self, color):
        color = get_unicode(color)
        if color is not None and colors.isValidColor(color):
            self.__color = color

    def get_name(self):
        return self.__name

    def get_units(self):
        return self.__units

    def get_position(self):
        return self.__pos

    def get_orientation(self):
        return self.__ori

    def get_size(self):
        return self.__size

    def is_image(self):
        return self.__is_img

    def get_image(self):
        return self.__image

    def get_shape(self):
        return self.__shape

    def get_color(self):
        return self.__color

    # =================================
    def get_figure(self, win=visual.Window):
        if self.__is_img and self.__image is not None:
            return visual.ImageStim(win=win, name=self.__name, image=self.__image,
                                    size=self.__size, pos=self.__pos, ori=self.__ori,
                                    units=self.__units
                                    )
        elif self.__shape == u'arrow':
            return visual.ShapeStim(win=win, name=self.__name, lineColor=self.__color, fillColor=self.__color,
                                    vertices=((1.0, 0.0), (0.6667, 0.1667), (0.6667, 0.0667), (0.0, 0.0667),
                                              (0.0, -0.0667), (0.6667, -0.0667), (0.6667, -0.1667)),
                                    size=self.__size, pos=self.__pos, ori=self.__ori,
                                    units=self.__units
                                    )
        else:
            return visual.GratingStim(win=win, name=self.__name, color=self.__color,
                                      mask=None if self.__shape == u'square' else self.__shape,
                                      sf=0, size=self.__size, pos=self.__pos, ori=self.__ori,
                                      units=self.__units
                                      )
