import sys
import os

# Ensure the root directory is in the python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.path_manager import get_data_path
from data.loader import load_excel
from data.processor import normalize_columns, clean_data, filter_data
from visualization.mindmap import generate_mindmap

def run_tests():
    print("--- DÉBUT DES TESTS ---")
    
    # Test 1: Chargement des données
    try:
        print("1. Test de chargement des données...")
        path = get_data_path()
        print(f"   Chemin des données: {path}")
        df = load_excel(path)
        print(f"   Données chargées avec succès. Nombre de lignes: {len(df)}")
    except Exception as e:
        print(f"   [ERREUR] Échec du chargement des données: {e}")
        return

    # Test 2: Nettoyage et normalisation
    try:
        print("2. Test de normalisation et nettoyage...")
        df = normalize_columns(df)
        df = clean_data(df)
        print(f"   Données nettoyées. Colonnes: {list(df.columns)}")
    except Exception as e:
        print(f"   [ERREUR] Échec du nettoyage: {e}")
        return

    # Test 3: Filtrage
    try:
        print("3. Test du filtrage des données...")
        search_term = "nerveux"
        df_filtered = filter_data(df, search_term)
        print(f"   Filtrage par '{search_term}': {len(df_filtered)} lignes trouvées.")
    except Exception as e:
        print(f"   [ERREUR] Échec du filtrage: {e}")
        return

    # Test 4: Génération de la carte mentale
    try:
        print("4. Test de génération de la carte mentale (mindmap)...")
        # On passe un df_filtered pour aller plus vite, mais on peut tester le complet si besoin
        html_path = generate_mindmap(df_filtered, search_term)
        print(f"   Carte mentale générée avec succès à l'emplacement : {html_path}")
        if os.path.exists(html_path):
            print(f"   Le fichier HTML existe et pèse {os.path.getsize(html_path)} octets.")
        else:
            print(f"   [ERREUR] Le fichier {html_path} est introuvable.")
    except Exception as e:
        print(f"   [ERREUR] Échec de la génération de la carte: {e}")
        return

    print("--- TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS ---")

if __name__ == "__main__":
    run_tests()
