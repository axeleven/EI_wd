import pandas as pd
import spacy
import emoji
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from visualisation import vizualisation

nlp = spacy.load("it_core_news_sm")


def nettoyer_et_lemmatiser(texte):
    """
    Nettoie et lemmatise un texte en italien en utilisant le modèle de langue italienne de spaCy.

    Cette fonction prend un texte en entrée, le convertit en minuscules, et utilise spaCy pour
    effectuer une analyse linguistique. Elle retourne une version nettoyée et lemmatisée du texte,
    en excluant les mots vides, la ponctuation, les URLs et les adresses e-mail.

    On utilise également la bibliothèque emoji pour traduire les emojis du texte.
    """
    texte = emoji.demojize(texte, delimiters=("", ""))
    doc = nlp(texte.lower())   
    blockwords = {"rt"}
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.like_url
        and not token.like_email
        and not token.text.startswith("@")
        and token.lemma_ not in blockwords
    ]
    return " ".join(tokens)

df = pd.read_csv("maxi_label.csv")

df = df.dropna(subset=["Content", "label"])


df["texte_nettoye"] = df["Content"].apply(nettoyer_et_lemmatiser)

# Séparation des données en ensembles d'entraînement et de test: on fixe la seed à 42, on utilise un stratifié pour conserver la proportion des classes
X_train, X_test, y_train, y_test = train_test_split(
    df["texte_nettoye"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

## Vectorisation et entraînement du modèle -> on fait le choix de la vectorisation TF-IDF et du classifieur Naive Bayes multinomial
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

for alpha in [0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]:
    clf = MultinomialNB(alpha=alpha)
    clf.fit(X_train_vec, y_train)
    y_pred_tmp = clf.predict(X_test_vec)
    vizualisation(y_test, y_pred_tmp, alpha)



