import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QSlider, QSpinBox, QPushButton, QFileDialog, QGroupBox
)
from PyQt5.QtGui import QPainter, QPixmap, QTransform
from PyQt5.QtCore import Qt, QTimer, QUrl, QPropertyAnimation, pyqtProperty, pyqtSignal, QObject
from PyQt5.QtMultimedia import QSoundEffect
import subprocess
import json
