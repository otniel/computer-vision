import cv
import cv2
import numpy
import os
import threading
import wx
from solid_attendance_dao import SolidAttendanceDao

EYE_SX = 0.10
EYE_SY = 0.30
EYE_SW = 0.40
EYE_SH = 0.50

import utils


class Trainer(wx.Frame):

    def __init__(self):
        self.attendance_dao = SolidAttendanceDao()
        self.instructions = {1: 'Instructions: Look to left',
                             2: 'Instructions: Look to up',
                             3: 'Instructions: Look to right',
                             4: 'Instructions: Look to down',
                             5: 'Instructions: Look straight',
                             6: 'Instructions: Move your head \nto left',
                             7: 'Instructions: Move your head \nto right',
                             8: 'Instructions: Move your head \nup',
                             9: 'Instructions: Move your head \ndown',
                             10: 'Instructions: Smile',
                             11: 'Instructions: Get angry',
                             12: 'Instructions: Neutral face'}

        self._running = True
        self.train_step = 1

        self._capture = cv2.VideoCapture(utils.camera_device_id)
        size = utils.resize_video_capture_with_image_size(self._capture, utils.frame_size)
        self._imageWidth, self._imageHeight = size
        self._currDetectedObject = None

        self._recognizer = cv2.createFisherFaceRecognizer()

        cascade_path = utils.resource_path('cascades/haarcascade_frontalface_alt2.xml')
        self._detector = cv2.CascadeClassifier(cascade_path)
        self._right_eye_detector = cv2.CascadeClassifier(
            '/home/otniel/Documents/repos/computer-vision/SOLIDAttendance/cascades/haarcascade_mcs_righteye.xml')
        self._left_eye_detector = cv2.CascadeClassifier(
            '/home/otniel/Documents/repos/computer-vision/SOLIDAttendance/cascades/haarcascade_mcs_lefteye.xml')

        min_image_size = min(self._imageWidth, self._imageHeight)
        self.min_size = (int(min_image_size * utils.min_size_proportional[0]),
                         int(min_image_size * utils.min_size_proportional[1]))

        style = wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION | wx.SYSTEM_MENU | wx.CLIP_CHILDREN

        wx.Frame.__init__(self, None, style=style, size=size)
        self.SetBackgroundColour(wx.Colour(232, 232, 232))

        self.Bind(wx.EVT_CLOSE, self._onCloseWindow)

        quitCommandID = wx.NewId()
        self.Bind(wx.EVT_MENU, self._onQuitCommand, id=quitCommandID)
        acceleratorTable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, quitCommandID)])
        self.SetAcceleratorTable(acceleratorTable)

        self._staticBitmap = wx.StaticBitmap(self, size=size)
        self._showImage(None)

        self.instructions_label = wx.StaticText(self)
        self.instructions_label.SetLabel(self.instructions[self.train_step])

        # self.name, self.charge = self.get_user_info()
        self.name, self.charge = "Javi", "HR"
        self.name_label = wx.StaticText(self, label="Name: " + self.name)
        self.charge_label = wx.StaticText(self, label='Charge: ' + self.charge)

        user_info_sizer = wx.BoxSizer(wx.VERTICAL)
        user_info_sizer.Add(self.name_label, 0, wx.LEFT, 5)
        user_info_sizer.Add(self.charge_label, 0, wx.LEFT, 5)

        self.change_name_button = wx.Button(self, label='Update info')
        # self.change_name_button.Bind(wx.EVT_BUTTON, self._update_user_info)
        self._take_photo_button = wx.Button(self, label='Take photo')
        self._take_photo_button.Bind(wx.EVT_BUTTON, self._take_photo)

        border = 12

        controls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        controls_sizer.Add(self.instructions_label, 0, wx.ALIGN_CENTER_VERTICAL)
        controls_sizer.Add((0, 0), 1)  # Spacer
        controls_sizer.Add(user_info_sizer, 0, wx.ALIGN_CENTER_VERTICAL)
        controls_sizer.Add((0, 0), 1)  # Spacer
        controls_sizer.Add(self.change_name_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border)

        controls_sizer.Add((0, 0), 1)  # Spacer

        controls_sizer.Add(self._take_photo_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border)

        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self._staticBitmap)
        rootSizer.Add(controls_sizer, 0, wx.EXPAND | wx.ALL, border)
        self.SetSizerAndFit(rootSizer)

        self._captureThread = threading.Thread(target=self._runCaptureLoop)
        self._captureThread.start()

        self.temp_images_path = utils.resource_path('temp_images/')

        if not os.path.exists(self.temp_images_path):
            os.makedirs(self.temp_images_path)


    def _take_photo(self, event):
        print "TRAINSTEP ", self.train_step
        if self.train_step >= 12:
            last_id = self.attendance_dao.get_last_user_id()
            user_directory = utils.resource_path('training_images/' + str(last_id + 1) + "/")
            os.makedirs(user_directory)
            utils.move_all_files(self.temp_images_path, user_directory)
            self.attendance_dao.insert_new_user(self.name, self.charge)
            self._running = False
            self._captureThread.join()
            self.Destroy()
            exit()

        for shot in xrange(1, 5):
            success, image = self._capture.read()
            if success:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                equalized_image = cv2.equalizeHist(gray_image)
                faces = self._detector.detectMultiScale(equalized_image, scaleFactor=utils.scale_factor,
                                                        minNeighbors=utils.min_neighbors,  # For overlapping detections
                                                        minSize=self.min_size, flags=utils.flags)
                for x, y, width, height in faces:
                    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 1)

            if len(faces) > 0:
                x, y, width, height = faces[0]
                image = cv2.equalizeHist(gray_image[y:y + height, x:x + width])
                image = cv2.resize(image, (100, 100))
                image_name = self.name + '_' + str(self.train_step) + '_' + str(shot) + '.png'
                cv2.imwrite(self.temp_images_path + image_name, image)

        self.train_step += 1
        self.set_instructions(self.instructions[self.train_step])

    def _onCloseWindow(self, event):
        self._running = False
        self._captureThread.join()
        self._capture.release()
        self.Destroy()

    def _onQuitCommand(self, event):
        self.Close()

    def _runCaptureLoop(self):
        while self._running:
            success, image = self._capture.read()
            # if image is not None:
            if success:
                self.detect_faces(image)
                image[:] = numpy.fliplr(image)
            wx.CallAfter(self._showImage, image)

    def detect_faces(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        equalized_image = cv2.equalizeHist(gray_image)
        faces = self._detector.detectMultiScale(equalized_image, scaleFactor=utils.scale_factor,
                                                        minNeighbors=utils.min_neighbors,
                                                        minSize=self.min_size, flags=utils.flags)

        for face in faces:
            x, y, width, height = face
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 1)
            # top_y = cv.Round(y + height * EYE_SY)
            # width_x = cv.Round(x + width * EYE_SW)
            # height_y = cv.Round(y + height * EYE_SH)
            # left_x = cv.Round(x + width * EYE_SX + 10)
            # width_r = cv.Round(width_x + width * 0.5)
            # right_x = cv.Round(x + 15 + width * (1.0 - EYE_SX - EYE_SW))
            # cv2.rectangle(image, (left_x, top_y), (width_x, height_y), (255, 255, 255), 1)
            #
            # left_eye = cv2.equalizeHist(gray_image[top_y:top_y + height, left_x:left_x + width])
            # cv2.imwrite('eye.png', left_eye)
            # cv2.rectangle(image, (right_x, top_y), (width_r, height_y), (255, 255, 255), 1)

    def _showImage(self, image):
        if image is None:
            bitmap = wx.EmptyBitmap(self._imageWidth, self._imageHeight)
        else:
            # Convert the image to bitmap format.
            bitmap = utils.image_to_wxbitmap(image)
        # Show the bitmap.
        self._staticBitmap.SetBitmap(bitmap)

    def set_instructions(self, instruction):
        wx.CallAfter(self.instructions_label.SetLabel, instruction)


def main():
    app = wx.App()
    trainer = Trainer()
    trainer.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()