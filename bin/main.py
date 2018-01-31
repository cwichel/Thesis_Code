# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from psychopy import visual, core
from saccadeApp import saccadedb, Experiment, Test, Frame, Component


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
    database = saccadedb()

    exp = Experiment()
    exp.set_database(db=database)
    # exp.set_code(u'exp1_t23')
    # exp.set_info(u'exp1', u'v1.0')

    exp.load(code=u'exp1_t23')

    print 1



