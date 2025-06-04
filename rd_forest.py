##import des fonctions utiles
import spacy
import emoji
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

#from import as data_lab #importation des données étiquetées




nlp = spacy.load("it_core_news_sm") #chargement du modèle spacy

'''data = [
    ("J'adore ce produit, il est génial !", "positif"),
    ("Ce film est une vraie perte de temps.", "négatif"),
    ("Excellent service, très satisfait.", "positif"),
    ("Horrible expérience, je ne reviendrai jamais.", "négatif"),
    ("Le produit est bien, mais le service client est nul.", "négatif"),
    ("C'était parfait du début à la fin.", "positif"),
]'''

data = pd.read_csv("C:\\Users\\jean\\Documents\\CS\\Cours 1A\\ST4 Data web\\ei_wd\\equilibre.csv")
df = pd.DataFrame(data, columns=["Content", "label"]) 

def preprocess(text):
    if not isinstance(text, str):
        text = ""
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.text.startswith("@"):
            continue  # On saute ce token
        if emoji.is_emoji(token.text):
            tokens.append(emoji.demojize(token.text))
        if not token.is_stop and not token.is_punct and not token.like_num and not token.like_url:
            tokens.append(token.lemma_.lower())#renvoie le lemme en minuscule de chaque mot
    return " ".join(tokens)#renvoie la liste de token sous la forme d'un unique string





df["clean"] = df["Content"].apply(preprocess) # crée une nouvelle colonne contenant les txeet netoyés

vectorizer = TfidfVectorizer() # création de la fonction de vectorisation
X = vectorizer.fit_transform(df["clean"]) # calcul des statistiques tfidf et création des vecteur documents
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # divise le data set en deux sous ensemble de test et 'entrainement



#création du model avec 100 arbres, en utilisant les données d'entrainement
model = RandomForestClassifier(n_estimators=160,criterion='gini',max_depth= None,max_features='sqrt', min_samples_leaf=1,min_samples_split=6,random_state=42)



model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))






