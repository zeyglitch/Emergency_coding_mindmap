# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:26:39 2026

@author: 039976
"""

'''data loader'''

import pandas as pd

def load_excel(file_path):
    """
    Charge le fichier Excel et retourne un DataFrame pandas
    """
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        return df
    except Exception as e:
        raise Exception(f"Erreur chargement fichier Excel: {str(e)}")    

