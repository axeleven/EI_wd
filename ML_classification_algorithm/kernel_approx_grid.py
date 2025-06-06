"""
Apprentissage avec l'algorithme de régression logistique, après un échantillonage des données à l'aide d'un RBF sampler
Optimisation des hyperparamètres avec grid search cv 
"""


import emoji
import spacy
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

nlp = spacy.load("it_core_news_sm")

def nettoyer_et_lemmatiser(texte):
    texte = emoji.demojize(texte, delimiters=("", ""))
    doc = nlp(texte.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.like_url and not token.like_email
    ]
    return " ".join(tokens)

#récupération et lemmatisation des tweets
df = pd.read_csv("equilibre.csv")
df["Content_nettoye"] = df["Content"].astype(str).apply(nettoyer_et_lemmatiser)

X = df["Content_nettoye"]
y = df["label"]

#séparation de l'échantillon: 20% test, 80% apprentissage
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#pipeline et grille des hyperparamètres pour le grid search
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("rbf", RBFSampler()),
    ("clf", LogisticRegression(max_iter=1000))])

param_grid = {
    "tfidf__max_features": [1700, 1750, 1800],
    "rbf__gamma": [0.325, 0.35, 0.375],
    "rbf__n_components": [1300, 1350],
    "clf__C": [350, 400,450]}


grid = GridSearchCV(
    pipeline,
    param_grid=param_grid,
    cv=3,
    scoring="f1_macro",
    verbose=2,
    n_jobs=-1
)

# apprentissage
grid.fit(X_train, y_train)
print("Meilleurs paramètres :", grid.best_params_)


# différents paramètres d'évaluation
y_pred = grid.predict(X_test)
print(classification_report(y_test, y_pred))


"""
Meilleurs paramètres : {'clf__C': 400, 'rbf__gamma': 0.35, 'rbf__n_components': 1300, 'tfidf__max_features': 1750}
              precision    recall  f1-score   support

           0       0.73      0.76      0.74       484
           1       0.77      0.74      0.75       518
           2       1.00      1.00      1.00         1

    accuracy                           0.75      1003
   macro avg       0.83      0.83      0.83      1003
weighted avg       0.75      0.75      0.75      1003
"""