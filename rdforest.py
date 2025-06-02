##import des fonctions utiles
import spacy
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

#from import as data_lab #importation des données étiquetées

nlp = spacy.load("it_core_news_sm") #chargement du modèle spacy

data = [
    ("J'adore ce produit, il est génial !", "positif"),
    ("Ce film est une vraie perte de temps.", "négatif"),
    ("Excellent service, très satisfait.", "positif"),
    ("Horrible expérience, je ne reviendrai jamais.", "négatif"),
    ("Le produit est bien, mais le service client est nul.", "négatif"),
    ("C'était parfait du début à la fin.", "positif"),
]

df = pd.DataFrame(data, columns=["tweet", "label"]) 


def preprocess(text):
    doc = nlp(text)
    tokens = [
        token.lemma_.lower() #renvoie le lemme en minuscule de chaque mot
        for token in doc
        if not token.is_stop and not token.is_punct and not token.like_url and not token.like_num #filtrage des token vides de sens
    ]
    return " ".join(tokens) #renvoie la liste de token sous la forme d'un unique string



df["clean"] = df["tweet"].apply(preprocess) # crée une nouvelle colonne contenant les txeet netoyés



