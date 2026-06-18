# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:19:35 2026

@author: 039976
"""

'''Main.py (point d'entrée)'''
         
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())