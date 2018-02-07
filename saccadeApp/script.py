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
        # ===================
        # Prepare Hardware
        # ===================
        try:
            tracker = self.hub.devices.tracker
            tracker.runSetupProcedure()
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

        # ===================
        # Get experiment
        # ===================
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
        instruction_screen.setText(exp_data[u'instruction'] + u"\nPress Any Key to Start Experiment.")
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

        # ===================
        # Experiment presentation
        # ===================
        self.hub.sendMessageEvent(text=u"= TESTS SECUENCE START =")
        self.hub.clearEvents(u'all')
        # -------------------
        for test_index in exp_data[u'test_secuence'][:, 0]:
            test = exp_data[u'test_data'][test_index]
            instruction_screen.setText(test[u'name']+u"\nPress Space to Start Experiment.")
            instruction_screen.draw()
            flip_time = window.flip()
            # ---------------
            kb.waitForPresses(keys=[u' ', ])
            # ---------------
            for frame in test[u'frames']:
                frame[u'background'].draw()
                if frame[u'components'] is not None:
                    for component in frame[u'components']:
                        component.draw()
                window.flip()
                core.wait(1.5)





        # t = 0
        # for trial in trials:
        #     # Update the instruction screen text to indicate
        #     # a trial is about to start.
        #     #
        #     instuction_text = u"Press Space Key To Start Trial %d"%t
        #     instructions_text_stim.setText(instuction_text)
        #     instructions_text_stim.draw()
        #     flip_time = window.flip()
        #
        #     self.hub.sendMessageEvent(text=u"EXPERIMENT_START", sec_time=flip_time)
        #
        #
        #     # Wait until a space key press event occurs after the
        #     # start trial instuctions have been displayed.
        #     #
        #     self.hub.clearEvents(u'all')
        #     kb.waitForPresses(keys=[u' ', ])
        #
        #
        #     # Space Key has been pressed, start the trial.
        #     # Set the current session and trial id values to be saved
        #     # in the ioDataStore for the upcoming trial.
        #     #
        #
        #     trial[u'session_id'] = self.hub.getSessionID()
        #     trial[u'trial_id'] = t+1
        #
        #     # Send a msg to the ioHub indicating that the trial started, and the time of
        #     # the first retrace displaying the trial stm.
        #     #
        #     self.hub.sendMessageEvent(text=u"TRIAL_START", sec_time=flip_time)
        #
        #
        #     # Start Recording Eye Data
        #     #
        #     tracker.setRecordingState(True)
        #
        #     # Get the image stim for this trial.
        #     imageStim = image_cache[trial[u'IMAGE_NAME']]
        #     imageStim.draw()
        #     flip_time=window.flip()
        #     # Clear all the events received prior to the trial start.
        #     #
        #     self.hub.clearEvents(u'all')
        #     # Send a msg to the ioHub indicating that the trial started,
        #     # and the time of the first retrace displaying the trial stim.
        #     #
        #     self.hub.sendMessageEvent(text=u"TRIAL_START", sec_time=flip_time)
        #     # Set the value of the trial start variable for this trial
        #     #
        #     trial[u'TRIAL_START']=flip_time
        #
        #     # Loop until we get a keyboard event
        #     #
        #     run_trial = True
        #     while run_trial is True:
        #         # Get the latest gaze position in display coord space..
        #         #
        #         gpos=tracker.getPosition()
        #         if type(gpos) in [tuple,list]:
        #             # If we have a gaze position from the tracker,
        #             # redraw the background image and then the
        #             # gaze_cursor at the current eye position.
        #             #
        #             gaze_dot.setPos([gpos[0],gpos[1]])
        #             imageStim.draw()
        #             gaze_dot.draw()
        #         else:
        #             # Otherwise just draw the background image.
        #             # This will remove the gaze cursor from the screen
        #             # when the eye tracker is not successfully
        #             # tracking eye position.
        #             #
        #             imageStim.draw()
        #
        #         # Flip video buffers, displaying the stim we just
        #         # updated.
        #         #
        #         flip_time=window.flip()
        #
        #         # Send an experiment message to the ioDataStore
        #         # indicating the time the image was drawn and
        #         # current position of gaze spot.
        #         #
        #         if type(gpos) in [tuple,list]:
        #             self.hub.sendMessageEvent("IMAGE_UPDATE %s %.3f %.3f"%(
        #                                         trial['IMAGE_NAME'],gpos[0],gpos[1]),
        #                                         sec_time=flip_time)
        #         else:
        #             self.hub.sendMessageEvent("IMAGE_UPDATE %s [NO GAZE]"%(
        #                                         trial['IMAGE_NAME']),
        #                                         sec_time=flip_time)
        #
        #         # Check any new keyboard press events by a space key.
        #         # If one is found, set the trial end variable and break.
        #         # from the loop
        #         if kb.getPresses(keys=[' ',]):
        #             run_trial=False
        #             break
        #
        #     # The trial has ended, so update the trial end time condition value,
        #     # and send a message to the ioDataStore with the trial end time.
        #     #
        #     flip_time=window.flip()
        #     trial['TRIAL_END']=flip_time
        #     self.hub.sendMessageEvent(text="TRIAL_END %d"%t,sec_time=flip_time)
        #
        #     # Stop recording eye data.
        #     # In this example, we have no use for any eye data
        #     # between trials, so why save it.
        #     #
        #     tracker.setRecordingState(False)
        #
        #     # Save the experiment condition variable values for this
        #     # trial to the ioDataStore.
        #     #
        #     self.hub.addRowToConditionVariableTable(trial.values())
        #
        #     # Clear all event buffers
        #     #
        #     self.hub.clearEvents('all')
        #     t+=1
        #
        # # All trials have been run, so end the experiment.
        # #
        #
        # flip_time=window.flip()
        # self.hub.sendMessageEvent(text='EXPERIMENT_COMPLETE',sec_time=flip_time)
        #
        # # Disconnect the eye tracking device.
        # #
        # tracker.setConnectionState(False)
        #
        # # The experiment is done, all trials have been run.
        # # Clear the screen and show an 'experiment  done' message using the
        # # instructionScreen text.
        # #
        # instuction_text="Press Any Key to Exit Demo"
        # instructions_text_stim.setText(instuction_text)
        # instructions_text_stim.draw()
        # flip_time=window.flip()
        # self.hub.sendMessageEvent(text="SHOW_DONE_TEXT",sec_time=flip_time)
        # self.hub.clearEvents('all')
        # # wait until any key is pressed
        # kb.waitForPresses()

