# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:25:04 2026

@author: 039976
"""

''' Path manager.py'''

import sys
import os

def get_data_path():
    """
    Retourne le chemin du fichier de données
    Compatible environnement dev et .exe (PyInstaller)
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "data", "donnees.xlsx") 
