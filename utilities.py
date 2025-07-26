import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QSlider, QSpinBox 
)
from PyQt5.QtGui import QPainter, QPixmap, QTransform
from PyQt5.QtCore import Qt, QTimer, QUrl, QPropertyAnimation, pyqtProperty
from PyQt5.QtMultimedia import QSoundEffect
import subprocess