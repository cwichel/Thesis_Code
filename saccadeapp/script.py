# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import os
import platform
from psychopy import visual, core
from psychopy.iohub import (ioHubExperimentRuntime, getCurrentDateTimeString)

if any(platform.win32_ver()):
    fold = u'\\'
else:
    fold = u'/'


# =============================================================================
# Script Handler
# =============================================================================
class ExperimentHandler(object):
    # =================================
    def __init__(self):
        self.__database = None
        self.__master = None
        self.__experiment = None
        # ==================
        self.__base_path = u''
        self.__exp_path = u''
        self.__exp_version_path = u''
        # ==================
        self.__execution_parameters = dict()
        self.__execution_timestamp = u''
        # ==================
        self.__is_loaded = False
        self.__is_ready = False

    # =================================
    def load_configuration(self, db, master, experiment):
        import time
        from saccadeapp import SaccadeDB, Master, Experiment
        # ===================
        if not self.__is_loaded:
            if isinstance(db, SaccadeDB):
                self.__master = Master()
                self.__master.set_database(db=db)
                is_master = self.__master.load(name=master)
                # ===========
                self.__experiment = Experiment()
                self.__experiment.set_database(db=db)
                is_experiment = self.__experiment.load(code=experiment)
                # ===========
                if is_master and is_experiment:
                    self.__is_loaded = True
                    self.__execution_timestamp = unicode(int(time.time()))
                    self.__base_path = self.__master.get_experiment_path()
                    self.__exp_path = self.__base_path + u'\\' + self.__experiment.get_name()
                return self.__is_loaded
        else:
            return self.__is_loaded

    def save_parameters(self, save_frame=False):
        import yaml
        import codecs
        # ===================
        if self.__is_loaded and not self.__is_ready:
            experiment_code = self.__experiment.get_code()
            experiment_version = self.__experiment.get_version()
            # ===============
            self.__exp_version_path = self.__exp_path + fold + u'['+experiment_version+u']['+experiment_code+u']'
            log_files_path = self.__exp_version_path + fold + u'logs'
            cfg_files_path = self.__exp_version_path + fold + u'config'
            # ===============
            if not os.path.exists(self.__base_path):
                os.makedirs(self.__base_path)
            if not os.path.exists(self.__exp_path):
                os.makedirs(self.__exp_path)
            if not os.path.exists(self.__exp_version_path):
                os.makedirs(self.__exp_version_path)
            if not os.path.exists(log_files_path):
                os.makedirs(log_files_path)
            if not os.path.exists(cfg_files_path):
                os.makedirs(cfg_files_path)
            # ===============
            cfg_experiment = u'['+experiment_code+u']['+self.__execution_timestamp+u']experiment_config.yaml'
            cfg_iohub = u'['+experiment_code+u']['+self.__execution_timestamp+u']iohub_config.yaml'
            log_data = u'['+experiment_code+u']['+self.__execution_timestamp+u']config_log.yaml'
            # ===============
            cfg_exp_data = self.__experiment.get_iohub()
            cfg_exp_data[u'ioHub'][u'config'] = cfg_files_path + fold + cfg_iohub
            cfg_exp_data[u'session_defaults'][u'code'] = self.__execution_timestamp
            # ---------------
            filepath = cfg_files_path + fold + cfg_experiment
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(cfg_exp_data, outfile, default_flow_style=None, indent=4)
            # ===============
            cfg_mas_data = self.__master.get_iohub()
            cfg_mas_data[u'data_store'][u'filename'] = self.__exp_version_path + fold +\
                                                       u'['+experiment_code+u']events_data'
            # ---------------
            filepath = cfg_files_path + fold + cfg_iohub
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(cfg_mas_data, outfile, default_flow_style=None, indent=4)
            # ===============
            execution_log = dict()
            execution_log[u'experiment'] = self.__experiment.get_configuration()
            execution_log[u'master'] = self.__master.get_configuration()
            # ---------------
            filepath = log_files_path + fold + log_data
            with codecs.open(filename=filepath, mode=u'w', encoding=u'utf-8') as outfile:
                yaml.safe_dump(execution_log, outfile, default_flow_style=False, indent=4)
            # ===============
            self.__execution_parameters[u'execution_configuration_path'] = cfg_files_path
            self.__execution_parameters[u'execution_configuration_file'] = cfg_experiment
            self.__execution_parameters[u'execution_base_path'] = self.__exp_version_path
            self.__execution_parameters[u'experiment'] = self.__experiment
            self.__execution_parameters[u'save_frame'] = save_frame
            self.__is_ready = True
            return self.__is_ready
        else:
            return self.__is_loaded

    def execute_experiment(self):
        if self.__is_loaded and self.__is_ready:
            runtime = ExperimentRuntime(execution_parameters=self.__execution_parameters)
            runtime.start()
            # ---------------
            return True
        else:
            return False


# =============================================================================
# Script
# =============================================================================
class ExperimentRuntime(ioHubExperimentRuntime):
    # =================================
    def __init__(self, execution_parameters):
        super(ExperimentRuntime, self).__init__(configFilePath=execution_parameters[u'execution_configuration_path'],
                                                configFile=execution_parameters[u'execution_configuration_file'])
        self.__experiment = execution_parameters[u'experiment']
        self.__save_frame = execution_parameters[u'save_frame']
        if self.__save_frame:
            self.__frame_path = execution_parameters[u'execution_base_path'] + fold + u'frames'
            if not os.path.isdir(self.__frame_path):
                os.mkdir(self.__frame_path)
        else:
            self.__frame_path = None

    # =================================
    def run(self, *args):
        from switch import Switch
        # =============================
        # Prepare Hardware
        # =============================
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
        # ===================
        display = self.hub.devices.display
        kb = self.hub.devices.keyboard
        # =============================
        # Get experiment
        # =============================
        # Prepare Window
        resolution = display.getPixelResolution()
        coordinate = display.getCoordinateType()
        window = visual.Window(size=resolution, monitor=display.getPsychopyMonitorName(), units=coordinate,
                               fullscr=True, allowGUI=False, screen=display.getIndex())
        # Get experiment content
        execution = self.__experiment.get_execution(win=window)
        # Show instructions
        instruction_screen = visual.TextStim(window, text=u'', pos=(0, 0), height=24, color=u'white',
                                             alignHoriz=u'center', alignVert=u'center', wrapWidth=window.size[0] * 0.9)
        instruction_screen.setText(execution[u'instruction'] + u"\n\nPress Any Key to Start Experiment.")
        instruction_screen.draw()
        flip_time = window.flip()
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
        kb.waitForPresses()
        # =============================
        # Experiment presentation
        # =============================
        self.hub.sendMessageEvent(text=u"== TESTS SECUENCE START ==")
        test_count = 0
        for test_index in execution[u'test_secuence'][:, 0]:
            test = execution[u'test_data'][test_index]
            if execution[u'rest_active'] and test_count > 0 and test_count % execution[u'rest_period'] == 0:
                instruction_screen.setText(u"Rest time.")
                instruction_screen.draw()
                flip_time = window.flip()
                self.hub.sendMessageEvent(text=u"Rest time started...")
                core.wait(execution[u'rest_time'])
                self.hub.sendMessageEvent(text=u"Rest time finished.")
            if execution[u'space_start']:
                instruction_screen.setText(u"Test: "+test[u'name']+u"\n\nPress Space to Start Experiment.")
                instruction_screen.draw()
                flip_time = window.flip()
                self.hub.sendMessageEvent(text=u"Waiting user input to start Test (ID:{0} , Name: {1})".format(
                    test_index, test[u'name']))
                self.hub.clearEvents(u'all')
                kb.waitForPresses(keys=[u' ', ])
            timer = core.Clock()
            frames = test[u'frames']
            frame_index = 0
            frame_buffer_index = -1
            frame_total = len(frames)
            state = u'buffer'
            frame = None
            frame_buffer = None
            is_last_frame = False
            is_first_frame = True
            is_test_finish = False
            self.hub.sendMessageEvent(text=u"Starting Test (ID:{0} , Name: {1})".format(test_index, test[u'name']))
            tracker.setRecordingState(True)
            while not is_test_finish:
                with Switch(state) as case:
                    if case(u'buffer'):
                        frame_buffer_index += 1
                        if frame_buffer_index < frame_total:
                            self.hub.sendMessageEvent(text=u"Loading Frame (ID: {0})".format(frame_buffer_index))
                            frame_buffer = frames[frame_buffer_index]
                            frame_buffer[u'background'].draw()
                            if frame_buffer[u'components'] is not None:
                                for component in frame_buffer[u'components']:
                                    component.draw()
                        else:
                            self.hub.sendMessageEvent(text=u"No more frames to load...")
                            is_last_frame = True
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
                            if frame[u'is_task']:
                                self.hub.sendMessageEvent(
                                    text=u"Frame Started (ID: {0}, Type: Task, Time: User dependent.)"
                                    .format(frame_index))
                            else:
                                self.hub.sendMessageEvent(
                                    text=u"Frame Started (ID: {0}, Type: Timed, Time: {1}.)"
                                    .format(frame_index, frame[u'time']))
                            flip_time = window.flip()
                            timer.reset()
                            state = u'buffer'
                            if self.__save_frame:
                                frame_name = u"test{0}_frame{1}.png".format(test_index, frame_index)
                                window.getMovieFrame()
                                window.saveMovieFrames(self.__frame_path + fold + frame_name)
                    elif case(u'loop'):
                        if frame[u'is_task']:                           # is a selection frame
                            pressed = kb.waitForPresses(keys=frame[u'allowed_keys'])
                            key = unicode(pressed[len(pressed)-1].key).replace(u' ', u'space')
                            self.hub.sendMessageEvent(
                                text=u"Frame Ended (ID: {0}, Time:{1}, Selected key: {2}, Correct key: {3})"
                                .format(frame_index, timer.getTime(), key, frame[u'correct_keys_str']))
                            state = u'flip'
                        elif timer.getTime() >= frame[u'time']:         # is a timed frame
                            self.hub.sendMessageEvent(
                                text=u"Frame Ended (ID: {0}, Time:{1})"
                                .format(frame_index, timer.getTime()))
                            state = u'flip'
                        if kb.getKeys(keys=[u'escape', u'q', ]):
                            self.hub.sendMessageEvent(text=u"== EXPERIMENT ENDED BY USER == ")
                            self.hub.quit()
                            window.close()
                            core.quit()
                            return 0
                        self.hub.clearEvents(u'all')

                    elif case(u'end'):
                        self.hub.sendMessageEvent(
                            text=u"Ending Test (ID:{0} , Name: {1})"
                            .format(test_index, test[u'name']))
                        is_test_finish = True
            tracker.setRecordingState(False)
            test_count += 1
        # =======================================
        # Experiment exit
        # =======================================
        self.hub.sendMessageEvent(text=u"== EXPERIMENT ENDED NORMALLY == ")
        window.close()
        core.quit()


# =====================================


