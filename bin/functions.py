# -*- coding: utf-8 -*-
# =============================================================================
from saccadeapp.api import format_path
import h5py as h5
import cv2

exp_ver = u"1.0"
exp_name = u"Sample Experiment"
exp_code = u"exs_0001"

base_path = format_path(u"D:/Github/Thesis/Thesis_Code/bin/events/")
data_path = format_path(base_path + u"[{0}]/[{1}][{2}]/".format(exp_name, exp_ver, exp_code))

image = cv2.imread(format_path(data_path + u"frames/Test[0]_Frame[0].png"), cv2.IMREAD_COLOR)
image_size_x = image.shape[1]
image_size_y = image.shape[0]

h5_data = h5.File(format_path(data_path + u"[{0}]events_data.hdf5".format(exp_code)))
et_data = h5_data.get(u"data_collection/events/eyetracker/BinocularEyeSampleEvent").value
et_time = et_data[u"logged_time"] - et_data[u"logged_time"].min()
et_gazex = ((et_data[u"left_gaze_x"]+et_data[u"right_gaze_x"])/2) + (image_size_x/2) - 1
et_gazey = -((et_data[u"left_gaze_y"]+et_data[u"right_gaze_y"])/2) + (image_size_y/2) - 1


writer = cv2.VideoWriter(u"test.mp4", fourcc=cv2.VideoWriter_fourcc(*'MP4V'), fps=60, frameSize=(image_size_x, image_size_y))
for frame in range(et_time.size):
    new_image = image.copy()
    cv2.circle(new_image, (et_gazex[frame], et_gazey[frame]), 10, (0, 0, 255), -1)
    writer.write(new_image)
writer.release()
