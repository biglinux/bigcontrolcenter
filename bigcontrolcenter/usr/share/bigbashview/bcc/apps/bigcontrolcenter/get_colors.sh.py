#!/usr/bin/env python3
import sys, math
from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtGui import QPalette

class Window(QWidget):
    """doc for class"""
    def __init__(self):
        super().__init__()
        Background = self.palette().color(QPalette.Window).name()
        COLORS = '''%s''' % (Background)
        print(COLORS)
        sys.exit()


app = QApplication(sys.argv)
main = Window()
app.exec_()

