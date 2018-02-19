# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
from psychopy import visual, core
from psychopy.iohub import (ioHubExperimentRuntime, getCurrentDateTimeString)


# =============================================================================
# Script Handler
# =============================================================================
class ExperimentHandler(object):
    # =================================
    def __init__(self):
        self.__database = None
        self.__mas_data = None
        self.__exp_data = None
        self.__exp_exec = {}
        self.__exp_path = u''
        self.__base_path = u''
        self.__timestamp = u''
        self.__is_loaded = False
        self.__is_ready = False

    # =================================
    def load_experiment(self, db, mas, exp):
        import time
        from saccadeApp import SaccadeDB, Master, Experiment
        # -----------------------
        if not self.__is_loaded:
            if isinstance(db, SaccadeDB):
                self.__mas_data = Master()
                self.__mas_data.set_database(db=db)
                mas_check = self.__mas_data.load(name=mas)
                # -------------------
                self.__exp_data = Experiment()
                self.__exp_data.set_database(db=db)
                exp_check = self.__exp_data.load(code=exp)
                # -------------------
                if mas_check and exp_check:
                    self.__is_loaded = True
                    self.__timestamp = unicode(int(time.time()))
                    # ---------------
                    self.__base_path = self.__mas_data.get_experiment_path()
                    self.__exp_path = self.__base_path + u'\\' + self.__exp_data.get_name()
                # -------------------
                return self.__is_loaded
        else:
            return self.__is_loaded

    def save_execution_parameters(self):
        import yaml
        import codecs
        # -------------------
        if self.__is_loaded and not self.__is_ready:
            exp_code = self.__exp_data.get_code()
            exp_version = self.__exp_data.get_version()
            # ---------------
            exp_version_path = self.__exp_path + u'\\' + u'['+exp_version+u']['+exp_code+u']'
            exp_version_log_path = exp_version_path + u'\\logs'
            exp_version_cfg_path = exp_version_path + u'\\config'
            # ---------------
            if not os.path.exists(self.__base_path):
                os.makedirs(self.__base_path)
            if not os.path.exists(self.__exp_path):
                os.makedirs(self.__exp_path)
            if not os.path.exists(exp_version_path):
                os.makedirs(exp_version_path)
            if not os.path.exists(exp_version_log_path):
                os.makedirs(exp_version_log_path)
            if not os.path.exists(exp_version_cfg_path):
                os.makedirs(exp_version_cfg_path)
            # ---------------
            exp_logfile_config = u'['+exp_code+u']['+self.__timestamp+u']log_experiment_config.yaml'
            exp_logfile_master = u'['+exp_code+u']['+self.__timestamp+u']log_master_config.yaml'
            exp_cfgfile_config = u'['+exp_code+u']['+self.__timestamp+u']experiment_config.yaml'
            exp_cfgfile_iohub = u'[' + exp_code + u'][' + self.__timestamp + u']iohub_config.yaml'
            # ---------------
            mas_config = self.__mas_data.get_iohub()
            mas_config[u'data_store'][u'filename'] = exp_version_path + u'\\' + u'[' + exp_code + u']events_data'
            filepath = exp_version_cfg_path + u'\\' + exp_cfgfile_iohub
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(mas_config, outfile, default_flow_style=None, indent=4)
            # ---------------
            mas_log = self.__mas_data.get_configuration()
            filepath = exp_version_log_path + u'\\' + exp_logfile_master
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(mas_log, outfile, default_flow_style=False, indent=4)
            # ---------------
            exp_config = self.__exp_data.get_iohub(unixstamp=self.__timestamp)
            exp_config[u'ioHub'][u'config'] = exp_version_cfg_path + u'\\' + exp_cfgfile_iohub
            filepath = exp_version_cfg_path + u'\\' + exp_cfgfile_config
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(exp_config, outfile, default_flow_style=None, indent=4)
            # ---------------
            exp_log = self.__exp_data.get_configuration()
            filepath = exp_version_log_path + u'\\' + exp_logfile_config
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(exp_log, outfile, default_flow_style=False, indent=4)
            # ---------------
            self.__exp_exec[u'experiment_config_path'] = exp_version_cfg_path
            self.__exp_exec[u'experiment_config_file'] = exp_cfgfile_config
            self.__exp_exec[u'experiment_data'] = self.__exp_data
            # -------------------
            self.__is_ready = True
            return self.__is_ready
        else:
            return self.__is_loaded

    def execute_experiment(self):
        if self.__is_loaded and self.__is_ready:
            runtime = ExperimentRuntime(self.__exp_exec)
            runtime.start()
            # ---------------
            return True
        else:
            return False


# =============================================================================
# Script
# =============================================================================
class ExperimentRuntime(ioHubExperimentRuntime):
    def __init__(self, exp_cfg_dict):
        super(ExperimentRuntime, self).__init__(configFilePath=exp_cfg_dict[u'experiment_config_path'],
                                                configFile=exp_cfg_dict[u'experiment_config_file'])
        self.__experiment = exp_cfg_dict[u'experiment_data']

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
        exp_data = self.__experiment.get_execution(win=window)

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

    def __exit__(self, swt_type, value, traceback):  # Allows traceback to occur
        return False

    def __call__(self, *mconds):
        return self._val in mconds

