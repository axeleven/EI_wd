import pandas as pd
import spacy
import emoji
import joblib
import optuna
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from visualisation import vizualisation
from xgboost import XGBClassifier

# Charger le modèle spaCy pour l'italien
nlp = spacy.load("it_core_news_sm")

def nettoyer_et_lemmatiser(texte):
    """
    Nettoie et lemmatise un texte en italien en utilisant spaCy et emoji.
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

# 1. Lecture et prétraitement des données
df = pd.read_csv("dataset.csv")
df = df.dropna(subset=["Content", "label"])
df["texte_nettoye"] = df["Content"].apply(nettoyer_et_lemmatiser)

# 2. Séparation en train/test
X_train, X_test, y_train, y_test = train_test_split(
    df["texte_nettoye"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# 3. Vectorisation TF-IDF
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. Définition de l'objectif Optuna
def objective(trial):
    # Définir la plage de recherche pour chaque hyperparamètre
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 2000),
        "max_depth": trial.suggest_int("max_depth", 3, 15),
        "learning_rate": trial.suggest_loguniform("learning_rate", 0.01, 0.4),
        "gamma": trial.suggest_loguniform("gamma", 1e-3, 0.5),
        "subsample": trial.suggest_uniform("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_uniform("colsample_bytree", 0.5, 1.0),
        "reg_lambda": trial.suggest_loguniform("reg_lambda", 1e-3, 10.0),
        "reg_alpha": trial.suggest_loguniform("reg_alpha", 1e-3, 10.0),
    }
    # Ajouter les paramètres GPU
    xgb = XGBClassifier(
        **params,
        objective='multi:softprob',
        num_class=3,
        tree_method="gpu_hist",
        predictor="gpu_predictor",
        gpu_id=0,
        use_label_encoder=False,
        eval_metric="logloss"
    )
    # Cross-validation 5-fold
    scores = cross_val_score(xgb, X_train_vec, y_train, cv=5, scoring="accuracy", n_jobs=2)
    return scores.mean()

# 5. Lancer l’optimisation avec Optuna
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100)

print("Meilleurs paramètres Optuna :", study.best_params)
print("Meilleure accuracy CV :", study.best_value)

# 6. Entraînement final avec les meilleurs paramètres sur tout l'ensemble d'entraînement
best_params = study.best_params
xgb_best = XGBClassifier(
    **best_params,
    objective="binary:logistic",
    tree_method="gpu_hist",
    predictor="gpu_predictor",
    gpu_id=0,
    use_label_encoder=False,
    eval_metric="logloss"
)
xgb_best.fit(X_train_vec, y_train)

# 7. Prédiction et visualisation sur l’ensemble de test
y_pred_xgb = xgb_best.predict(X_test_vec)
vizualisation(y_test, y_pred_xgb, "XGBoost Optuna (GPU)")

# 8. Sauvegarde du modèle et du vectorizer
joblib.dump(xgb_best, "xgb_modele_gpu_optuna.joblib")
joblib.dump(vectorizer, "tfidf_vectorizer.joblib")
