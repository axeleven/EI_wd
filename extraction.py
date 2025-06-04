"""
A partir de la base de données complète, extrait un échantillon tiré aléatoirement
"""

import pandas as pd
import csv

def detecter_separateur(fichier):
    # Ouvre le fichier et lit la première ligne pour détecter automatiquement le séparateur
    with open(fichier, 'r', encoding='utf-8', errors='replace') as f:
        dialect = csv.Sniffer().sniff(f.readline(), delimiters=";,")
    return dialect.delimiter

def extraire_lignes(fichier_entree, nb_lignes, fichier_sortie="big_echantillon.csv"):

    sep = detecter_separateur(fichier_entree)

    #lecture
    df = pd.read_csv(fichier_entree, sep=sep, on_bad_lines="skip", engine="python")

    # tirage aléatoire 
    df_sample = df.sample(n=min(nb_lignes, len(df)), random_state=42).reset_index(drop=True)


    # sauvegarde
    df_sample.to_csv(fichier_sortie, index=False)
    print(f"{len(df_sample)} lignes enregistrées dans : {fichier_sortie}")



fichier = input("Chemin du fichier CSV : ").strip()
nb = int(input("Nombre de lignes à extraire : ").strip())
extraire_lignes(fichier, nb, "big_echantillon.csv")
