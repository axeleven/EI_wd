from sklearn import metrics

def vizualisation(Y_test, Y_train):
    """
    Visualisation des performances du modèle.
    None
    """
    # Example of using sklearn metrics to visualize performance
    print("Classification Report:")
    print(metrics.classification_report(Y_test, Y_train))
    print("Confusion Matrix:")
    print(metrics.confusion_matrix(Y_test, Y_train))
    print("ROC AUC Score:", metrics.roc_auc_score(Y_test, Y_train))
    print("F1 Score:", metrics.f1_score(Y_test, Y_train, average='weighted'))
    print("Accuracy Score:", metrics.accuracy_score(Y_test, Y_train))
    print("Precision Score:", metrics.precision_score(Y_test, Y_train, average='weighted'))
    print("Recall Score:", metrics.recall_score(Y_test, Y_train, average='weighted'))