"""
Choix d'apprentissage pour les scores de colère:
Prédiction d'un score --> Régression
Moins de 100K truth et peu de mots servent à caractériser la colère (il s'agit rarement de textes construits)
--> Régression de Lasso
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV



import emoji
import spacy



nlp = spacy.load("en_core_news_sm")

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
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.like_url and not token.like_email
    ]
    return " ".join(tokens)



#lecture
df = pd.read_csv("tweets_colere.csv")  # change le nom du fichier si besoin
df["Content_nettoye"] = df["Content"].astype(str).apply(nettoyer_et_lemmatiser)

X = df["Content_nettoye"]
y = df["colere_score"]  

#séparation de l'échantillon: 20% test, 80% apprentissage
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=2000)),
    ("lasso", Lasso(max_iter=100000))
])

param_grid = {
    "lasso__alpha": [0.001, 0.01, 0.1, 1.0, 10.0]
}

grid = GridSearchCV(pipeline, param_grid, cv=3, scoring="r2", verbose=1)
grid.fit(X_train, y_train)


y_pred = grid.predict(X_test)


print("meilleur alpha :", grid.best_params_["lasso__alpha"])
print("MSE :", mean_squared_error(y_test, y_pred))
print("R²  :", r2_score(y_test, y_pred))


best_lasso = grid.best_estimator_.named_steps["lasso"]
vectorizer = grid.best_estimator_.named_steps["tfidf"]

coefs = best_lasso.coef_
features = vectorizer.get_feature_names_out()
mots_importants = [(features[i], coef) for i, coef in enumerate(coefs) if coef != 0]
mots_importants = sorted(mots_importants, key=lambda x: abs(x[1]), reverse=True)

print("\nMots les plus liés à la colère :")
for mot, poids in mots_importants[:20]:
    print(f"{mot:20s} → {poids:.4f}")

