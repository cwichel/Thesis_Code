# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from psychopy import visual, core
from saccadeApp import saccadedb, experiment, test, frame, frame_object


def test1(db):  # Test 1: Crear un test completo y guardarlo.
    # Create test:
    tes1 = test()
    tes1.set_database(db)
    if tes1.set_code(u'tes1_test'):
        # Create frames...
        # frame 1 ===============
        obj1 = frame_object()
        obj1.set_units(u'deg')
        obj1.set_size(2.0)
        obj1.set_name(u'fixation')
        obj1.set_shape(u'cross')
        # -------------
        fra1 = frame()
        fra1.set_time(1.8)
        fra1.object_new(obj1)
        # frame 2 ===============
        obj2 = frame_object()
        obj2.set_units(u'deg')
        obj2.set_size(2.0)
        obj2.set_name(u'objective')
        obj2.set_shape(u'square')
        obj2.set_color(u'yellow')
        obj2.set_position(10.0, 0.0)
        # -------------
        fra2 = fra1.copy()
        fra2.object_new(obj2)
        # frame 3 ===============
        fra3 = fra2.copy()
        fra3.object_remove(0)
        # frame 4 ===============
        obj3 = frame_object()
        obj3.set_image(u'image1.jpeg')
        obj3.set_units(u'deg')
        obj3.set_orientation(45.0)
        obj3.set_size(2.0)
        obj3.set_is_image(True)
        # -------------
        fra4 = frame()
        fra4.set_time(3.0)
        fra4.set_color(u'green')
        fra4.object_new(obj3)
        # =======================
        tes1.set_info(u'first', u'v1.0')
        tes1.set_description(u'test purpose')
        tes1.frame_new(fra1)
        tes1.frame_new(fra2)
        tes1.frame_new(fra3)
        tes1.frame_new(fra4)
        # ---------
        if tes1.save():
            print u'Test correctly saved.'
            return True
        else:
            print u'Error saving test!'
            return False
    else:
        print u'Test already on DB.'
        return True


def test2(db):  # Test 2: Cargar el test creado anteriormente
    tes2 = test()
    tes2.set_database(db)
    if tes2.load(u'tes1_test'):
        print u'Test correctly loaded'
        return tes2
    else:
        print u'Error loading test!'
        return None


# =============================================================================
# Main Loop
# =============================================================================
if __name__ == '__main__':

    database = saccadedb()
    # Execute test 1
    res = test1(db=database)
    # Execute test 2
    if res:
        tes = test2(db=database)
    else:
        tes = None
    # Show frames...
    if isinstance(tes, test):
        win = visual.Window(size=(800, 600), monitor=u'default', screen=1, color=u'black')
        num = tes.frame_count()
        fra = tes.frame_get_all()
        if num is not None:
            for fra_item in fra:
                back = visual.Rect(win=win, width=800, height=600, fillColor=fra_item.get_color(), units=u'pix')
                back.draw()
                obj = fra_item.get_frame(win)
                for obj_item in obj:
                    obj_item.draw()
                win.flip()
                core.wait(2.0)
        win.close()
