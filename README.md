# EI Web Data Project

## Structure du Projet

```
ei_wd/
├── datasets/                     # Jeux de données collectés
├── étiquettage/                  # Scripts et outils d'annotation des données
├── ML_classification_algorithm/  # Modèles de classification (machine learning)
├── ML_regression_algorithm/      # Modèles de régression (machine learning)
├── results/                      # Résultats des analyses et modèles (xgboost et randomforest)
├── scrapping/                    # Scripts de collecte de données web
├── tentativees_retranscription/  # Scripts pour gérer les problèmes d'encodage dans le CSV
├── correelation_colere.py        # Script final pour déterminer s'il existe une corrélation entre le fait d'être haineux et le buzz sur le réseau de Trump
├── api.py                        # Version modifiée de truthbrush à remplacer dans le module
├── README.md                      # Documentation du projet et instructions d'utilisation
```



## Description

Ce projet combine la collecte de données web, l'étiquettage, et l'apprentissage automatique pour analyser des données extraites du web. 
Il a pour objectif final de démontrer une corrélation entre le niveau de haine et le buzz d'un "truth"

:

- **Scrapping** : Scripts pour l'extraction automatisée de données web.
- **Datasets** : Répertoire contenant les jeux de données collectés.
- **Étiquettage** : Outils et scripts pour annoter et préparer les données.
- **ML_classification_algorithm** : Modèles et scripts pour la classification automatique.
- **ML_regression_algorithm** : Modèles et scripts pour la régression automatique.
- **Results** : Résultats des analyses, incluant les sorties des modèles (xgboost, randomforest).
- **Tentativees_retranscription** : Scripts pour résoudre les problèmes d'encodage dans les fichiers CSV.
- **correelation_colere.py** : Script principal pour l'analyse de la corrélation entre discours haineux et viralité sur le réseau de Trump.






