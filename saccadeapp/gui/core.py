# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import sys
from models import *
from saccadeapp.api import *


# =============================================================================
# Aux Functions
# =============================================================================
def get_compiled_ui(file_name):
    from PyQt4.uic import loadUiType
    base_path = format_path(get_module_path()+u"/gui/resources/")
    base, form = loadUiType(base_path+file_name)
    return base, form


def check_item_name(item_parent, item, old_name=u""):
    new_name = item.get_name()
    is_edit = True if old_name != u"" else False
    index = item_parent.check_item_name(item_name=old_name) if is_edit else -1
    if is_edit and (new_name == old_name or item_parent.check_item_name(item_name=new_name) == -1):
        item_parent.item_replace(item_id=index, new_item=item)
    elif not is_edit and item_parent.check_item_name(item_name=new_name) == -1:
        index = item_parent.get_items_length()
        item_parent.item_add(item=item)
    else:
        index = -1
        diag_tit = u"Error"
        diag_msg = u"Name already used."
        QtGui.QMessageBox.warning(None, diag_tit, diag_msg)
    return index


# =============================================================================
# Qt GUI Modules
# =============================================================================
base_main, form_main = get_compiled_ui(u"saccadeApp.ui")
base_exp, form_exp = get_compiled_ui(u"experiment.ui")
base_tes, form_tes = get_compiled_ui(u"test.ui")
base_tes_seq, form_tes_seq = get_compiled_ui(u"test_sequence.ui")
base_fra, form_fra = get_compiled_ui(u"frame.ui")
base_com, form_com = get_compiled_ui(u"component.ui")
base_con, form_con = get_compiled_ui(u"configuration.ui")
base_copy_exp, form_copy_exp = get_compiled_ui(u"copy_experiment.ui")
base_copy, form_copy = get_compiled_ui(u"copy_item.ui")                 # Used for: ItemList objects, Configuration
base_about, form_about = get_compiled_ui(u"about.ui")


# =============================================================================
# Main App Class: saccadeapp
# =============================================================================
class SaccadeApp(base_main, form_main):
    def __init__(self):
        super(SaccadeApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.database = SaccadeDB()
        self.model_configuration = ListModel(items=[], header=u"Profile")
        self.model_experiment_tab = TableModel(items=[], header=[u"Name", u"Code"])
        self.model_experiment_tree = ExperimentTreeModel(items=None)
        # -------------------
        self.__setup_menu()
        self.__setup_tabs()

    # =================================
    def __setup_menu(self):
        self.mac_documentation.triggered.connect(self.__app_documentation)
        self.mac_about.triggered.connect(self.__app_about)
        self.mac_exit.triggered.connect(self.__app_close)

    @staticmethod
    def __app_documentation():
        open_documentation()

    @staticmethod
    def __app_about():
        dialog = AboutApp()
        dialog.exec_()

    @staticmethod
    def __app_close():
        sys.exit()

    # =================================
    def __setup_tabs(self):
        # Experiment Tab
        self.pbt_experiment_new.clicked.connect(self.__handle_experiment_new)
        self.pbt_experiment_edit.clicked.connect(self.__handle_experiment_edit)
        self.pbt_experiment_copy.clicked.connect(self.__handle_experiment_copy)
        self.pbt_experiment_remove.clicked.connect(self.__handle_experiment_remove)
        self.trv_experiment.setModel(self.model_experiment_tree)
        self.trv_experiment.setColumnWidth(0, 160)
        self.trv_experiment.setColumnWidth(1, 120)
        self.trv_experiment.setColumnWidth(2, 120)
        # Configuration Tab
        self.pbt_monitor_center.clicked.connect(self.__handle_monitor_center)
        self.pbt_configuration_new.clicked.connect(self.__handle_configuration_new)
        self.pbt_configuration_edit.clicked.connect(self.__handle_configuration_edit)
        self.pbt_configuration_copy.clicked.connect(self.__handle_configuration_copy)
        self.pbt_configuration_remove.clicked.connect(self.__handle_configuration_remove)
        self.lsv_configuration.setModel(self.model_configuration)
        # Execution Tab
        self.pbt_execute.clicked.connect(self.__handle_execute_experiment)
        self.cmb_execution_experiment.setModel(self.model_experiment_tab)
        self.cmb_execution_configuration.setModel(self.model_configuration)
        # Model update
        self.update_experiment_model()
        self.update_configuration_model()
        if self.model_configuration.rowCount() > 0:
            self.lsv_configuration.setCurrentIndex(self.model_configuration.index(0, 0))
        if self.model_experiment_tab.rowCount() > 0:
            base_index = self.model_experiment_tree.index(0, 0, QtCore.QModelIndex())
            self.trv_experiment.setCurrentIndex(self.model_experiment_tree.index(0, 0, base_index))

    def update_configuration_model(self):
        conf_list = Configuration.get_list(db=self.database)
        if conf_list is not None:
            conf_list = [item[0] for item in conf_list]
            self.model_configuration.update_items(items=conf_list)
        else:
            self.model_configuration.update_items(items=[])
        self.cmb_execution_configuration.setCurrentIndex(0)

    def update_experiment_model(self):
        experiment_list = Experiment.get_list(db=self.database)
        experiment_names = []
        root_node = ExperimentNode(mask=u"Experiments") if experiment_list else None
        if experiment_list:
            exp_name = u""
            base_node = root_node
            for item in experiment_list:
                experiment_names.append([item[1][0]+u" "+item[1][1], item[0]])
                if exp_name != item[1][0]:
                    exp_name = item[1][0]
                    base_node = ExperimentNode(mask=exp_name, parent=root_node)
                new_node = ExperimentNode(mask=item[1][1], code=item[0], date=item[2], parent=base_node)
        self.model_experiment_tab.update_items(items=experiment_names)
        self.model_experiment_tree.update_items(node=root_node)
        self.trv_experiment.expandAll()
        self.cmb_execution_experiment.setCurrentIndex(0)

    # =================================
    def __get_execution_parameters(self):
        exp_code = u"None"
        cfg_name = u"None"
        if self.model_experiment_tab.rowCount() > 0:
            exp_index = self.cmb_execution_experiment.currentIndex()
            exp_code = unicode(self.model_experiment_tab.get_item(index=exp_index)[1])
        if self.model_configuration.rowCount() > 0:
            cfg_name = unicode(self.cmb_execution_configuration.currentText())
        fra_save = unicode(self.cbt_execution_save.isChecked())
        return exp_code, cfg_name, fra_save

    def __handle_execute_experiment(self):
        import subprocess as sp
        exp_code, cfg_name, fra_save = self.__get_execution_parameters()
        execution_path = format_path(get_module_path()+u"/api/resources/subprocess/experimentExecution.py")
        sp.call([u"python", execution_path, u"-e", exp_code, u"-c", cfg_name, u"-f", fra_save])

    # =================================
    def __handle_experiment_new(self):
        dialog = ExperimentApp(parent=self)
        dialog.exec_()

    def __handle_experiment_edit(self):
        this_node = self.model_experiment_tree.get_node(index=self.trv_experiment.currentIndex())
        if this_node is not None and this_node.get_code() is not None:
            dialog = ExperimentApp(parent=self, experiment_code=unicode(this_node.get_code()))
            dialog.exec_()

    def __handle_experiment_copy(self):
        this_node = self.model_experiment_tree.get_node(index=self.trv_experiment.currentIndex())
        if this_node is not None and this_node.get_code() is not None:
            dialog = CopyExperimentApp(parent=self, experiment_code=this_node.get_code())
            dialog.exec_()

    def __handle_experiment_remove(self):
        this_node = self.model_experiment_tree.get_node(index=self.trv_experiment.currentIndex())
        if this_node is not None and this_node.get_code() is not None:
            parent_node = this_node.get_parent()
            name = parent_node.get_mask()
            version = this_node.get_mask()
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\nexperiment (%s %s)?" % (name, version)
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                experiment = Experiment(db=self.database, code=this_node.get_code())
                experiment.remove()
                self.update_experiment_model()

    # =================================
    def __handle_monitor_center(self):
        open_psychopy_monitor_center()

    def __handle_configuration_new(self):
        dialog = ConfigurationApp(parent=self, profile_name=u"")
        dialog.exec_()

    def __handle_configuration_edit(self):
        index = self.lsv_configuration.currentIndex().row()
        if index != -1:
            profile = self.model_configuration.get_item(index)
            dialog = ConfigurationApp(parent=self, profile_name=profile)
            dialog.exec_()

    def __handle_configuration_copy(self):
        index = self.lsv_configuration.currentIndex().row()
        if index != -1:
            dialog = CopyConfigurationApp(parent=self, profile_name=self.model_configuration.get_item(index=index))
            dialog.exec_()

    def __handle_configuration_remove(self):
        index = self.lsv_configuration.currentIndex().row()
        if index != -1:
            name = self.model_configuration.get_item(index=index)
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\nconfiguration profile (%s)?" % name
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                profile = Configuration(db=self.database, name=name)
                profile.remove()
                self.update_configuration_model()
                new_index = index-1 if index > 0 else 0
                self.lsv_configuration.setCurrentIndex(self.model_configuration.index(new_index, 0))


# =============================================================================
# Experiment related Classes:
# =============================================================================
# ===============================================
# Class: ExperimentApp
# ===============================================
class ExperimentApp(base_exp, form_exp):
    def __init__(self, parent=SaccadeApp, experiment_code=u""):
        super(ExperimentApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__parent = parent
        self.__is_edit = False
        self.__experiment = Experiment(db=parent.database)
        # -------------------
        self.model_test_data = ListModel(items=[], header=u"Test")
        self.model_test_sequence = TableModel(items=[], header=[u"Test", u"Qty"])
        # -------------------
        self.__setup_experiment()
        self.__check_code(code=experiment_code)

    # =================================
    def __setup_experiment(self):
        self.pbt_save.clicked.connect(self.__handle_save_action)
        self.pbt_cancel.clicked.connect(self.close)
        self.pbt_dat_new.clicked.connect(self.__handle_test_new)
        self.pbt_dat_edit.clicked.connect(self.__handle_test_edit)
        self.pbt_dat_copy.clicked.connect(self.__handle_test_copy)
        self.pbt_dat_remove.clicked.connect(self.__handle_test_remove)
        self.pbt_dat_up.clicked.connect(self.__handle_test_move_up)
        self.pbt_dat_down.clicked.connect(self.__handle_test_move_down)
        self.pbt_seq_add.clicked.connect(self.__handle_sequence_add)
        self.pbt_seq_edit.clicked.connect(self.__handle_sequence_edit)
        self.pbt_seq_copy.clicked.connect(self.__handle_sequence_copy)
        self.pbt_seq_remove.clicked.connect(self.__handle_sequence_remove)
        self.pbt_seq_up.clicked.connect(self.__handle_sequence_move_up)
        self.pbt_seq_down.clicked.connect(self.__handle_sequence_move_down)
        self.cbt_rest_active.clicked.connect(self.__handle_rest_checkbox)
        self.cbt_dialog_active.clicked.connect(self.__handle_dialog_checkbox)
        self.lsv_test_dat.setModel(self.model_test_data)
        self.tbv_test_seq.setModel(self.model_test_sequence)
        self.tbv_test_seq.setColumnWidth(0, 80)
        self.tbv_test_seq.setColumnWidth(1, 45)

    def __update_experiment_data(self):
        self.__experiment.set_instructions(text=self.ted_instructions.toPlainText())
        self.__experiment.set_descripton(text=self.ted_description.toPlainText())
        self.__experiment.set_comments(text=self.led_comments.text())
        self.__experiment.set_space_start(status=self.cbt_use_space_key.isChecked())
        self.__experiment.set_random(status=self.cbt_random_active.isChecked())
        self.__experiment.set_rest_conf(
            status=self.cbt_rest_active.isChecked(),
            period=self.isb_rest_period.value(),
            time=self.dsb_rest_time.value(),
        )
        self.__experiment.set_dialog(
            status=self.cbt_dialog_active.isChecked(),
            askage=self.cbt_age.isChecked(),
            askgender=self.cbt_gender.isChecked(),
            askglasses=self.cbt_glasses.isChecked(),
            askeyecolor=self.cbt_eyes.isChecked(),
        )

    def __handle_save_action(self):
        try:
            is_saved = False
            is_code_used = False
            is_info_used = False
            new_code = unicode(self.led_code.text())
            new_name = unicode(self.led_name.text())
            new_version = unicode(self.led_version.text())
            if self.__is_edit:
                old_code = self.__experiment.get_code()
                old_name = self.__experiment.get_name()
                old_version = self.__experiment.get_version()
                experiment_list = Experiment.get_list(db=self.__parent.database)
                if new_code == old_code:
                    if ((new_name == old_name and new_version == old_version) or
                        self.__experiment.set_info(name=new_name, version=new_version)
                    ):
                        self.__update_experiment_data()
                        is_saved = self.__experiment.save()
                    else:
                        is_info_used = True
                elif (new_code != old_code) and not is_in_list(item=new_code, item_list=experiment_list):
                    if ((new_name == old_name and new_version == old_version) or not
                        is_in_list(item=[new_name, new_version], item_list=experiment_list)
                    ):
                        self.__experiment.remove()
                        self.__experiment.set_code(code=new_code)
                        self.__experiment.set_info(name=new_name, version=new_version)
                        self.__update_experiment_data()
                        is_saved = self.__experiment.save()
                    else:
                        is_info_used = True
                else:
                    is_code_used = True
            else:
                if self.__experiment.set_code(code=new_code):
                    if self.__experiment.set_info(name=new_name, version=new_version):
                        self.__update_experiment_data()
                        is_saved = self.__experiment.save()
                    else:
                        is_info_used = True
                else:
                    is_code_used = True
            if is_code_used:
                diag_tit = u"Error"
                diag_msg = u"Experiment code already used."
                QtGui.QMessageBox.warning(self, diag_tit, diag_msg)
            elif is_info_used:
                diag_tit = u"Error"
                diag_msg = u"Experiment name/version already used."
                QtGui.QMessageBox.warning(self, diag_tit, diag_msg)
            elif is_saved:
                self.__parent.update_experiment_model()
                new_index = self.__parent.model_experiment_tree.get_index_by_code(code=new_code)
                self.__parent.trv_experiment.setCurrentIndex(new_index)
                self.close()
        except Exception as error:
            diag_tit = u"Error"
            diag_msg = u"Experiment "+error.message
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_test_new(self):
        dialog = TestApp(parent=self.__experiment)
        new_index = dialog.exec_()
        if new_index != -1:
            self.update_data_model()
            self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(new_index, 0))

    def __handle_test_edit(self):
        index = self.lsv_test_dat.currentIndex().row()
        if index != -1:
            dialog = TestApp(parent=self.__experiment, test_id=index)
            new_index = dialog.exec_()
            if new_index != -1:
                seq_index = self.tbv_test_seq.currentIndex()
                self.update_data_model()
                self.update_sequence_model()
                self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(new_index, 0))
                self.tbv_test_seq.setCurrentIndex(seq_index)

    def __handle_test_copy(self):
        index = self.lsv_test_dat.currentIndex().row()
        if index != -1:
            dialog = CopyItemApp(item_parent=self.__experiment, item_type=u"Test",  item_id=index)
            new_index = dialog.exec_()
            if new_index != -1:
                self.update_data_model()
                self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(new_index, 0))

    def __handle_test_remove(self):
        index = self.lsv_test_dat.currentIndex().row()
        if index != -1:
            name = self.model_test_data.get_item(index=index)
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\ntest (%s)?" % name
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                self.__experiment.item_remove(item_id=index)
                self.update_data_model()
                self.update_sequence_model()
                new_index = index-1 if index > 0 else 0
                self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(new_index, 0))
                self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(0, 0))

    def __handle_test_move_up(self):
        index = self.lsv_test_dat.currentIndex().row()
        if self.__experiment.item_swap(item1_id=index, item2_id=index-1):
            self.update_data_model()
            self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(index-1, 0))

    def __handle_test_move_down(self):
        index = self.lsv_test_dat.currentIndex().row()
        if self.__experiment.item_swap(item1_id=index, item2_id=index+1):
            self.update_data_model()
            self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(index+1, 0))

    def __handle_sequence_add(self):
        dialog = TestSequenceApp(parent=self.__experiment)
        new_index = dialog.exec_()
        if new_index != -1:
            self.update_sequence_model()
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(new_index, 0))

    def __handle_sequence_edit(self):
        index = self.tbv_test_seq.currentIndex().row()
        if index != -1:
            dialog = TestSequenceApp(parent=self.__experiment, index=index)
            new_index = dialog.exec_()
            if new_index != -1:
                self.update_sequence_model()
                self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(new_index, 0))

    def __handle_sequence_copy(self):
        index = self.tbv_test_seq.currentIndex().row()
        if index != -1:
            item_count = self.__experiment.get_sequence_length()
            item = self.__experiment.get_sequence()[index]
            self.__experiment.sequence_add(item_id=self.__experiment.get_items().index(item[0]), quantity=item[1])
            self.update_sequence_model()
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(item_count, 0))

    def __handle_sequence_remove(self):
        index = self.tbv_test_seq.currentIndex().row()
        if index != -1:
            self.__experiment.sequence_remove(index=index)
            self.update_sequence_model()
            new_index = index-1 if index > 0 else 0
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(new_index, 0))

    def __handle_sequence_move_up(self):
        index = self.tbv_test_seq.currentIndex().row()
        if self.__experiment.sequence_swap(index1=index, index2=index-1):
            self.update_sequence_model()
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(index-1, 0))

    def __handle_sequence_move_down(self):
        index = self.tbv_test_seq.currentIndex().row()
        if self.__experiment.sequence_swap(index1=index, index2=index+1):
            self.update_sequence_model()
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(index+1, 0))

    def __handle_rest_checkbox(self):
        if not self.cbt_rest_active.isChecked():
            self.isb_rest_period.setEnabled(False)
            self.dsb_rest_time.setEnabled(False)
        else:
            self.isb_rest_period.setEnabled(True)
            self.dsb_rest_time.setEnabled(True)

    def __handle_dialog_checkbox(self):
        if not self.cbt_dialog_active.isChecked():
            self.cbt_age.setEnabled(False)
            self.cbt_eyes.setEnabled(False)
            self.cbt_gender.setEnabled(False)
            self.cbt_glasses.setEnabled(False)
        else:
            self.cbt_age.setEnabled(True)
            self.cbt_eyes.setEnabled(True)
            self.cbt_gender.setEnabled(True)
            self.cbt_glasses.setEnabled(True)

    def __check_code(self, code=u""):
        if code != u"":
            self.__is_edit = True
            self.__experiment.load(code=code)
            self.led_code.setText(self.__experiment.get_code())
        self.led_name.setText(self.__experiment.get_name())
        self.led_version.setText(self.__experiment.get_version())
        self.led_comments.setText(self.__experiment.get_comments())
        self.ted_description.setPlainText(self.__experiment.get_description())
        self.ted_instructions.setPlainText(self.__experiment.get_instructions())
        self.isb_rest_period.setValue(self.__experiment.get_rest_period())
        self.dsb_rest_time.setValue(self.__experiment.get_rest_time())
        self.cbt_use_space_key.setChecked(self.__experiment.is_space_start())
        self.cbt_random_active.setChecked(self.__experiment.is_random())
        self.cbt_rest_active.setChecked(self.__experiment.is_rest())
        self.cbt_dialog_active.setChecked(self.__experiment.is_dialog_active())
        self.cbt_age.setChecked(self.__experiment.is_ask_age())
        self.cbt_eyes.setChecked(self.__experiment.is_ask_eye_color())
        self.cbt_gender.setChecked(self.__experiment.is_ask_gender())
        self.cbt_glasses.setChecked(self.__experiment.is_ask_glasses())
        self.__handle_rest_checkbox()
        self.__handle_dialog_checkbox()
        self.update_data_model()
        if self.model_test_data.rowCount() > 0:
            self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(0, 0))
        self.update_sequence_model()
        if self.model_test_sequence.rowCount() > 0:
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(0, 0))

    def update_data_model(self):
        test_lst = self.__experiment.get_items_str()
        self.model_test_data.update_items(items=test_lst if test_lst else [])

    def update_sequence_model(self):
        sequence_lst = self.__experiment.get_sequence()
        if sequence_lst:
            sequence_lst = [[item[0].get_name(), item[1]] for item in sequence_lst]
            self.model_test_sequence.update_items(items=sequence_lst)
        else:
            self.model_test_sequence.update_items(items=[])


# ===============================================
# Class: TestSequenceApp
# ===============================================
class TestSequenceApp(base_tes_seq, form_tes_seq):
    def __init__(self, parent=Experiment, index=-1):
        super(TestSequenceApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__experiment = parent
        self.__is_edit = False
        self.__index = index
        # -------------------
        self.model_test = ListModel(items=[])
        self.update_test_model()
        # -------------------
        self.__setup_dialog()
        self.__check_index()

    def __setup_dialog(self):
        self.pbt_ok.clicked.connect(self.__handle_ok_action)
        self.pbt_cancel.clicked.connect(lambda: self.done(-1))
        self.cmb_test.setModel(self.model_test)
        self.cmb_test.setCurrentIndex(0)

    def __handle_ok_action(self):
        test_id = self.cmb_test.currentIndex()
        test_quantity = self.isb_quantity.value()
        if self.__is_edit:
            self.__experiment.sequence_edit(index=self.__index, item_id=test_id, quantity=test_quantity)
        else:
            self.__experiment.sequence_add(item_id=test_id, quantity=test_quantity)
            self.__index = self.__experiment.get_sequence_length()-1
        self.done(self.__index)

    def __check_index(self):
        if self.__index != -1:
            self.__is_edit = True
            item = self.__experiment.get_sequence_item(index=self.__index)
            test_index = self.cmb_test.findText(item[0].get_name(), QtCore.Qt.MatchFixedString)
            self.isb_quantity.setValue(item[1])
            self.cmb_test.setCurrentIndex(test_index)

    def update_test_model(self):
        test_lst = self.__experiment.get_items_str()
        self.model_test.update_items(items=test_lst if test_lst else [])


# ===============================================
# Class: TestApp
# ===============================================
class TestApp(base_tes, form_tes):
    def __init__(self, parent=Experiment, test_id=-1):
        super(TestApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__experiment = parent
        self.__test = Test()
        self.__old_name = u""
        # -------------------
        self.model_frame = ListModel(items=[], header=u"Frame")
        # -------------------
        self.__setup_test()
        self.__check_id(test_id=test_id)

    # =================================
    def __setup_test(self):
        self.pbt_save.clicked.connect(self.__handle_save_action)
        self.pbt_cancel.clicked.connect(lambda: self.done(-1))
        self.pbt_new.clicked.connect(self.__handle_frame_new)
        self.pbt_edit.clicked.connect(self.__handle_frame_edit)
        self.pbt_copy.clicked.connect(self.__handle_frame_copy)
        self.pbt_remove.clicked.connect(self.__handle_frame_remove)
        self.pbt_up.clicked.connect(self.__handle_frame_move_up)
        self.pbt_down.clicked.connect(self.__handle_frame_move_down)
        self.lsv_frame.setModel(self.model_frame)

    def __handle_save_action(self):
        try:
            self.__test.set_name(name=self.led_name.text())
            self.__test.set_description(text=self.ted_description.toPlainText())
            index = check_item_name(item_parent=self.__experiment, item=self.__test, old_name=self.__old_name)
            if index != -1:
                self.done(index)
        except Exception as error:
            diag_tit = u"Error"
            diag_msg = u"Test "+error.message
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_frame_new(self):
        dialog = FrameApp(item_parent=self.__test)
        new_index = dialog.exec_()
        if new_index != -1:
            self.update_frame_model()
            self.lsv_frame.setCurrentIndex(self.model_frame.index(new_index, 0))

    def __handle_frame_edit(self):
        index = self.lsv_frame.currentIndex().row()
        if index != -1:
            dialog = FrameApp(item_parent=self.__test, frame_id=index)
            new_index = dialog.exec_()
            if new_index != -1:
                self.update_frame_model()
                self.lsv_frame.setCurrentIndex(self.model_frame.index(new_index, 0))

    def __handle_frame_copy(self):
        index = self.lsv_frame.currentIndex().row()
        if index != -1:
            dialog = CopyItemApp(item_parent=self.__test, item_type=u"Frame", item_id=index)
            new_index = dialog.exec_()
            if new_index != -1:
                self.update_frame_model()
                self.lsv_frame.setCurrentIndex(self.model_frame.index(new_index, 0))

    def __handle_frame_remove(self):
        index = self.lsv_frame.currentIndex().row()
        if index != -1:
            name = self.model_frame.get_item(index=index)
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\nframe (%s)?" % name
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                self.__test.item_remove(item_id=index)
                self.update_frame_model()
                new_index = index-1 if index > 0 else 0
                self.lsv_frame.setCurrentIndex(self.model_frame.index(new_index, 0))

    def __handle_frame_move_up(self):
        index = self.lsv_frame.currentIndex().row()
        if self.__test.item_swap(item1_id=index, item2_id=index-1):
            self.update_frame_model()
            self.lsv_frame.setCurrentIndex(self.model_frame.index(index-1, 0))

    def __handle_frame_move_down(self):
        index = self.lsv_frame.currentIndex().row()
        if self.__test.item_swap(item1_id=index, item2_id=index+1):
            self.update_frame_model()
            self.lsv_frame.setCurrentIndex(self.model_frame.index(index+1, 0))

    def __check_id(self, test_id=-1):
        if test_id != -1:
            self.__test = self.__experiment.get_item(item_id=test_id).copy()
            self.__old_name = self.__test.get_name()
        self.led_name.setText(self.__test.get_name())
        self.ted_description.setPlainText(self.__test.get_description())
        self.update_frame_model()
        if self.model_frame.rowCount() > 0:
            self.lsv_frame.setCurrentIndex(self.model_frame.index(0, 0))

    def update_frame_model(self):
        frame_lst = self.__test.get_items()
        if frame_lst:
            frame_lst = [item.get_name() for item in frame_lst]
            self.model_frame.update_items(items=frame_lst)
        else:
            self.model_frame.update_items(items=[])


# ===============================================
# Class: FrameApp
# ===============================================
class FrameApp(base_fra, form_fra):
    def __init__(self, item_parent=Test, frame_id=-1):
        super(FrameApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__test = item_parent
        self.__frame = Frame()
        self.__old_name = u""
        # -------------------
        self.__model_color = ColorListModel()
        self.model_component = TableModel(items=[], header=[u"Component", u"Shape"])
        # -------------------
        self.__setup_frame()
        self.__check_id(frame_id=frame_id)

    # =================================
    def __setup_frame(self):
        self.pbt_save.clicked.connect(self.__handle_save_action)
        self.pbt_cancel.clicked.connect(lambda: self.done(-1))
        self.pbt_new.clicked.connect(self.__handle_component_new)
        self.pbt_edit.clicked.connect(self.__handle_component_edit)
        self.pbt_copy.clicked.connect(self.__handle_component_copy)
        self.pbt_remove.clicked.connect(self.__handle_component_remove)
        self.pbt_up.clicked.connect(self.__handle_component_move_up)
        self.pbt_down.clicked.connect(self.__handle_component_move_down)
        self.rbt_task.clicked.connect(self.__handle_task_select)
        self.rbt_time.clicked.connect(self.__handle_task_select)
        self.cmb_background.setModel(self.__model_color)
        self.tbv_component.setModel(self.model_component)
        self.tbv_component.setColumnWidth(0, 160)
        self.tbv_component.setColumnWidth(1, 50)

    def __handle_save_action(self):
        try:
            self.__frame.set_name(name=self.led_name.text())
            if self.rbt_task.isChecked():
                self.__frame.set_as_task(state=True)
                self.__frame.set_keys_allowed(keys=self.led_keys_allowed.text())
                self.__frame.set_keys_correct(keys=self.led_keys_correct.text())
            else:
                self.__frame.set_as_task(state=False)
                self.__frame.set_time(value=self.dsb_time.value())
            index = check_item_name(item_parent=self.__test, item=self.__frame, old_name=self.__old_name)
            if index != -1:
                self.done(index)
        except Exception as error:
            diag_tit = u"Error"
            diag_msg = u"Frame "+error.message
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_component_new(self):
        dialog = ComponentApp(item_parent=self.__frame)
        new_index = dialog.exec_()
        if new_index != -1:
            self.update_component_model()
            self.tbv_component.setCurrentIndex(self.model_component.index(new_index, 0))

    def __handle_component_edit(self):
        index = self.tbv_component.currentIndex().row()
        if index != -1:
            dialog = ComponentApp(item_parent=self.__frame, component_id=index)
            new_index = dialog.exec_()
            if new_index != -1:
                self.update_component_model()
                self.tbv_component.setCurrentIndex(self.model_component.index(new_index, 0))

    def __handle_component_copy(self):
        index = self.tbv_component.currentIndex().row()
        if index != -1:
            dialog = CopyItemApp(item_parent=self.__frame, item_type=u"Component", item_id=index)
            new_index = dialog.exec_()
            if new_index != -1:
                self.update_component_model()
                self.tbv_component.setCurrentIndex(self.model_component.index(new_index, 0))

    def __handle_component_remove(self):
        index = self.tbv_component.currentIndex().row()
        if index != -1:
            name = self.model_component.get_item(index=index)[0]
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\ncomponent (%s)?" % name
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                self.__frame.item_remove(item_id=index)
                self.update_component_model()
                new_index = index-1 if index > 0 else 0
                self.tbv_component.setCurrentIndex(self.model_component.index(new_index, 0))

    def __handle_component_move_up(self):
        index = self.tbv_component.currentIndex().row()
        if self.__frame.item_swap(item1_id=index, item2_id=index-1):
            self.update_component_model()
            self.tbv_component.setCurrentIndex(self.model_component.index(index-1, 0))

    def __handle_component_move_down(self):
        index = self.tbv_component.currentIndex().row()
        if self.__frame.item_swap(item1_id=index, item2_id=index+1):
            self.update_component_model()
            self.tbv_component.setCurrentIndex(self.model_component.index(index+1, 0))

    def __handle_task_select(self):
        if self.rbt_task.isChecked():
            self.dsb_time.setValue(0.0)
            self.dsb_time.setEnabled(False)
            self.led_keys_allowed.setEnabled(True)
            self.led_keys_correct.setEnabled(True)
        else:
            self.led_keys_allowed.setText(u"")
            self.led_keys_correct.setText(u"")
            self.dsb_time.setEnabled(True)
            self.led_keys_allowed.setEnabled(False)
            self.led_keys_correct.setEnabled(False)

    def __check_id(self, frame_id=-1):
        if frame_id != -1:
            self.__frame = self.__test.get_item(item_id=frame_id).copy()
            self.__old_name = self.__frame.get_name()
        self.led_name.setText(self.__frame.get_name())
        self.dsb_time.setValue(self.__frame.get_time())
        self.led_keys_allowed.setText(self.__frame.get_keys_allowed())
        self.led_keys_correct.setText(self.__frame.get_keys_correct())
        color_index = self.cmb_background.findText(self.__frame.get_color(), QtCore.Qt.MatchFixedString)
        self.cmb_background.setCurrentIndex(color_index)
        if self.__frame.is_task():
            self.rbt_task.setChecked(True)
        else:
            self.rbt_time.setChecked(True)
        self.__handle_task_select()
        self.update_component_model()
        if self.model_component.rowCount() > 0:
            self.tbv_component.setCurrentIndex(self.model_component.index(0, 0))

    def update_component_model(self):
        component_lst = self.__frame.get_items()
        if component_lst:
            component_lst = [[item.get_name(), item.get_shape()] for item in component_lst]
            self.model_component.update_items(items=component_lst)
        else:
            self.model_component.update_items(items=[])


# ===============================================
# Class: ComponentApp
# ===============================================
class ComponentApp(base_com, form_com):
    def __init__(self, item_parent=Frame, component_id=-1):
        super(ComponentApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__frame = item_parent
        self.__component = Component()
        self.__old_name = u""
        # -------------------
        self.__model_units = ListModel(items=get_available_units(), header=u"Measure unit")
        self.__model_shape = ListModel(items=get_available_shapes(), header=u"Component shape")
        self.__model_shape_color = ColorListModel()
        # -------------------
        self.__setup_component()
        self.__check_id(component_id=component_id)

    # =================================
    def __setup_component(self):
        self.pbt_save.clicked.connect(self.__handle_save_action)
        self.pbt_cancel.clicked.connect(lambda: self.done(-1))
        self.pbt_image_open.clicked.connect(self.__handle_image_open)
        self.pbt_image_remove.clicked.connect(self.__handle_image_remove)
        self.lbl_image_status.setOpenExternalLinks(True)
        self.rbt_shape.clicked.connect(self.__handle_type_select)
        self.rbt_image.clicked.connect(self.__handle_type_select)
        self.cmb_units.setModel(self.__model_units)
        self.cmb_shape.setModel(self.__model_shape)
        self.cmb_shape_color.setModel(self.__model_shape_color)

    def __handle_save_action(self):
        try:
            self.__component.set_name(name=self.led_name.text())
            self.__component.set_units(units=self.cmb_units.currentText())
            self.__component.set_size(size=self.dsb_size.value())
            self.__component.set_position(posx=self.dsb_posx.value(), posy=self.dsb_posy.value())
            self.__component.set_rotation(rot=self.dsb_rotation.value())
            if self.rbt_shape.isChecked():
                self.__component.set_shape(shape=self.cmb_shape.currentText())
                self.__component.set_color(color=self.cmb_shape_color.currentText())
            else:
                self.__component.set_image(image=self.lbl_image_status.get_image())
            index = check_item_name(item_parent=self.__frame, item=self.__component, old_name=self.__old_name)
            if index != -1:
                self.done(index)
        except Exception as error:
            diag_tit = u"Error"
            diag_msg = u"Component "+error.message
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_image_open(self):
        base_path = get_main_path()
        image_path = QtGui.QFileDialog.getOpenFileName(self, u"Open File...", base_path, u"Images (*.png *.jpeg *.jpg)")
        self.lbl_image_status.set_image(image=unicode(image_path))

    def __handle_image_remove(self):
        if self.lbl_image_status.get_image() is not None:
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this image?\nThis operation can't be undone."
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                self.lbl_image_status.remove_image()

    def __handle_type_select(self):
        if self.rbt_shape.isChecked():
            self.cmb_shape.setEnabled(True)
            self.cmb_shape_color.setEnabled(True)
            self.pbt_image_open.setEnabled(False)
            self.pbt_image_remove.setEnabled(False)
        else:
            self.cmb_shape.setEnabled(False)
            self.cmb_shape_color.setEnabled(False)
            self.pbt_image_open.setEnabled(True)
            self.pbt_image_remove.setEnabled(True)

    def __check_id(self, component_id=-1):
        if component_id != -1:
            self.__component = self.__frame.get_item(item_id=component_id).copy()
            self.__old_name = self.__component.get_name()
        self.led_name.setText(self.__component.get_name())
        self.dsb_size.setValue(self.__component.get_size())
        self.dsb_posx.setValue(self.__component.get_position()[0])
        self.dsb_posy.setValue(self.__component.get_position()[1])
        self.dsb_rotation.setValue(self.__component.get_rotation())
        units_index = self.cmb_units.findText(self.__component.get_units(), QtCore.Qt.MatchFixedString)
        shape_index = self.cmb_shape.findText(self.__component.get_shape(), QtCore.Qt.MatchFixedString)
        shape_color_index = self.cmb_shape_color.findText(self.__component.get_color(), QtCore.Qt.MatchFixedString)
        self.cmb_units.setCurrentIndex(units_index)
        self.cmb_shape.setCurrentIndex(shape_index)
        self.cmb_shape_color.setCurrentIndex(shape_color_index)
        if self.__component.get_shape() == u"image":
            self.rbt_image.setChecked(True)
            self.lbl_image_status.set_image(image=self.__component.get_image())
        else:
            self.rbt_shape.setChecked(True)
        self.__handle_type_select()


# =============================================================================
# Configuration related Class: ConfigurationApp
# =============================================================================
class ConfigurationApp(base_con, form_con):
    def __init__(self, parent=SaccadeApp, profile_name=u""):
        super(ConfigurationApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__is_edit = False
        # -------------------
        self.__parent = parent
        self.__profile = Configuration(db=parent.database)
        self.__model_tracker = ListModel(items=get_available_trackers())
        self.__model_monitor = ListModel(items=get_available_monitors())
        self.__model_screen = ListModel(items=get_available_screens())
        # -------------------
        self.__setup_dialog()
        self.__check_name(name=profile_name)

    # =================================
    def __setup_dialog(self):
        self.pbt_save.clicked.connect(self.__handle_save_action)
        self.pbt_cancel.clicked.connect(self.close)
        self.pbt_path_browse.clicked.connect(self.__handle_path_browse)
        self.cmb_tracker.setModel(self.__model_tracker)
        self.cmb_monitor.setModel(self.__model_monitor)
        self.cmb_screen.setModel(self.__model_screen)

    def __update_profile_data(self):
        self.__profile.set_events_path(path=self.led_path.text())
        self.__profile.set_screen(screen=self.cmb_screen.currentIndex())
        self.__profile.set_monitor(monitor=self.cmb_monitor.currentText())
        self.__profile.set_tracker(tracker=self.cmb_tracker.currentText())

    def __handle_save_action(self):
        try:
            is_saved = False
            is_name_used = False
            new_name = unicode(self.led_name.text())
            if self.__is_edit:
                old_name = self.__profile.get_name()
                if new_name == old_name:
                    self.__update_profile_data()
                    is_saved = self.__profile.save()
                elif new_name not in Configuration.get_list(db=self.__parent.database):
                    self.__profile.remove()
                    self.__profile.set_name(name=new_name)
                    self.__update_profile_data()
                    is_saved = self.__profile.save()
                else:
                    is_name_used = True
            else:
                if self.__profile.set_name(name=new_name):
                    self.__update_profile_data()
                    is_saved = self.__profile.save()
                else:
                    is_name_used = True
            if is_name_used:
                diag_tit = u"Error"
                diag_msg = u"Profile name already used."
                QtGui.QMessageBox.warning(self, diag_tit, diag_msg)
            elif is_saved:
                self.__parent.update_configuration_model()
                new_index = self.__parent.model_configuration.get_index(new_name)
                self.__parent.lsv_configuration.setCurrentIndex(self.__parent.model_configuration.index(new_index, 0))
                self.close()
        except Exception as error:
            diag_tit = u"Error"
            diag_msg = u"Profile "+error.message
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_path_browse(self):
        title = u"Select events save directory..."
        folder = QtGui.QFileDialog.getExistingDirectory(self, title, self.led_path.text(),
                                                        QtGui.QFileDialog.ShowDirsOnly)
        if folder:
            self.led_path.setText(format_path(unicode(folder)+u"/"))

    def __check_name(self, name=u""):
        if name != u"":
            self.__is_edit = True
            self.__profile.load(name=name)
        self.led_name.setText(self.__profile.get_name())
        self.led_path.setText(self.__profile.get_events_path())
        screen_index = self.cmb_screen.findText(self.__profile.get_screen(), QtCore.Qt.MatchFixedString)
        monitor_index = self.cmb_monitor.findText(self.__profile.get_monitor(), QtCore.Qt.MatchFixedString)
        tracker_index = self.cmb_tracker.findText(self.__profile.get_tracker_name(), QtCore.Qt.MatchFixedString)
        self.cmb_screen.setCurrentIndex(screen_index)
        self.cmb_monitor.setCurrentIndex(monitor_index)
        self.cmb_tracker.setCurrentIndex(tracker_index)


# =============================================================================
# Utility Classes:
# =============================================================================
# ===============================================
# Class: CopyExperimentApp
# ===============================================
class CopyExperimentApp(base_copy_exp, form_copy_exp):
    def __init__(self, parent=SaccadeApp, experiment_code=u""):
        super(CopyExperimentApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__parent = parent
        self.__experiment = Experiment(db=parent.database, code=experiment_code)
        # -------------------
        self.__setup_dialog()

    # =================================
    def __setup_dialog(self):
        self.pbt_ok.clicked.connect(self.__handle_ok_action)
        self.pbt_cancel.clicked.connect(self.__handle_cancel_action)
        self.lbl_code.setText(u"Base experiment code: "+self.__experiment.get_code()+u".\n\nNew code:")
        self.lbl_version.setText(u"Base experiment version: "+self.__experiment.get_version()+u".\n\nNew version:")
        self.led_code.setText(self.__experiment.get_code())
        self.led_version.setText(self.__experiment.get_version())

    def __handle_ok_action(self):
        new_code = unicode(self.led_code.text())
        new_version = unicode(self.led_version.text())
        try:
            new_experiment = self.__experiment.copy(code=new_code, version=new_version)
            if new_experiment is not None:
                new_experiment.save()
                self.__parent.update_experiment_model()
                new_index = self.__parent.model_experiment_tree.get_index_by_code(code=new_code)
                self.__parent.trv_experiment.setCurrentIndex(new_index)
                self.close()
            else:
                diag_tit = u"Error"
                diag_msg = u"Code or version value already\nused for this type of experiment."
                QtGui.QMessageBox.warning(self, diag_tit, diag_msg)
        except Exception as error:
            diag_tit = u"Error"
            diag_msg = u"Experiment "+error.message
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_cancel_action(self):
        self.close()


# ===============================================
# Class: CopyConfigurationApp
# ===============================================
class CopyConfigurationApp(base_copy, form_copy):
    def __init__(self, parent=SaccadeApp, profile_name=u""):
        super(CopyConfigurationApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__parent = parent
        self.__profile = Configuration(db=parent.database, name=profile_name)
        # -------------------
        self.__setup_dialog()

    # =================================
    def __setup_dialog(self):
        self.pbt_ok.clicked.connect(self.__handle_ok_action)
        self.pbt_cancel.clicked.connect(self.__handle_cancel_action)
        self.lbl_copy.setText(u"Old profile name: "+self.__profile.get_name()+u".\n\nNew name:")
        self.led_copy.setText(self.__profile.get_name())

    def __handle_ok_action(self):
        new_name = unicode(self.led_copy.text())
        try:
            new_profile = self.__profile.copy(name=new_name)
            if new_profile is not None:
                new_profile.save()
                self.__parent.update_configuration_model()
                new_index = self.__parent.model_configuration.get_index(item=new_name)
                self.__parent.lsv_configuration.setCurrentIndex(self.__parent.model_configuration.index(new_index, 0))
                self.close()
            else:
                diag_tit = u"Error"
                diag_msg = u"Profile name already used."
                QtGui.QMessageBox.warning(self, diag_tit, diag_msg)
        except Exception as error:
            diag_tit = u"Error"
            diag_msg = u"Profile "+error.message
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_cancel_action(self):
        self.close()


# ===============================================
# Class: CopyItemApp
# ===============================================
class CopyItemApp(base_copy, form_copy):
    def __init__(self, item_parent, item_type=u"", item_id=-1):
        super(CopyItemApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__parent = item_parent
        self.__item_id = item_id
        self.__item_type = item_type
        # -------------------
        self.__setup_dialog()

    def __setup_dialog(self):
        item_name = self.__parent.get_item(item_id=self.__item_id).get_name()
        self.pbt_ok.clicked.connect(self.__handle_ok_action)
        self.pbt_cancel.clicked.connect(self.__handle_cancel_action)
        self.lbl_copy.setText(u"Old name: "+item_name+u".\n\nNew name:")
        self.led_copy.setText(item_name)

    def __handle_ok_action(self):
        new_name = unicode(self.led_copy.text())
        try:
            new_index = self.__parent.get_items_length()
            if self.__parent.item_copy(item_id=self.__item_id, new_name=new_name):
                self.done(new_index)
            else:
                diag_tit = u"Error"
                diag_msg = u"Name already used."
                QtGui.QMessageBox.warning(self, diag_tit, diag_msg)
        except Exception as error:
            diag_tit = u"Error"
            diag_msg = self.__item_type+u" "+error.message
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_cancel_action(self):
        self.done(-1)


# ===============================================
# Class: About
# ===============================================
class AboutApp(base_about, form_about):
    def __init__(self):
        super(AboutApp, self).__init__(parent=None)
        self.setupUi(self)
