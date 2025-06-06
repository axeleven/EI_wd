"""
Afin d'étiqueter de manière déterministe un échantillon d'entrainement pour les truth, on veut un dictionnaire qui étant donné un mot, donne son "score de colère"
L'algorithme présente un nombre donné de truth, et pour chacun, l'utilisateur attribue un score de colère.
Ensuite, pour chacun de ces truth, l'algorithme analyse d'abord s'il contient des points d'exclamation
Puis, il tokenise le truth, et pour chacun des mots, il ajoute son score dans un dictionnaire
A la fin, le score d'un mot (et du point d'exlamation) sera la moyenne des scores de colère des tweets dans lequel il apparaît
"""

import emoji
import spacy

def type_de_caractere(c):
    if len(c) != 1:
        return "erreur"
    if c.islower():
        return "minuscule"
    elif c.isupper():
        return "majuscule"
    elif c.isalpha():
        return "lettre (non standard)"
    else:
        return "pas une lettre"
    

nlp = spacy.load("en_core_news_sm")

def nettoyer_et_lemmatiser(texte):
    texte = emoji.demojize(texte, delimiters=("", ""))
    doc = nlp(texte.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.like_url and not token.like_email
    ]
    return " ".join(tokens)


import pandas as pd
import os



def attribution_scores(fichier_entree, nb_lignes, colonne_contenu="Content"):
    score_termes = {'!':(0,0)}

    #lecture du fichier
    df = pd.read_csv(fichier_entree, sep=";", on_bad_lines='skip', engine='python')

    # tirage lignes aléatoires sans doublon
    nb_lignes = min(nb_lignes, len(df))
    lignes_choisies = df.sample(n=nb_lignes, random_state=42).reset_index(drop=True)

    for i, ligne in lignes_choisies.iterrows():
        #décompte des points d'exclamation
        count_excla = 0

        for c in ligne[colonne_contenu]:
            if c == '!':
                count_excla +=1

        #tokenisation
        tok = (nettoyer_et_lemmatiser(ligne[colonne_contenu])).split()


        print(f"\nLigne {i + 1}/{nb_lignes} :\n---\n{ligne[colonne_contenu]}\n---")
        while True:
            #l'utilisateur renseigne le pourcentage de colère
            score = (float(input("Étiquette (0 à 100) : ")))/100
            if 0 <= score <= 1:

                #on ajoute le score des points d'exclamation détectés
                score_termes["!"][0] += score*count_excla
                score_termes["!"][1] += count_excla

                #ajout des scores de colère des mots
                for elt in tok:
                    if elt in score_termes:
                        score_termes[elt][0] += score 
                        score_termes[elt][1] +=1

                    else:
                        score_termes[elt] = [score ,1]
                
                break
         
            else:
                print("Entrée invalide. Veuillez un nombre entre 0 et 1")

    for token,(sum,nb) in score_termes.items():
        score_termes[token] = sum/nb

    return (score_termes)




fichier_csv = input("Chemin du fichier CSV à étiqueter : ").strip()
nb = input("Nombre de lignes à étiqueter : ").strip()
attribution_scores(fichier_csv, int(nb))

