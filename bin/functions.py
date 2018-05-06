# =============================================================================
# Functions
# =============================================================================
def configure_experiment():
    # =======================
    import os
    from saccadeapp import SaccadeDB
    from saccadeapp import Experiment, Test, Frame, Component

    # =======================
    base_dir = u'C:\\Experiments'
    if not os.path.isdir(base_dir):
        os.mkdir(base_dir)

    data = SaccadeDB(base_dir + u'\\test_database.sqlite3')

    # =======================
    cross = Component()
    cross.set_name(u'CP')
    cross.set_size(1.0)
    cross.set_shape(u'cross')
    cross.set_color(u'white')
    cross.set_position(0.0, 0.0)

    target = Component()
    target.set_name(u'TP')
    target.set_size(1.0)
    target.set_shape(u'square')
    target.set_color(u'red')
    target.set_position(16.0, 0.0)

    frame1 = Frame()
    frame1.set_name(u'Central Stimulus')
    frame1.set_time(1.8)
    frame1.set_as_task(False)
    frame1.set_color(u'black')
    frame1.component_add(cross)

    frame2 = frame1.copy()
    frame2.set_name(u'Target')
    frame2.set_time(1.5)
    frame2.component_add(target)

    frame3 = frame1.copy()

    test1 = Test()
    test1.set_name(u'Overlap Task')
    test1.set_quantity(1)
    test1.frame_add(frame1)
    test1.frame_add(frame2)
    test1.frame_add(frame3)

    # =======================
    image = Component()
    image.set_image(u'couple.png')

    frame4 = Frame()
    frame4.set_name(u'Image Presentation')
    frame4.set_as_task(True)
    frame4.set_keys_allowed(u'space')
    frame4.set_keys_selected(u'space')
    frame4.component_add(image)

    test2 = Test()
    test2.set_name(u'Search task')
    test2.set_quantity(1)
    test2.frame_add(frame4)

    # =======================
    experiment = Experiment()
    experiment.set_database(data)

    experiment.set_code(u'expcode_01')
    experiment.set_info(u'Experiment test', u'v1.0')
    experiment.set_space_start(True)
    experiment.set_dialog(status=False)
    experiment.test_add(test1)
    experiment.test_add(test2)
    experiment.save()


def execute_experiment():
    # =======================
    import os
    from saccadeapp import SaccadeDB
    from saccadeapp import Master
    from saccadeapp import ExperimentHandler

    # =======================
    base_dir = u'C:\\Experiments'
    data_dir = base_dir + u'\\Events'

    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

    data = SaccadeDB(base_dir + u'\\test_database.sqlite3')

    # =======================
    conf = Master()
    conf.set_database(data)

    conf.set_name(u'my_profile')
    conf.set_monitor(u'test_monitor')
    conf.set_screen(1)
    conf.set_tracker(u'eyetribe')
    conf.set_experiment_path(data_dir)
    conf.save()

    # =======================
    execution = ExperimentHandler()

    if execution.load_configuration(db=data, master=u'my_profile', experiment=u'expcode_01'):
        execution.save_parameters(save_frame=True)
        execution.execute_experiment()


def get_eyetracker_gaze_data(h5_file, is_binocular=True):
    # =======================
    import h5py as h5
    import numpy as np
    # =======================
    try:
        data = h5.File(h5_file)
        # ===============
        if is_binocular:
            eye_data = data.get(u'data_collection/events/eyetracker/BinocularEyeSampleEvent')
        else:
            eye_data = data.get(u'data_collection/events/eyetracker/BinocularEyeSampleEvent')
        # ===============
        eye_data = [list(item) for item in eye_data[:]]
        if eye_data:
            eye_data = np.array(eye_data, dtype=object)
            if is_binocular:
                gaze_x = np.average(eye_data[:, [11, 30]], axis=1)
                gaze_y = np.average(eye_data[:, [12, 31]], axis=1)
                eye_data = eye_data[:, [0, 1, 6]]
                eye_data = np.insert(eye_data, 3, gaze_x, axis=1)
                eye_data = np.insert(eye_data, 4, gaze_y, axis=1)
            else:
                eye_data = eye_data[:, [0, 1, 6, 12, 13]]
            # ===========
            return eye_data
        else:
            return None
    except:
        print u"Error: Can't open the file."
        return None


def check_image():
    # =======================
    from matplotlib import pyplot as pp

    # =======================
    base_dir = u'C:\\Experiments'
    data_dir = base_dir + u'\\Events'
    exps_dir = data_dir + u'\\Experiment test\\[v1.0][expcode_01]'

    # =======================
    h5_data = get_eyetracker_gaze_data(exps_dir + u'\\[expcode_01]events_data.hdf5', is_binocular=True)
    frame_gaze = h5_data[(h5_data[:, 2] >= 29.7) & (h5_data[:, 2] <= 56.5)]

    image = pp.imread(exps_dir + u'\\frames\\test1_frame0.png')
    im_x_size = image.shape[1]
    im_y_size = image.shape[0]

    # =======================
    x_gaze = frame_gaze[:, 3] + (im_x_size/2) - 1
    y_gaze = frame_gaze[:, 4] + (im_y_size/2) - 1

    # =======================
    fig, ax = pp.subplots()
    ax.imshow(image, extent=[0, im_x_size, 0, im_y_size])
    ax.plot(x_gaze, y_gaze, u'-', linewidth=1, color=u'red')
    ax.xlim(0, 1440)
    fig.show()