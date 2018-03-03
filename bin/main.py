# -*- coding: utf-8 -*-


# =============================================================================
# Test utils
# =============================================================================
def get_eyetracker_gaze_data(h5_file, is_binocular=True):
    import h5py as h5
    import numpy as np
    # ===================
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

def get_image_as_frame(image_file, screen_width, screen_height):
    import numpy as np
    from matplotlib import pyplot as pp
    # =======================
    try:
        image = pp.imread(image_file)
        image_x_size = image.shape[1]
        image_y_size = image.shape[0]
        # ===================

    except:
        print u"Error: Can't open the file."



# =============================================================================
# Main: Use example
# =============================================================================
if __name__ == '__main__':
    # # =================================
    # # =================================
    # # =================================
    # import os
    # from saccadeApp import SaccadeDB, Master
    # from saccadeApp import Experiment, Test, Frame, Component
    #
    # # Se crean los directorios para almacenar las configuraciones y resultados de los experimentos
    # base_dir = u'C:\\Experiments'
    # data_dir = base_dir + u'\\Experiment_Data'
    # if not os.path.isdir(base_dir):
    #     os.mkdir(base_dir)
    #     os.mkdir(data_dir)
    # elif not os.path.isdir(data_dir):
    #     os.mkdir(data_dir)
    #
    # # Se abre (o si no existe, crea) la base de datos local
    # data = SaccadeDB(base_dir + u'\\test_database.sqlite3')
    #
    # # Se abre la instancia de configuración de monitores para verificar que el perfil a ser escogido existe
    # Master.open_psychopy_monitor_center()
    #
    # # =================================
    # # =================================
    # # =================================
    # # Se crea una instancia de configuración
    # conf = Master()
    # conf.set_database(data)
    #
    # # Se asigna nombre, se selecciona la pantalla secundaria con el perfil 'test_profile' para un eyetracker
    # # 'eyetribe'. Los resultados de los experimentos se almacenarán en el directorio de datos
    # conf.set_name(u'test_profile')
    # conf.set_screen(1)
    # conf.set_monitor(u'test_monitor')
    # conf.set_tracker(u'eyetribe')
    # conf.set_experiment_path(data_dir)
    #
    # # Y finalmente se guarda la cconfiguración
    # conf.save()
    #
    # # =================================
    # # =================================
    # # =================================
    # # Construccion del primer test: Movimiento pro/anti-sacádico  con overlap
    # # Componentes
    # cross = Component()
    # cross.set_size(0.5)
    # cross.set_shape(u'cross')
    # cross.set_position(0.0, 0.0)
    #
    # target = Component()
    # target.set_size(0.5)
    # target.set_shape(u'square')
    # target.set_position(16.0, 0)
    #
    # # Cuadros
    # frame1 = Frame()
    # frame1.set_name(u'Central Stimulus')
    # frame1.set_time(1.8)
    # frame1.set_as_task(False)
    # frame1.set_color(u'black')
    # frame1.component_add(cross)
    #
    # frame2 = frame1.copy()
    # frame2.set_name(u'Target')
    # frame2.set_time(1.5)
    # frame2.component_add(target)
    #
    # frame3 = frame1.copy()
    # frame3.set_time(1.0)
    #
    # # Tarea
    # test1 = Test()
    # test1.set_name(u'Overlap task')
    # test1.set_quantity(1)
    # test1.frame_add(frame1)
    # test1.frame_add(frame2)
    # test1.frame_add(frame3)
    #
    # # Construccion del segundo test: Patrones de busqueda
    # # Componente
    # image = Component()
    # image.set_image(u'couple.png')
    #
    # # Cuadro
    # frame4 = Frame()
    # frame4.set_name(u'Image Presentation')
    # frame4.set_as_task(True)
    # frame4.set_keys_allowed(u'space')
    # frame4.set_keys_selected(u'space')
    # frame4.component_add(image)
    #
    # # Tarea
    # test2 = Test()
    # test2.set_name(u'Search task')
    # test2.set_quantity(1)
    # test2.frame_add(frame4)
    #
    # # Se construye el experimento
    # experiment = Experiment()
    # experiment.set_database(data)
    # experiment.set_code(u'expcode_01')
    # experiment.set_info(u'Capability Test', u'v1.0')
    # experiment.set_space_start(True)
    # experiment.set_dialog(status=False)
    # experiment.test_add(test1)
    # experiment.test_add(test2)
    #
    # # Y finalmente se guarda la configuración
    # experiment.save()
    #
    # # =================================
    # # =================================
    # # =================================
    from saccadeApp import ExperimentHandler
    #
    # # Con las configuraciones anteriores es posible ejecutar el experimento
    # execution = ExperimentHandler()
    #
    # if execution.load_experiment(db=data, mas=u'test_profile', exp=u'expcode_01'):
    #     execution.save_parameters()
    #     execution.execute_experiment()

    base_dir = u'C:\\Experiments\\Experiment_Data'
    h5_file = base_dir + u'\\Experiment test\\[v1.0][expcode_01]\\[expcode_01]events_data.hdf5'
    h5_data = get_eyetracker_gaze_data(h5_file, is_binocular=True)

    from matplotlib import pyplot as pp
    frame_gaze = h5_data[(h5_data[:, 1] == 2) & (h5_data[:, 2] >= 47.0) & (h5_data[:, 2] <= 93.0)]

    image = pp.imread(u'couple.png')
    image_size = image.shape
    x_size = image_size[1]
    y_size = image_size[0]

    x_gaze = frame_gaze[:, 3] + (x_size/2) - 1
    y_gaze = frame_gaze[:, 4] + (y_size/2) - 1

    fig, ax = pp.subplots()
    ax.imshow(image, extent=[0, image_size[1], 0, image_size[0]])
    ax.plot(x_gaze, y_gaze, u'-', linewidth=2, color=u'firebrick')
    fig.show()


