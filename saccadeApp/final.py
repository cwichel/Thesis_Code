# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import copy
from PIL import Image
from psychopy import visual, colors


# =============================================================================
# Constants
# =============================================================================
class utils:
    @staticmethod
    def ftext(word, lmin=0, lmax=-1):
        try:
            temp = unicode(word)
            if lmax <= lmin <= len(temp) or lmin <= len(temp) <= lmax:
                return temp
            else:
                return u''
        except:
            return u''

    @staticmethod
    def fint(value, default=None):
        try:
            temp = int(value)
            return temp
        except:
            return default

    @staticmethod
    def ffloat(value, default=None):
        try:
            temp = float(value)
            return temp
        except:
            return default

    @staticmethod
    def fbool(state, default=False):
        try:
            temp = bool(state)
            return temp
        except:
            return default


# =============================================================================
# Constants
# =============================================================================
class frame(object):
    pass


class component(object):
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
    def set_name(self, name):
        name = utils.ftext(name, lmin=3)
        if name != u'':
            self.__name = name
            return True
        else:
            return False

    def get_name(self):
        return self.__name

    # -----------------------
    def set_units(self, units):
        units = utils.ftext(units)
        if units in [u'norm', u'cm', u'deg', u'degFlat', u'degFlatPos', u'pix']:
            self.__unit = units
            return True
        else:
            return False

    def get_units(self):
        return self.__unit

    # -----------------------
    def set_pos(self, posx, posy):
        posx = utils.ffloat(posx)
        posy = utils.ffloat(posy)
        if posx is not None and posy is not None:
            self.__pos = (posx, posy)
            return True
        else:
            return False

    def get_pos(self):
        return self.__pos

    # -----------------------
    def set_orientation(self, ori):
        ori = utils.ffloat(ori)
        if ori is not None:
            self.__ori = ori
            return True
        else:
            return False

    def get_orientation(self):
        return self.__ori

    # -----------------------
    def set_size(self, size):
        size = utils.ffloat(size)
        if size is not None:
            self.__size = size
            return True
        else:
            return False

    def get_size(self):
        return self.__size

    # -----------------------
    def set_image(self, imagepath):
        imagepath = utils.ftext(imagepath)
        if imagepath is not u'' and os.path.isfile(imagepath):
            self.__fimg = True
            self.__imag = Image.open(imagepath)
            return True
        else:
            return False

    def get_image(self):
        return self.__imag

    # -----------------------
    def set_shape(self, shape):
        shape = utils.ftext(shape)
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
        color = utils.ftext(color)
        if colors.isValidColor(color):
            self.__colr = color
            return True
        else:
            return False

    def get_color(self):
        return self.__colr

    # =================================
    def __decode_image(self, encimg):
        from io import BytesIO as bio
        # -------------------
        coded = utils.ftext(encimg)
        if coded != u'':
            try:
                img_buff = bio()
                img_buff.write(coded.decode(u'base64'))
                # -----------
                self.__fimg = True
                self.__imag = Image.open(img_buff)
            except:
                return False
        else:
            return False

    def __encode_image(self):
        from io import BytesIO as bio
        # -------------------
        if self.__imag is not None:
            img_buff = bio()
            self.__imag.save(img_buff, u'PNG')
            return img_buff.getvalue().encode(u'base64')
        else:
            return u''

    # =================================
    def load(self, db, exp, tes, fra, com):
        try:
            sql = u"""
            select
            com_name, com_unit, com_posx, com_posy, com_orie, com_size, com_fimg, com_imag, com_shpe, com_colr
            from component
            where exp_code='%s' and tes_indx='%d' and fra_indx='%d' and com_indx='%d'
            """ % (exp, tes, fra, com)
            com_res = db.pull_query(query=sql)
            # ---------------
            if com_res is not None:
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
                # -----------
                return True
            else:
                return False
        except:
            return False

    def save(self, db, exp, tes, fra, com):
        try:
            sql = u"""
            insert into component
            (exp_code, tes_indx, fra_indx, com_indx, 
            com_name, com_unit, com_posx, com_posy, com_orie, com_size, 
            com_fimg, com_imag, com_shpe, com_colr)
            values ('%s', '%d', '%d', '%d', '%s', '%s', '%f', '%f', '%f', '%f', '%x', '%s', '%s', '%s')
            """ % (
                exp, tes, fra, com,
                self.__name, self.__unit, self.__pos[0], self.__pos[1], self.__ori, self.__size,
                self.__fimg, self.__encode_image(), self.__shpe, self.__colr)
            com_res = db.push_query(query=sql)
            # ---------------
            return com_res
        except:
            return False

    def copy(self):
        return copy.deepcopy(self)
