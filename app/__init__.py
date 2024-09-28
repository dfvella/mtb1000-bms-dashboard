import enum
import time
import threading
import sys
import ctypes

from PyQt5 import QtCore, QtWidgets, uic, QtGui, QtTest

import serial
from serial.tools import list_ports

WINDOWS_APPID = u'mracing.telemetry.viewer.version'
