import os
import cv2
import numpy as np
import sys
import wx
import shutil

camera_device_id = 0
frame_size = (1280, 720)
min_size_proportional = (0.25, 0.25)
scale_factor = 1.3
min_neighbors = 4
flags = cv2.cv.CV_HAAR_SCALE_IMAGE


def image_to_wxbitmap(image):
    image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)
    h, w = image.shape[:2]
    # The following conversion fails on Raspberry Pi.
    bitmap = wx.BitmapFromBuffer(w, h, image)
    return bitmap


def resize_video_capture_with_image_size(capture, preferredSize):
    # Try to set the requested dimensions.
    w, h = preferredSize
    if capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w):
        if capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, h):
            # The requested dimensions were successfully set.
            # Return the requested dimensions.
            return preferredSize
    # The requested dimensions could not be set.
    # Return the actual dimensions.
    w = capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    h = capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    return w, h


def get_pictures_and_labels():
    pictures, labels = [], []
    training_images_path = resource_path('training_images/')
    for dirname, dirnames, filenames in os.walk(training_images_path):
        dirnames = sorted(dirnames)
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    pictures.append(np.asarray(im, dtype=np.uint8))
                    labels.append(int(subdirname))
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
    return pictures, labels


def resource_path(relativePath):
    basePath = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(basePath, relativePath)


def move_all_files(origin_path, destination_path):
    source = os.listdir(origin_path)
    for files in source:
        print files, destination_path
        shutil.move(origin_path + "/" + files, destination_path)