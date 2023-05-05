"""
QCircularProgressBar: A customizable circular progress bar widget for PyQt6

This module provides a circular progress bar widget for PyQt6 applications.
The progress bar can be customized in terms of colors, text, and appearance.
It is designed to be easily integrated into any PyQt6 application.

Author: luandiasrj (https://github.com/luandiasrj)
Url:
https://github.com/luandiasrj/QCircularProgressBar_-_New_QProgressBar_for_PyQT6
License: GNU General Public License v3.0
Date: 2023-05-04

Usage:
Import the QCircularProgressBar class and add it to your application as a
widget. You can customize the appearance of the progress bar by setting its
properties and using style sheets.

Example:
See the ProgressBarExample class in this module for a demonstration of how
to use the QCircularProgressBar widget.
"""
import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QTimer, Qt, pyqtProperty
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QLabel, QSizePolicy)


class QCircularProgressBar(QWidget):
    bg_color1 = pyqtProperty(
        str, lambda self: QColor(self._bg_color1).name(), lambda self, col:
        setattr(self, "_bg_color1", col), )
    bg_color2 = pyqtProperty(
        str, lambda self: QColor(self._bg_color2).name(), lambda self, col:
        setattr(self, "_bg_color2", col), )
    mask_color = pyqtProperty(
        str, lambda self: QColor(self._mask_color).name(), lambda self, col:
        setattr(self, "_mask_color", col), )
    text_color = pyqtProperty(
        str, lambda self: QColor(self._text_color).name(), lambda self, col:
        setattr(self, "_text_color", col), )
    text_bg_color = pyqtProperty(
        str, lambda self: QColor(self._text_bg_color).name(), lambda self, col:
        setattr(self, "_text_bg_color", col), )

    def __init__(self, parent=None):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(16)  # ~60 FPS
        self.angle = 0
        self.current_value = 0

        self._bg_color1 = "rgb(0, 255, 255)"
        self._bg_color2 = "rgb(0, 69, 142)"
        self._mask_color = "rgb(227, 227, 227)"
        self._text_color = "rgb(0, 0, 0)"
        self._text_bg_color = "rgb(255, 255, 255)"

        self.Circle_size = 160  # Widget Size
        chunk_size = int(self.Circle_size * 0.07)
        self.center_radius = int(
            self.Circle_size * 0.43)  # Center Circle Size (0.43 + 0.07 = 0.5)
        self.percent_size = int(self.Circle_size * 0.25)  # Percentil Size
        self.text_size = int(self.Circle_size * 0.12)

        self.alignment = None
        self.description = ""
        self.indicator = None
        self.progress = None

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.ProgressBack = QWidget(parent)
        self.ProgressBack.setObjectName("ProgressBack")
        self.ProgressBack.setMinimumSize(
            QtCore.QSize(self.Circle_size, self.Circle_size))
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed,
                                  QSizePolicy.Policy.Fixed)
        self.ProgressBack.setSizePolicy(size_policy)
        self.ProgressBack_2 = QVBoxLayout(self.ProgressBack)
        self.ProgressBack_2.setObjectName("ProgressBack_2")
        self.ProgressBack_2.setContentsMargins(0, 0, 0, 0)

        self.ProgressIndicator = QWidget(self.ProgressBack)
        self.ProgressIndicator.setObjectName("ProgressIndicator")

        self.ProgressIndicator_2 = QVBoxLayout(self.ProgressIndicator)
        self.ProgressIndicator_2.setObjectName("ProgressIndicator_2")
        self.ProgressIndicator_2.setContentsMargins(
            chunk_size, chunk_size, chunk_size, chunk_size)

        self.ProgressLabel = QLabel(self.ProgressIndicator)
        self.ProgressLabel.setObjectName("ProgressLabel")

        self.ProgressIndicator_2.addWidget(self.ProgressLabel)
        self.ProgressBack_2.addWidget(self.ProgressIndicator)
        self.layout.addWidget(self.ProgressBack,
                              alignment=Qt.AlignmentFlag.AlignCenter)

    def setValue(self, value):
        self.current_value = value

    def setFormat(self, text):
        self.description = text
        self.update_font_size()

    def setLabelStyleSheet(self):
        style = (
                "border-radius:" + str(self.center_radius) +
                "px; background-color:" + self._text_bg_color + ";")
        self.ProgressLabel.setStyleSheet(style)

    def update_label(self):
        if self.description is None:
            text = ""
            self.percent_size = int(self.Circle_size * 0.25)
        else:
            text = self.description

        percentage = str(round(self.current_value, None))

        sup_size = int(self.percent_size * 0.75)

        self.progress = self.current_value / 100
        self.indicator = 270 - (self.current_value * 3.6)
        stop1 = 1.000 - self.progress
        stop2 = 0.999 - self.progress

        self.update_style_sheet(stop1, stop2)

        if self.current_value != 0:
            if text != "":
                f_text = (
                        '<br><span style="color:' + self.text_color
                        + ";font-size:" + str(self.text_size) + 'px;">'
                        + text + "</span>")
            else:
                f_text = ""
            style = (
                    '<p align="center"><span style="font-weight: 500;color:' +
                    self.text_color + ";font-size:" + str(self.percent_size) +
                    'px;">' + percentage + '<span style="font-size:' +
                    str(sup_size) + 'px;"><sup>%</sup></span>' + f_text +
                    "</p></body></html>")
            self.ProgressLabel.setText(style)

    def update_font_size(self):
        max_characters = 11
        text_length = len(self.description)
        if text_length > max_characters:
            shrink_factor = max_characters / text_length
            self.text_size = int((self.Circle_size * 0.14) * shrink_factor)
        else:
            self.text_size = int(self.Circle_size * 0.12)

    def update_style_sheet(self, stop1, stop2):
        if stop1 < 0:
            stop1 = 0.001
        if stop2 < 0:
            stop2 = 0.000
        base_style = (
                "background-color: qconicalgradient(cx:0.5, cy:0.5, angle:270, "
                "stop:" + str(stop1) + " " + "rgba(255,255,255, 0), stop:"
                + str(stop2) + " " + self._mask_color + ");")
        self.ProgressIndicator.setStyleSheet(base_style)

    def rotate(self):
        self.angle -= 1
        radius = int(self.Circle_size / 2)
        base_style = (
                "border: 0px; background-color: qconicalgradient(cx:0.5,cy:0.5,"
                " angle:" + str(self.angle) + ", stop:0 " + self._bg_color1 +
                ", stop:0.5 " + self._bg_color2 + ", stop:1 " + self._bg_color1
                + "); border-radius:" + str(radius) + "px")
        self.ProgressBack.setStyleSheet(base_style)
        self.setLabelStyleSheet()
        self.update_label()

    def setAlignment(self, alignment):
        self.alignment = alignment

    def setMinimumWidth(self, width):
        self.ProgressBack.setMinimumWidth(width)


# ============== Example ==============
class ProgressBarExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Example QProgressBar")
        self.setGeometry(100, 100, 300, 100)

        self.progress_bar = QCircularProgressBar()
        self.progress_bar.setStyleSheet(
            "QCircularProgressBar {"
            "qproperty-bg_color1: #0F0;"
            "qproperty-bg_color2: #006600;"
            "qproperty-mask_color: #afa;"
            "qproperty-text_color: #006600;"
            "qproperty-text_bg_color: #dfd;}"
        )
        self.progress_bar.setFormat("Loading...")
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(10)

    def update_progress_bar(self):
        if self.progress_bar.current_value < 100:
            self.progress_bar.setValue(self.progress_bar.current_value + 0.1)
        else:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ProgressBarExample()
    window.show()

    sys.exit(app.exec())
