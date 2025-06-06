import pandas as pd
import spacy
import emoji
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from ML_classification_algorithm.visualisation import vizualisation
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
import multiprocessing

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
param_grid = {
    'n_estimators': [500],
    'max_depth': [12],
    'learning_rate': [0.3],
    'gamma': [0.25],
    'min_child_weight': [1]
}

xgb_clf_grid = XGBClassifier(objective='binary:logistic', random_state=42, eval_metric='logloss', n_jobs=multiprocessing.cpu_count()//2)
grid_search = GridSearchCV(xgb_clf_grid, param_grid, cv=5, scoring='accuracy', n_jobs=2, verbose=1)
grid_search.fit(X_train_vec, y_train)

print("Meilleurs paramètres :", grid_search.best_params_)

xgb_clf = grid_search.best_estimator_
xgb_clf.fit(X_train_vec, y_train)
y_pred_xgb = xgb_clf.predict(X_test_vec)
vizualisation(y_test, y_pred_xgb, "XGBoost")
