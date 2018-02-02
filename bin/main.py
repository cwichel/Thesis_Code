# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from psychopy import visual, core
from saccadeApp import generate_experiment_files
from saccadeApp import SaccadeDB, Master, Experiment, Test, Frame, Component


# Execute test 1
# res = test1(db=database)
# # Execute test 2
# if res:
#     tes = test2(db=database)
# else:
#     tes = None
# # Show frames...
# if isinstance(tes, test):
#     win = visual.Window(size=(800, 600), monitor=u'default', screen=1, color=u'black')
#     num = tes.frame_count()
#     fra = tes.frame_get_all()
#     if num is not None:
#         for fra_item in fra:
#             back = visual.Rect(win=win, width=800, height=600, fillColor=fra_item.get_color(), units=u'pix')
#             back.draw()
#             obj = fra_item.get_frame(win)
#             for obj_item in obj:
#                 obj_item.draw()
#             win.flip()
#             core.wait(2.0)
#     win.close()
# =============================================================================
# Main Loop
# =============================================================================
if __name__ == '__main__':
    database = SaccadeDB()
    # =======================
    # =======================
    # mas = Master()
    # mas.set_database(db=database)
    # mas.load(name=u'Default')
    # mas.set_name(name=u'Default')
    # mas.set_screen(screen=1)
    # mas.set_tracker(tracker=u'pytribe')
    # mas.set_monitor(monitor=u'default')
    # mas.set_experiment_path(path=u"D:\\Github\\Memoria\\Memoria_Code\\bin\\events")
    # mas.save()
    # =======================
    # =======================
    # exp = Experiment()
    # exp.set_database(db=database)
    # exp.load(code=u'exp1_t23')
    # # =======================
    # exp.set_code(u'exp1_t23')
    # exp.set_info(u'exp1', u'v1.0')
    # exp.set_random(status=True)
    # com1 = Component()
    # com1.set_name(u'fixation')
    # com1.set_shape(u'cross')
    # com2 = Component()
    # com2.set_position(0.0, 10.0)
    # com2.set_name(u'objective')
    # com3 = Component()
    # com3.set_name(u'image')
    # com3.set_orientation(25.0)
    # com3.set_image(u'image1.jpeg')
    # fra1 = Frame()
    # fra1.set_name(u'fixation')
    # fra1.component_add(com1)
    # fra2 = fra1.copy()
    # fra2.set_name(u'prepare')
    # fra2.component_add(com2)
    # fra3 = Frame()
    # fra3.set_name(u'nothing')
    # fra4 = Frame()
    # fra4.set_name(u'image presentation')
    # fra4.component_add(com3)
    # tes1 = Test()
    # tes1.set_repetitions(5)
    # tes1.set_name(u'test 1')
    # tes1.frame_add(fra1)
    # tes1.frame_add(fra2)
    # tes1.frame_add(fra3)
    # tes2 = tes1.copy()
    # tes2.set_name(u'test2')
    # tes2.set_repetitions(3)
    # tes2.frame_delete(2)
    # tes2.frame_add(fra4)
    # exp.test_add(tes1)
    # exp.test_add(tes2)
    # # =======================
    # exp.save()
    # =======================
    # exp.remove()
    # =======================
    # =======================
    # win = visual.Window(size=(800, 600), monitor=u'default', screen=1, color=u'black')

    generate_experiment_files(db=database, mas=u'Default', exp=u'exp1_t23')

    print u'FIN'

