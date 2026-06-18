# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:36:14 2026

@author: 039976
"""

''' transformation du fichier source'''
def normalize_columns(df):
    """
    Normalise les noms de colonnes
    """
    mapping = {
        "ORGANE": "organe",
        "TYPE ATTEINTE": "type_atteinte",
        "INTERMEDIAIRE": "intermediaire",
        "DEFINITION": "definition",
        "CODE": "code"
    }

    df.columns = [col.strip().upper() for col in df.columns]

    try:
        df = df.rename(columns=mapping)
    except Exception:
        raise Exception("Erreur normalisation colonnes")

    required = list(mapping.values())

    for col in required:
        if col not in df.columns:
            raise Exception(f"Colonne manquante : {col}")

    return df[required]


def clean_data(df):
    """
    Nettoie les données
    """
    df = df.copy()

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    df = df.fillna("Non renseigné")

    df = df[df.any(axis=1)]

    return df


def filter_data(df, search_term, organe_filter="Tous"):
    """
    Filtre le DataFrame par organe puis par terme de recherche sur toutes les colonnes
    """
    df_filtered = df

    # 1. Filtrage par organe
    if organe_filter and organe_filter != "Tous":
        df_filtered = df_filtered[df_filtered["organe"].astype(str) == organe_filter]

    # 2. Filtrage textuel global
    if not search_term:
        return df_filtered

    search_term = search_term.lower()

    mask = df_filtered.apply(
        lambda row: search_term in " ".join(row.values.astype(str)).lower(),
        axis=1
    )

    return df_filtered[mask]