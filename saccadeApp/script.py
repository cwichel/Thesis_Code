# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
from psychopy import visual, core
from psychopy.data import TrialHandler, importConditions
from psychopy.iohub import (ioHubExperimentRuntime, module_directory, getCurrentDateTimeString)


# =============================================================================
# Script Handler
# =============================================================================
def generate_experiment(db, mas, exp):
    import time
    import yaml
    import codecs
    from saccadeApp import SaccadeDB, Master, Experiment
    # -----------------------
    if isinstance(db, SaccadeDB):
        mas_data = Master()
        mas_data.set_database(db=db)
        mas_check = mas_data.load(name=mas)
        # -------------------
        exp_data = Experiment()
        exp_data.set_database(db=db)
        exp_check = exp_data.load(code=exp)
        # -------------------
        if mas_check and exp_check:
            # ===================================
            # Configuration
            # ===================================
            mas_path = mas_data.get_experiment_path()
            exp_name = exp_data.get_name()
            exp_code = exp_data.get_code()
            exp_vers = exp_data.get_version()
            exp_time = unicode(int(time.time()))
            # ---------------
            exp_path = mas_path + u'\\' + exp_name
            exp_cod_path_base = exp_path + u'\\' + u'['+exp_vers+u']['+exp_code+u']'
            exp_cod_path_logs = exp_cod_path_base + u'\\' + u'logs'
            exp_cod_path_conf = exp_cod_path_base + u'\\' + u'config'
            # ---------------
            file_exp_config = u'['+exp_code+u']['+exp_time+u']experiment_config.yaml'
            file_exp_iohub_config = u'['+exp_code+u']['+exp_time+u']iohub_config.yaml'
            file_log_experiment = u'['+exp_code+u']['+exp_time+u']log_experiment_config.yaml'
            file_log_master = u'['+exp_code+u']['+exp_time+u']log_master_config.yaml'
            # ---------------
            if not os.path.exists(mas_path):
                os.makedirs(mas_path)
            if not os.path.exists(exp_path):
                os.makedirs(exp_path)
            if not os.path.exists(exp_cod_path_base):
                os.makedirs(exp_cod_path_base)
            if not os.path.exists(exp_cod_path_logs):
                os.makedirs(exp_cod_path_logs)
            if not os.path.exists(exp_cod_path_conf):
                os.makedirs(exp_cod_path_conf)
            # ---------------
            mas_config = mas_data.get_iohub()
            mas_config[u'data_store'][u'filename'] = exp_cod_path_base + u'\\' + u'['+exp_code+u']events_data'
            filepath = exp_cod_path_conf + u'\\' + file_exp_iohub_config
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(mas_config, outfile, default_flow_style=None, indent=4)
            # ---------------
            mas_log = mas_data.get_configuration()
            filepath = exp_cod_path_logs + u'\\' + file_log_master
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(mas_log, outfile, default_flow_style=False, indent=4)
            # ---------------
            exp_config = exp_data.get_iohub(unixstamp=exp_time)
            exp_config[u'ioHub'][u'config'] = exp_cod_path_conf + u'\\' + file_exp_iohub_config
            filepath = exp_cod_path_conf + u'\\' + file_exp_config
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(exp_config, outfile, default_flow_style=None, indent=4)
            # ---------------
            exp_log = exp_data.get_configuration()
            filepath = exp_cod_path_logs + u'\\' + file_log_experiment
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(exp_log, outfile, default_flow_style=False, indent=4)
            # ===================================
            # Execution
            # ===================================
            runtime = ExperimentRuntime(exp_cod_path_conf, file_exp_config, exp_data)
            runtime.start()
            return True
        else:
            return False
    else:
        return False


# =============================================================================
# Script
# =============================================================================
class ExperimentRuntime(ioHubExperimentRuntime):
    def __init__(self, conf_file_path, conf_file, experiment):
        super(ExperimentRuntime, self).__init__(configFilePath=conf_file_path, configFile=conf_file)
        self.experiment = experiment

    def run(self, *args):
        # =======================================
        # Prepare Hardware
        # =======================================
        try:
            tracker = self.hub.devices.tracker
            tracker.runSetupProcedure()
            tracker.setRecordingState(False)
        except Exception:
            from psychopy.iohub.util import MessageDialog
            md = MessageDialog(title=u"No Eye Tracker Configuration Found",
                               msg=u"No eyetracker selected/found. Check the" 
                                   u"experiment settings.",
                               showButtons=MessageDialog.OK_BUTTON,
                               dialogType=MessageDialog.ERROR_DIALOG,
                               allowCancel=False, display_index=0)
            md.show()
            return 1
        # -------------------
        display = self.hub.devices.display
        kb = self.hub.devices.keyboard

        # =======================================
        # Get experiment
        # =======================================
        # Prepare Window
        resolution = display.getPixelResolution()
        coordinate = display.getCoordinateType()
        window = visual.Window(size=resolution, monitor=display.getPsychopyMonitorName(), units=coordinate,
                               fullscr=True, allowGUI=False, screen=display.getIndex())

        # Get experiment content
        exp_data = self.experiment.get_execution(win=window)

        # Show instructions
        instruction_screen = visual.TextStim(window, text=u'', pos=(0, 0), height=24, color=u'white',
                                             alignHoriz=u'center', alignVert=u'center', wrapWidth=window.size[0] * 0.9)
        instruction_screen.setText(exp_data[u'instruction'] + u"\n\nPress Any Key to Start Experiment.")
        instruction_screen.draw()
        flip_time = window.flip()
        # -------------------
        self.hub.sendMessageEvent(text=u"=== EXPERIMENT START ===", sec_time=flip_time)
        self.hub.sendMessageEvent(text=u"========= INFO =========")
        self.hub.sendMessageEvent(text=u"Date:          {0}".format(getCurrentDateTimeString()))
        self.hub.sendMessageEvent(text=u"Experiment ID: {0}".format(self.hub.experimentID))
        self.hub.sendMessageEvent(text=u"Session    ID: {0}".format(self.hub.experimentSessionID))
        self.hub.sendMessageEvent(text=u"Screen (ID, Size, CoordType): ({0}, {1}, {2})".format(
            display.getIndex(), display.getPixelResolution(), display.getCoordinateType()))
        self.hub.sendMessageEvent(text=u"Screen calculated Pixels Per Degree: {0} x, {1} y".format(
            *display.getPixelsPerDegree()))
        self.hub.sendMessageEvent(text=u"======= END INFO =======")
        self.hub.clearEvents(u'all')
        # -------------------
        kb.waitForPresses()

        # =======================================
        # Experiment presentation
        # =======================================
        self.hub.sendMessageEvent(text=u"== TESTS SECUENCE START ==")
        # -------------------
        test_count = 0
        for test_index in exp_data[u'test_secuence'][:, 0]:
            test = exp_data[u'test_data'][test_index]
            # ===================================
            if exp_data[u'rest_active'] and test_count > 0 and test_count % exp_data[u'rest_period'] == 0:
                instruction_screen.setText(u"Rest time.")
                instruction_screen.draw()
                flip_time = window.flip()
                # -----------
                self.hub.sendMessageEvent(text=u"Rest time started...")
                core.wait(exp_data[u'rest_time'])
                self.hub.sendMessageEvent(text=u"Rest time finished.")
            # ---------------
            if exp_data[u'space_start']:
                instruction_screen.setText(u"Test: "+test[u'name']+u"\n\nPress Space to Start Experiment.")
                instruction_screen.draw()
                flip_time = window.flip()
                # -----------
                self.hub.sendMessageEvent(text=u"Waiting user input to start Test (ID:{0} , Name: {1})".format(
                    test_index, test[u'name']))
                self.hub.clearEvents(u'all')
                kb.waitForPresses(keys=[u' ', ])
            # ===================================
            timer = core.Clock()
            # ---------------
            frames = test[u'frames']
            frame_index = 0
            frame_buffer_index = -1
            frame_total = len(frames)
            # ---------------
            state = u'buffer'
            frame = None
            frame_buffer = None
            is_last_frame = False
            is_first_frame = True
            is_test_finish = False
            # ---------------
            self.hub.sendMessageEvent(text=u"Starting Test (ID:{0} , Name: {1})".format(test_index, test[u'name']))
            # ---------------
            tracker.setRecordingState(True)
            while not is_test_finish:
                with Switch(state) as case:
                    if case(u'buffer'):
                        frame_buffer_index += 1
                        if frame_buffer_index < frame_total:
                            self.hub.sendMessageEvent(text=u"Loading Frame (ID: {0})".format(frame_buffer_index))
                            self.hub.sendMessageEvent(text=u"Loading Frame Components...")
                            # ---------
                            frame_buffer = frames[frame_buffer_index]
                            frame_buffer[u'background'].draw()
                            if frame_buffer[u'components'] is not None:
                                for component in frame_buffer[u'components']:
                                    component.draw()
                        else:
                            self.hub.sendMessageEvent(text=u"No more frames to load...")
                            is_last_frame = True
                        # -------------
                        if is_first_frame:
                            is_first_frame = False
                            state = u'flip'
                        else:
                            state = u'loop'

                    elif case(u'flip'):
                        if is_last_frame:
                            state = u'end'
                        else:
                            frame = frame_buffer
                            frame_index = frame_buffer_index
                            # ---------
                            self.hub.sendMessageEvent(text=u"Frame Started (ID: {0})".format(frame_index))
                            # ---------
                            flip_time = window.flip()
                            timer.reset()
                            state = u'buffer'

                    elif case(u'loop'):
                        if frame[u'is_task']:                           # is a selection frame
                            pressed = kb.waitForPresses(keys=frame[u'allowed_keys'])
                            key = unicode(pressed[len(pressed)-1].key).replace(u' ', u'space')
                            # ---------
                            self.hub.sendMessageEvent(text=u"Frame Ended (ID: {0}, Time:{1}, "
                                                           u"Selected key: {2}, Correct key: {3})".format(
                                frame_index, timer.getTime(), key, frame[u'correct_keys_str']))
                            # ---------
                            state = u'flip'

                        elif timer.getTime() >= frame[u'time']:         # is a timed frame
                            self.hub.sendMessageEvent(text=u"Frame Ended (ID: {0}, Time:{1})".format(
                                frame_index, timer.getTime()))
                            # ---------
                            state = u'flip'

                        # -------------
                        if kb.getKeys(keys=[u'escape', u'q', ]):
                            self.hub.sendMessageEvent(text=u"== EXPERIMENT ENDED BY USER == ")
                            self.hub.quit()
                            window.close()
                            core.quit()
                            return 0

                        # -------------
                        self.hub.clearEvents(u'all')

                    elif case(u'end'):
                        self.hub.sendMessageEvent(text=u"Ending Test (ID:{0} , Name: {1})".format(
                            test_index, test[u'name']))
                        # ---------
                        is_test_finish = True

            # ===================================
            tracker.setRecordingState(False)
            # ---------------
            test_count += 1

        # =======================================
        # Experiment exit
        # =======================================
        self.hub.sendMessageEvent(text=u"== EXPERIMENT ENDED NORMALLY == ")
        window.close()
        core.quit()


# =====================================
class Switch:
    def __init__(self, value):
        self._val = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):  # Allows traceback to occur
        return False

    def __call__(self, *mconds):
        return self._val in mconds

