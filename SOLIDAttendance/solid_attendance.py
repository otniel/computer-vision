import binascii
import cv2
import numpy as np
import os
import sys
import threading
import wx
import utils
from trainer import Trainer
from solid_attendance_dao import SolidAttendanceDao


THRESHOLD_FACE_RECOGNITION = 1200


def fourCharsToInt(s):
    return int(binascii.hexlify(s), 16)

def intToFourChars(i):
    return binascii.unhexlify(format(i, 'x'))


class SolidAttendance(wx.Frame):
    def __init__(self):

        self._running = True
        self.users_dao = SolidAttendanceDao()
        self._capture = cv2.VideoCapture(utils.camera_device_id)
        size = utils.resize_video_capture_with_image_size(self._capture, utils.frame_size)
        self._imageWidth, self._imageHeight = size
        self._currDetectedObject = None

        self._recognizer = cv2.createFisherFaceRecognizer()
        pictures, labels = utils.get_pictures_and_labels()
        self._recognizer.train(np.array(pictures), np.array(labels))

        cascade_path = utils.resource_path('cascades/haarcascade_frontalface_alt2.xml')
        self._detector = cv2.CascadeClassifier(cascade_path)

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

        self._predictionStaticText = wx.StaticText(self)
        # Insert an end line for consistent spacing.
        self._predictionStaticText.SetLabel('\n')

        self._updateModelButton = wx.Button(self, label='Train')
        self._updateModelButton.Bind(wx.EVT_BUTTON, self._updateModel)

        border = 12
        self._recognizerTrained = True

        controls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        controls_sizer.Add(self._updateModelButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border)
        # controls_sizer.Add(self._predictionStaticText, 0, wx.ALIGN_CENTER_VERTICAL)

        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self._staticBitmap)
        rootSizer.Add(controls_sizer, 0, wx.EXPAND | wx.ALL, border)
        self.SetSizerAndFit(rootSizer)

        self._captureThread = threading.Thread(target=self._runCaptureLoop)
        self._captureThread.start()

    def _onCloseWindow(self, event):
        self._running = False
        self._captureThread.join()
        self.Destroy()

    def _updateModel(self, event):
        self._running = False
        self._captureThread.join()
        self._capture.release()
        trainer = Trainer()
        trainer.Show()
        self.Close()

    def _onQuitCommand(self, event):
        self.Close()

    def _onReferenceTextCtrlKeyUp(self, event):
        self._enableOrDisableUpdateModelButton()

    def _runCaptureLoop(self):
        while self._running:
            success, image = self._capture.read()
            if success:
                self.detect_faces(image)
                #image[:] = np.fliplr(image)
            wx.CallAfter(self._showImage, image)

    def detect_faces(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        equalized_gray_image = cv2.equalizeHist(gray_image)
        # equalized_gray_image = cv2.resize(equalized_gray_image, (100, 100))
        faces = self._detector.detectMultiScale(equalized_gray_image, scaleFactor=utils.scale_factor,
                                                        minNeighbors=utils.min_neighbors,
                                                        minSize=self.min_size, flags=utils.flags)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            test_image = cv2.equalizeHist(gray_image[y:y + h, x:x + w])
            self._currDetectedObject = cv2.resize(test_image, (100, 100))
            if self._recognizerTrained:
                try:
                    labelAsInt, distance = self._recognizer.predict(self._currDetectedObject)
                    if distance > THRESHOLD_FACE_RECOGNITION:
                        cv2.putText(image, "Face not found! Please train the system." , (x, y), fontFace=cv2.cv.CV_FONT_HERSHEY_SIMPLEX,
                                fontScale=0.4, color=(0, 255, 0))
                    else:
                        name, charge = self.users_dao.get_user_by_id(labelAsInt)
                        cv2.putText(image, "Name: %s, Charge: %s, Distance: %s" % (name, charge, distance), (x, y), fontFace=cv2.cv.CV_FONT_HERSHEY_SIMPLEX,
                                    fontScale=0.4, color=(0, 255, 0))
                except cv2.error:
                    print >> sys.stderr, 'Recreating model due to error.'
            else:
                self._showInstructions()

    def _showImage(self, image):
        if image is None:
            bitmap = wx.EmptyBitmap(self._imageWidth, self._imageHeight)
        else:
            # Convert the image to bitmap format.
            bitmap = utils.image_to_wxbitmap(image)
        # Show the bitmap.
        self._staticBitmap.SetBitmap(bitmap)

    def _showInstructions(self):
        self._showMessage('When an object is highlighted, type its name\n(max 4 chars) and click "Add to Model".')

    def _clearMessage(self):
        # Insert an endline for consistent spacing.
        self._showMessage('\n')

    def _showMessage(self, message):
        wx.CallAfter(self._predictionStaticText.SetLabel, message)


def main():
    app = wx.App()
    solid_attendance = SolidAttendance()
    solid_attendance.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()