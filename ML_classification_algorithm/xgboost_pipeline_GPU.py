import pandas as pd
import spacy
import emoji
import joblib
import optuna
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import f1_score, cohen_kappa_score
from xgboost import XGBClassifier
from ML_classification_algorithm.visualisation import vizualisation
# Charger le modèle spaCy pour l'italien
#TODO: Entrainer le modèle sur un dataset anglophone.
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

# Prepocessing
df = pd.read_csv("../datasets/dataset.csv")
df = df.dropna(subset=["Content", "label"])
df["texte_nettoye"] = df["Content"].apply(nettoyer_et_lemmatiser)

# Séparation des données: 80% train, 20% test et stratification par label
X_text = df["texte_nettoye"]
y = df["label"]
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text, y, test_size=0.2, random_state=42, stratify=y
)

# vectorisation tf-idf

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train_text)
X_test_tfidf = vectorizer.transform(X_test_text)

# réduction de dimension avec SVD
dim_reduction = TruncatedSVD(n_components=300, random_state=42)
X_train_reduced = dim_reduction.fit_transform(X_train_tfidf)
X_test_reduced = dim_reduction.transform(X_test_tfidf)

# Définition de la fonction objectif d'Optuna
def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 12),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'gamma': trial.suggest_float('gamma', 0.0, 1000),
        'subsample': trial.suggest_float('subsample', 0, 1),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0, 1),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 50),
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


study = optuna.create_study(directions=["maximize", "maximize"])
study.optimize(objective, n_trials=100)

# sélection du meilleur essai
best_trial = max(study.trials, key=lambda t: t.values[0])
best_params = best_trial.params
print("Meilleurs paramètres (selon F1-macro) :", best_params)
print("Values (F1, Kappa) :", best_trial.values)

# entrainement du modèle final avec les meilleurs paramètres
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


y_pred_test = final_model.predict(X_test_reduced)
vizualisation(y_test, y_pred_test, "XGBoost Optuna (GPU) avec early stopping")
# sauvegarde (l'optimisation des paramètres est très longue, on veut éviter de la refaire)
joblib.dump(final_model, "xgb_modele_gpu_optuna_es2.joblib")
joblib.dump(vectorizer, "tfidf_vectorizer_ameliore2.joblib")
joblib.dump(dim_reduction, "svd_dim_reduction2.joblib")