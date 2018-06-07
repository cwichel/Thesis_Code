# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
from psychopy import visual, core
from psychopy.iohub.util import MessageDialog
from psychopy.iohub import (ioHubExperimentRuntime, getCurrentDateTimeString)


# =============================================================================
# Script Handler
# =============================================================================
class ExperimentHandler(object):
    # =================================
    def __init__(self):
        self.__parameters = dict()
        self.__is_ready = False

    # =================================
    def prepare(self, db_path=u"", conf_name=u"", exp_code=u""):
        import time
        import yaml
        import codecs
        from os import path, makedirs
        from .utils import format_path
        from .saccadedb import SaccadeDB
        from .core import Configuration, Experiment
        if not self.__is_ready:
            database = SaccadeDB(filepath=db_path)
            exp_data = Experiment(db=database, code=exp_code)
            cfg_data = Configuration(db=database, name=conf_name)
            if cfg_data.in_database() and exp_data.in_database():
                # Prepare folders and file names
                exp_timestamp = unicode(int(time.time()))
                exp_name = exp_data.get_name()
                exp_code = exp_data.get_code()
                exp_version = exp_data.get_version()
                event_path = cfg_data.get_events_path()
                exp_base_path = format_path(event_path+u"["+exp_name+u"]/")
                exp_this_path = format_path(exp_base_path+u"["+exp_version+u"]"+u"["+exp_code+u"]/")
                exp_conf_path = format_path(exp_this_path+u"iohub/")
                exp_back_path = format_path(exp_this_path+u"backup/")
                exp_imag_path = format_path(exp_this_path+u"frames/")
                exp_back_file = u"["+exp_code+u"]["+u"["+exp_timestamp+u"]configuration_back.yaml"
                exp_conf_file = u"["+exp_code+u"]["+u"["+exp_timestamp+u"]experiment_config.yaml"
                exp_exec_file = u"["+exp_code+u"]["+u"["+exp_timestamp+u"]iohub_config.yaml"
                if not path.exists(event_path):
                    makedirs(event_path)
                if not path.exists(exp_base_path):
                    makedirs(exp_base_path)
                if not path.exists(exp_this_path):
                    makedirs(exp_this_path)
                if not path.exists(exp_conf_path):
                    makedirs(exp_conf_path)
                if not path.exists(exp_back_path):
                    makedirs(exp_back_path)
                if not path.exists(exp_imag_path):
                    makedirs(exp_imag_path)
                # Prepare and save data to files
                # Execution configuration log
                exp_back_data = {
                    u"Experiment": exp_data.get_configuration(),
                    u"Configuration": cfg_data.get_configuration()
                }
                with codecs.open(filename=exp_back_path+exp_back_file, mode=u"w", encoding=u"utf-8") as outfile:
                    yaml.safe_dump(data=exp_back_data, stream=outfile, default_flow_style=False, indent=4)
                # Experiment configuration data
                exp_conf_data = exp_data.get_iohub()
                exp_conf_data[u"ioHub"][u"config"] = exp_conf_path+exp_exec_file
                exp_conf_data[u"session_defaults"][u"code"] = exp_timestamp
                with codecs.open(filename=exp_conf_path+exp_conf_file, mode=u"w", encoding=u"utf-8") as outfile:
                    yaml.safe_dump(data=exp_conf_data, stream=outfile, default_flow_style=None, indent=4)
                # Iohub execution data
                exp_exec_data = cfg_data.get_iohub()
                exp_exec_data[u"data_store"][u"filename"] = exp_this_path+u"["+exp_code+u"]events_data"
                with codecs.open(filename=exp_conf_path+exp_exec_file, mode=u"w", encoding=u"utf-8") as outfile:
                    yaml.safe_dump(data=exp_exec_data, stream=outfile, default_flow_style=None, indent=4)
                # Create script configuration dict
                self.__parameters[u"experiment_path"] = exp_this_path
                self.__parameters[u"frame_save_path"] = exp_imag_path
                self.__parameters[u"configuration_path"] = exp_conf_path
                self.__parameters[u"configuration_file"] = exp_conf_file
                self.__parameters[u"experiment_data"] = exp_data
                # Avoid to execute this again
                self.__is_ready = True
                return u"Operation Ok.", True
            return u"Configuration profile/experiment doesn't exist on database.", False
        return u"No need to execute this again.", False

    def execute(self, frame_save=False):
        if self.__is_ready:
            self.__parameters[u"frame_save"] = frame_save
            runtime = ExperimentRuntime(parameters=self.__parameters)
            runtime.start()
            return u"Operation Ok.", True
        return u"Experiment not configured.", False


# =============================================================================
# Script
# =============================================================================
class ExperimentRuntime(ioHubExperimentRuntime):
    # =================================
    def __init__(self, parameters):
        super(ExperimentRuntime, self).__init__(configFilePath=parameters[u'configuration_path'],
                                                configFile=parameters[u'configuration_file'])
        self.__frame_save_path = parameters[u'frame_save_path']
        self.__frame_save = parameters[u'frame_save']
        self.__experiment = parameters[u'experiment_data']

    # =================================
    def run(self, *args):
        from .switch import Switch
        # Hardware configuration
        try:
            tracker = self.hub.devices.tracker
            tracker.runSetupProcedure()
            tracker.setRecordingState(False)
        except Exception:
            md = MessageDialog(title=u"No Eye Tracker Configuration Found",
                               msg=u"No eyetracker selected/found.\nCheck your configuration profile.",
                               showButtons=MessageDialog.OK_BUTTON, dialogType=MessageDialog.ERROR_DIALOG,
                               allowCancel=False, display_index=0)
            md.show()
            core.quit()
        display = self.hub.devices.display
        kb = self.hub.devices.keyboard
        # Main window configuration
        win = visual.Window(size=display.getPixelResolution(), monitor=display.getPsychopyMonitorName(), fullscr=True,
                            units=display.getCoordinateType(), allowGUI=False, screen=display.getIndex())
        # Get experiment content
        execution = self.__experiment.get_execution(win=win)
        if len(execution[u"test_sequence"]) == 0:
            md = MessageDialog(title=u"No test available",
                               msg=u"No available tests selected/found.\nCheck the experiment settings.",
                               showButtons=MessageDialog.OK_BUTTON, dialogType=MessageDialog.ERROR_DIALOG,
                               allowCancel=False, display_index=0)
            md.show()
            win.close()
            core.quit()
        # Show instructions
        text_scr = visual.TextStim(win=win, text=u"", pos=(0, 0), height=24, wrapWidth=win.size[0] * 0.9,
                                   color=u"white", alignHoriz=u"center", alignVert=u"center", )
        text_scr.setText(text=execution[u"instructions"]+u"\n\nPress Any Key to Start Experiment.")
        text_scr.draw()
        flip_time = win.flip()
        self.hub.clearEvents(u"all")
        kb.waitForPresses()
        # Start Data Logging
        self.hub.sendMessageEvent(text=u"======= EXPERIMENT START =======", sec_time=flip_time)
        self.hub.sendMessageEvent(text=u"============= INFO =============")
        self.hub.sendMessageEvent(text=u"Date:          {0}.".format(getCurrentDateTimeString()))
        self.hub.sendMessageEvent(text=u"Experiment ID: {0}.".format(self.hub.experimentID))
        self.hub.sendMessageEvent(text=u"Session    ID: {0}.".format(self.hub.experimentSessionID))
        self.hub.sendMessageEvent(text=u"Screen (ID, Size, CoordType): ({0}, {1}, {2}).".format(
            display.getIndex(), display.getPixelResolution(), display.getCoordinateType()))
        self.hub.sendMessageEvent(text=u"Screen Calculated Pixels Per Degree (x, y): ({0}, {1}).".format(
            *display.getPixelsPerDegree()))
        self.hub.sendMessageEvent(text=u"=========== END INFO ===========")
        self.hub.sendMessageEvent(text=u"===== TESTS SEQUENCE START =====")
        # Experiment presentation
        sequence_index = 0
        sequence_count = len(execution[u"test_sequence"])
        while sequence_index < sequence_count:
            # Test selection
            test_index = execution[u"test_sequence"][sequence_index]
            test = execution[u"test_data"][test_index]
            # Pre-Test action
            if (execution[u"rest"][u"active"] and
                sequence_index > 0 and sequence_index%execution[u"rest"][u"period"] == 0
            ):
                text_scr.setText(text=u"Rest time:\n\n{0}[s]".format(execution[u"rest"][u"time"]))
                text_scr.draw()
                flip_time = win.flip()
                self.hub.sendMessageEvent(text=u"Rest Time (Test Count, Time[s]): ({0}, {1}).".format(
                    sequence_index, execution[u"rest"][u"time"]))
                core.wait(execution[u"rest"][u"time"])
                self.hub.sendMessageEvent(text=u"Rest Time Finished.")
            if execution[u"space_start"]:
                text_scr.setText(text=u"Test: {0}\n\nPress Space to Start Experiment.".format(test[u"name"]))
                text_scr.draw()
                flip_time = win.flip()
                self.hub.sendMessageEvent(text=u"Waiting User Input to Start Test (ID, Name): ({0}, {1}).".format(
                    test_index, test[u"name"]))
                self.hub.clearEvents(u"all")
                kb.waitForPresses(keys=[u" ", ])
                self.hub.sendMessageEvent(text=u"User Input Received.")
            # Test presentation
            timer = core.Clock()
            this_frame = None
            next_frame = None
            frame_index = -1
            frame_count = len(test[u"frames"])
            test_end = False
            test_state = u"buffer"
            self.hub.sendMessageEvent(text=u"Test Start (ID, Name): ({0}, {1}).".format(test_index, test[u"name"]))
            tracker.setRecordingState(True)
            while not test_end:
                with Switch(test_state) as case:
                    if case(u"buffer"):
                        next_index = frame_index + 1
                        if next_index < frame_count:
                            next_frame = test[u"frames"][next_index]
                            next_frame[u"background"].draw()
                            for component in next_frame[u"components"]:
                                component.draw()
                            self.hub.sendMessageEvent(text=u"Frame Loaded (ID, Name): ({0}, {1}).".format(
                                next_index, next_frame[u"name"]))
                        else:
                            self.hub.sendMessageEvent(text=u"No More Frames Available.")
                        test_state = u"flip" if next_index==0 else u"loop"
                    elif case(u"flip"):
                        if frame_index+1 == frame_count:
                            test_state = u"end"
                            break
                        this_frame = next_frame
                        frame_index += 1
                        if this_frame[u"is_task"]:
                            self.hub.sendMessageEvent(text=u"Frame Started (ID, Type, Time): ({0}, {1}, {2}).".format(
                                frame_index, u"Task", u"User dependent"))
                        else:
                            self.hub.sendMessageEvent(text=u"Frame Started (ID, Type, Time): ({0}, {1}, {2}).".format(
                                frame_index, u"Timed", this_frame[u"time"]))
                        flip_time = win.flip()
                        timer.reset()
                        if self.__frame_save:
                            frame_name = u"Test[{0}_{1}]_Frame[{2}_{3}].png".format(
                                test_index, test[u"name"], frame_index, this_frame[u"name"])
                            win.getMovieFrame()
                            win.saveMovieFrames(self.__frame_save_path+frame_name)
                        test_state = u"buffer"
                    elif case(u"loop"):
                        if this_frame[u"is_task"]:
                            key_pressed = kb.waitForPresses(keys=this_frame[u"allowed_keys"])
                            key_pressed = unicode(key_pressed[len(key_pressed)-1].key).replace(u" ", u"space")
                            self.hub.sendMessageEvent(text=u"Frame Ended ({0}): ({1})".format(
                                u"ID, Time, Selected Key, Correct Key", u"{0}, {1}, {2}, {3}".format(
                                    frame_index, timer.getTime(), key_pressed, this_frame[u"correct_keys_str"])))
                            test_state = u"flip"
                        elif timer.getTime() >= this_frame[u"time"]:
                            self.hub.sendMessageEvent(text=u"Frame Ended ({0}): ({1})".format(
                                u"ID, Time", u"{0}, {1}".format(frame_index, timer.getTime())))
                            test_state = u"flip"
                        if kb.getKeys(keys=[u"escape", u"q", ]):
                            self.hub.sendMessageEvent(text=u"== EXPERIMENT ENDED: BY USER  == ")
                            md = MessageDialog(title=u"Warning",
                                               msg=u"Experiment ended by user.",
                                               showButtons=MessageDialog.OK_BUTTON,
                                               dialogType=MessageDialog.ERROR_DIALOG,
                                               allowCancel=False, display_index=0)
                            md.show()
                            self.hub.quit()
                            win.close()
                            core.quit()
                    else:
                        test_end = True
            tracker.setRecordingState(False)
            self.hub.sendMessageEvent(text=u"Test End (ID, Name): ({0}, {1}).".format(test_index, test[u"name"]))
            sequence_index += 1
        # =======================================
        # Experiment exit
        # =======================================
        self.hub.sendMessageEvent(text=u"== EXPERIMENT ENDED: NORMALLY == ")
        self.hub.quit()
        win.close()
        core.quit()
