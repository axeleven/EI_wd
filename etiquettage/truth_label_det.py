"""
Etiquetage déterministe de l'échantillon d'entrainement pour truth
Etiquette d'un truth: moyenne des scores de colère de ses tokens (scores renseignés dans dict_tokens) (si un token n'est pas dans le dictionnaire, il est simplement ignoré), ajusté par sa teneur en majuscules
"""

import emoji
import spacy

nlp = spacy.load("en_core_news_sm")

def nettoyer_et_lemmatiser(texte):
    texte = emoji.demojize(texte, delimiters=("", ""))
    doc = nlp(texte.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.like_url and not token.like_email
    ]
    return " ".join(tokens)



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
    


def score_truth(str, dict_tokens):
    count_excla = 0
    count_maj = 0
    count_lettre = 0

    #parcourt le truth avant la tokenisation pour analyser la ponctuation et les majuscules/minuscules
    for c in str:
        if c == '!':
            count_excla +=1

        if type_de_caractere(c) == "majuscule":
            count_maj +=1 
            count_lettre +=1
        
        if type_de_caractere(c) == "minuscule":
            count_lettre +=1       

    #proportion de majuscules parmi les lettres
    prop_maj = count_maj/count_lettre

    #tokenisation
    tokens = (nettoyer_et_lemmatiser(str)).split()

    #score de colère du truth
    mean = 0

    tokens_comptabilises = 0

    for elt in tokens:
        if elt in dict_tokens:
            mean += dict_tokens[elt]
            tokens_comptabilises +=1
    
    mean += count_excla * (dict_tokens['!'])


    mean = mean/(count_excla + tokens_comptabilises)

    #prise en compte des majuscules: s'il y en a plus de 50%, on ajoute au score son reste pondéré par le pourcentage de majuscules
    if prop_maj>0.5:
        reste = 1 - mean
        mean += prop_maj*reste

    return mean

    




import pandas as pd

def ajouter_labels(fichier_entree, fichier_sortie, colonne_texte="Content"):
    # lecture échantillon
    df = pd.read_csv(fichier_entree)

    # étiquetage
    df["label"] = df[colonne_texte].astype(str).apply(score_truth)

    # sauvegarde
    df.to_csv(fichier_sortie, index=False)
    print(f"fichier sauvegardé sous : {fichier_sortie}")



entree = input("Chemin du fichier échantillon CSV : ").strip()
sortie = input("Nom du fichier de sortie : ").strip()
ajouter_labels(entree, sortie)
