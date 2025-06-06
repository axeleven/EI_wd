"""
Prend la base de donnée en entrée, et renvoie un à un un certain nombre de tweets que l'on va étiqueter manuellement (une centaine)
Il crée ensuite un fichier avec les tweets et les labels renseignés, afin de pouvoir simplement établir des règles pour correctement étiqueter un échantillon d'entrainement
"""


import pandas as pd
import random
import os


def etiqueter_csv(fichier_entree, nb_lignes, colonne_contenu="Content", fichier_sortie="etiquettes_resultat.csv"):
    #lecture du csv
    df = pd.read_csv(fichier_entree, sep=";", on_bad_lines='skip', engine='python')

    # tirage lignes aléatoires sans doublon
    nb_lignes = min(nb_lignes, len(df))
    lignes_choisies = df.sample(n=nb_lignes, random_state=42).reset_index(drop=True)

    etiquettes = []

    for i, ligne in lignes_choisies.iterrows():
        print(f"\nLigne {i + 1}/{nb_lignes} :\n---\n{ligne[colonne_contenu]}\n---")
        while True:
            label = input("Étiquette: ")
            if label in {"0", "1", "2"}:
                etiquettes.append(int(label))
                break
            else:
                print("Entrée invalide")


    #colonne étiquettes
    lignes_choisies["Label"] = etiquettes

    # Sauvegarde
    lignes_choisies.to_csv(fichier_sortie, index=False)
    print(f"\nfichier sauvegardé sous : {fichier_sortie}")




fichier_csv = input("Chemin du fichier CSV à étiqueter : ").strip()
nb = input("Nombre de lignes à étiqueter : ").strip()
etiqueter_csv(fichier_csv, int(nb))
