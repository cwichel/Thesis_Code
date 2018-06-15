# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from saccadeapp.api import SaccadeDB
from saccadeapp.api import Configuration
from saccadeapp.api import ExperimentHandler
from saccadeapp.api import Experiment, Test, Frame, Component


# =============================================================================
# Configuration Example
# =============================================================================
if __name__ == u"__main__":
    database = SaccadeDB()
    #
    config_profile = Configuration(db=database)
    config_profile.set_name(name=u"Test Profile (code)")
    config_profile.set_events_path(path=u"C:/SaccadeApp_events/")
    config_profile.set_tracker(tracker=u"eyetribe")
    config_profile.set_monitor(monitor=u"default")
    config_profile.set_screen(screen=0)
    config_profile.save()
    #
    experiment = Experiment(db=database)
    experiment.set_code(code=u"exp_0001")
    experiment.set_info(name=u"Test Experiment", version=u"coded_1.0")
    experiment.set_dialog(status=False)
    experiment.set_random(status=False)
    experiment.set_rest_conf(status=False)
    experiment.set_space_start(status=False)
    experiment.set_comments(text=u"")
    experiment.set_descripton(text=u"This experiment was created with code!")
    experiment.set_instructions(text=u"Look the image, then press space.")
    #
    test = Test()
    test.set_name(name=u"Couple Image Test")
    test.set_description(text=u"")
    #
    frame = Frame()
    frame.set_name(name=u"Couple Presentation")
    frame.set_color(color=u"black")
    frame.set_as_task(state=True)
    frame.set_keys_allowed(keys=u"space")
    frame.set_keys_correct(keys=u"space")
    #
    component = Component()
    component.set_name(name=u"Couple Image")
    component.set_size(size=1.0)
    component.set_units(units=u"deg")
    component.set_position(posx=0.0, posy=0.0)
    component.set_rotation(rot=0.0)
    component.set_image(image=u"couple.png")
    #
    frame.item_add(item=component)
    test.item_add(item=frame)
    experiment.item_add(item=test)
    experiment.sequence_add(item_id=0, quantity=1)
    experiment.save()

    handler = ExperimentHandler()
    handler.prepare(exp_code=u"exp_0001", conf_name=u"Test Profile (code)")
    handler.execute(frame_save=True)

