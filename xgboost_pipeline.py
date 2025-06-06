import pandas as pd
import spacy
import emoji
import joblib
import optuna
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import f1_score, cohen_kappa_score
from xgboost import XGBClassifier
from visualisation import vizualisation
print("hell no")
# Charger le modèle spaCy pour l'italien
nlp = spacy.load("it_core_news_sm")

def nettoyer_et_lemmatiser(texte):
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
X_text = df["texte_nettoye"]
y = df["label"]
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Vectorisation TF-IDF avec paramètres optimisés
tfidf_params = {
    'ngram_range': (1, 2),
    'min_df': 0.001,
    'max_df': 0.8,
    'max_features': 75000
}
vectorizer = TfidfVectorizer(**tfidf_params)
X_train_tfidf = vectorizer.fit_transform(X_train_text)
X_test_tfidf = vectorizer.transform(X_test_text)

# 4. Réduction de dimension avec TruncatedSVD
dim_reduction = TruncatedSVD(n_components=300, random_state=42)
X_train_reduced = dim_reduction.fit_transform(X_train_tfidf)
X_test_reduced = dim_reduction.transform(X_test_tfidf)

# 5. Définition de l'objectif Optuna (multi-objectifs: F1-macro et Kappa)
def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1500),
        'max_depth': trial.suggest_int('max_depth', 3, 17),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.35, log=True),
        'gamma': trial.suggest_float('gamma', 0.0, 1000),
        'subsample': trial.suggest_float('subsample', 0, 1),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0, 1),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 55),
        'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10),
        'objective': 'multi:softprob',
        'num_class': 3,
        'tree_method': 'hist',
        'device': 'cuda',
        'eval_metric': 'mlogloss',
        'early_stopping_rounds' : 20
    }
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train_reduced, y_train, test_size=0.2, random_state=trial.number, stratify=y_train
    )
    model = XGBClassifier(**params)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_val, y_val)],
        verbose=False
    )
    y_pred = model.predict(X_val)
    f1 = f1_score(y_val, y_pred, average='macro')
    kappa = cohen_kappa_score(y_val, y_pred)
    return f1, kappa

# 6. Création et optimisation de l'étude Optuna
study = optuna.create_study(directions=["maximize", "maximize"])
study.optimize(objective, n_trials=100)

# 7. Sélection du meilleur essai
best_trial = max(study.trials, key=lambda t: t.values[0])
best_params = best_trial.params
print("Meilleurs paramètres (selon F1-macro) :", best_params)
print("Values (F1, Kappa) :", best_trial.values)

# 8. Entraînement final
final_params = best_params.copy()
final_params.update({
    'objective': 'multi:softprob',
    'num_class': 3,
    'tree_method': 'hist',
    'device': 'cuda',
    'eval_metric': 'mlogloss'
})
final_model = XGBClassifier(**final_params)
final_model.fit(
    X_train_reduced, y_train,
    eval_set=[(X_test_reduced, y_test)],
    verbose=False
)

# 9. Évaluation sur l'ensemble de test
y_pred_test = final_model.predict(X_test_reduced)
f1_final = f1_score(y_test, y_pred_test, average='macro')
kappa_final = cohen_kappa_score(y_test, y_pred_test)
print(f"F1-macro sur test set: {f1_final:.4f}")
print(f"Kappa de Cohen sur test set: {kappa_final:.4f}")

# 10. Visualisation et sauvegarde
vizualisation(y_test, y_pred_test, "XGBoost Optuna (GPU) avec early stopping")
joblib.dump(final_model, "xgb_modele_gpu_optuna_es2.joblib")
joblib.dump(vectorizer, "tfidf_vectorizer_ameliore2.joblib")
joblib.dump(dim_reduction, "svd_dim_reduction2.joblib")
