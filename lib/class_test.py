# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from lib import saccadedb
from psychopy import visual, colors


# =============================================================================
# Constants
# =============================================================================
MIN_COD_LEN = 5
MIN_TIT_LEN = 5
MIN_VER_LEN = 5
MAX_COD_LEN = 10
MAX_VER_LEN = 10
MAX_TIT_LEN = 100


# =============================================================================
# Classes
# =============================================================================
class test:
    def __init__(self):
        self.__isondb = False
        self.__database = None
        # base
        self.__code = None
        self.__title = None
        self.__version = None
        self.__description = None
        # frames
        self.__frames = []

    # =======================
    def load(self):
        if self.__database is not None and self.__code is not None:
            sql = u"select tes_title, tes_version, tes_description " +\
                  u"from test where tes_code='%s'"
            sql = sql % self.__code
            res = self.__database.pull_query(query=sql)
            if res is not None:
                self.__isondb = True
                self.__title = unicode(res[0, 0])
                self.__version = unicode(res[0, 1])
                self.__description = unicode(res[0, 2])
                self.__frames = frame.test_load(parent=self)
                return True
        return False

    def save(self):
        if self.__database is not None and self.__code is not None and self.__title is not None:
            if self.__isondb:
                sql = u"update test " +\
                      u"set tes_title='%s', tes_version='%s', tes_description='%s' " +\
                      u"where tes_code='%s'"
                sql %= tuple([self.__title, self.__version, self.__description, self.__code])
            else:
                sql = u"insert into test " +\
                      u"(tes_code, tes_title, tes_version, tes_description) " +\
                      u"values ('%s','%s','%s','%s')"
                sql %= tuple([self.__code, self.__version, self.__description, self.__title])
            if self.__database.push_query(query=sql):
                self.__isondb = True
                for item in self.__frames:
                    if isinstance(item, frame):
                        item.save()
                return True
        return False

    def copy(self, code, version):
        newtest = test()
        if newtest.set_code(code=code) and newtest.set_info(title=self.__title, version=version):
            newtest.set_description(self.__description)
            for item in self.__frames:
                newtest.frame_new(item.copy(parent=newtest))
            return newtest
        return None

    def remove(self):
        if self.__database is not None and self.__code is not None and self.__isondb:
            sql = u"delete from test " +\
                  u"where tes_code='%s'"
            sql = sql % self.__code
            return self.__database.push_query(query=sql)

    # =======================
    def set_database(self, db):
        if isinstance(db, saccadedb):
            self.__database = db
            return True
        return False

    def set_code(self, code):
        cod_check = isinstance(code, unicode) and MIN_COD_LEN < len(code) < MAX_COD_LEN
        if self.__database is not None and cod_check:
            sql = u"select count(1) " +\
                  u"from test where tes_code='%s'" % code
            res = self.__database.pull_query(query=sql)
            if res is None:
                self.__code = code
                return True
        return False

    def set_info(self, title, version):
        tit_check = isinstance(title, unicode) and MIN_TIT_LEN < len(title) < MAX_TIT_LEN
        ver_check = isinstance(version, unicode) and MIN_VER_LEN < len(version) < MAX_VER_LEN
        if self.__database is not None and tit_check and ver_check:
            sql = u"select count(1) " +\
                  u"from test where tes_title='%s' and tes_version='%s" % tuple([title, version])
            res = self.__database.pull_query(query=sql)
            if res is None:
                self.__title = title
                self.__version = version
                return True
        return False

    def set_description(self, description):
        if isinstance(description, unicode):
            self.__description = description
            return True
        return False

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

    # =======================
    def frame_new(self, item=None):
        if isinstance(item, frame):
            self.__frames.append(item)
            return True
        else:
            return False

    def frame_remove(self):
        pass

    def frame_move_up(self):
        pass

    def frame_move_down(self):
        pass

    # =======================
    def preview(self):
        pass

class frame:
    def __init__(self):
        self.__isondb = False
        self.__parent_tes = None
        # base
        self.__color = u'black'
        self.__istask = False
        # extra
        self.__time = 0.0
        self.__keysall = None
        self.__keyssel = None
        # objects
        self.__objects = []

    # =======================
    @classmethod
    def test_load(cls, parent):
        if isinstance(parent, test) and parent.get_database() is not None:
            tes_code = parent.get_code()
            sql = u"select fra_id " +\
                  u"from tes_frame where tes_code='%s' " % tes_code +\
                  u"order by fra_id asc"
            res = parent.get_database().pull_query(query=sql)
            if res is not None:
                output = []
                for item in res:
                    frame_item = frame()
                    if frame_item.load(parent=parent, fra_id=item):
                        output.append(frame_item)
                return output
        return []

    def load(self, parent, fra_id):
        if isinstance(parent, test) and parent.get_database() is not None:
            sql = u"select * fra_color, fra_istask" +\
                  u"from tes_frame where tes_code='%s' and fra_id='%s'" % tuple([parent.get_code(), fra_id])
            res = parent.get_database().pull_query(query=sql)
            if res is not None:
                self.__isondb = True
                self.__parent_tes = parent
                self.__color = unicode(res[0, 0])
                self.__istask = bool(int(res[0, 1]))
                self.__objects = frameobject.frame_load(parent=self)
        return False

    def save(self):
        pass

    def copy(self):
        pass

    def remove(self):
        pass

    # =======================
    def set_parent(self, parent):
        if isinstance(parent, test):
            self.__parent_tes = parent
            return True
        else:
            return False

    def set_color(self, color):
        pass

    def set_astask(self, istask):
        pass

    def set_time(self, time):
        pass

    def set_keys_allowed(self, keys):
        pass

    def set_keys_selected(self, keys):
        pass

    def get_parent(self):
        return self.__parent_tes

    def get_color(self):
        pass

    def is_task(self):
        pass

    def get_time(self):
        pass

    def get_keys_allowed(self):
        pass

    def get_keys_selected(self):
        pass

    # =======================
    def object_new(self):
        pass

    def object_remove(self):
        pass

    def object_move_up(self):
        pass

    def object_move_down(self):
        pass

    # =======================
    def preview(self):
        pass

class frameobject:
    def __init__(self):
        self.__isondb = False
        self.__parent_fra = None
        # base
        self.__name = None
        self.__units = u'deg'
        self.__pos = (0.0, 0.0)
        self.__ori = 0.0
        # extra
        self.__isimg = False
        self.__image = None
        self.__shape = u'square'
        self.__color = u'white'

    # =======================
    @classmethod
    def frame_load(cls, parent):
        if isinstance(parent, frame) and parent.get_parent().get_database() is not None:
            pass
        return []

    def load(self):
        pass

    def save(self):
        pass

    def copy(self):
        pass

    def remove(self):
        pass

    # =======================
    def set_parent(self):
        pass

    def set_name(self):
        pass

    def set_units(self):
        pass

    def set_position(self):
        pass

    def set_orientation(self):
        pass

    def set_asimage(self):
        pass

    def set_image(self):
        pass

    def set_shape(self):
        pass

    def set_color(self):
        pass

    def get_parent(self):
        pass

    def get_name(self):
        pass

    def get_units(self):
        pass

    def get_position(self):
        pass

    def get_orientation(self):
        pass

    def is_image(self):
        pass

    def get_image(self):
        pass

    def get_shape(self):
        pass

    def get_color(self):
        pass
