from sklearn import metrics
import matplotlib.pyplot as plt
def vizualisation(Y_test, Y_pred, alpha):
    """
    Visualisation des performances du modèle.
    Cette fonction affiche la matrice de confusion, le rapport de classification.
    Il affiche également le score F2, le score de kappa-cohen.
    """
    # Plotting confusion matrix
    print("---Working with alpha =", alpha, "---")
    title_cm = f'Confusion Matrix (alpha={alpha})'
    cm = metrics.confusion_matrix(Y_test, Y_pred)
    disp = metrics.ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title(title_cm)
    plt.grid(False)
    plt.show()
    # Plotting classification report
    print("Classification Report:")
    print(metrics.classification_report(Y_test, Y_pred))
    # Calculating F2 score
    f2_score = metrics.fbeta_score(Y_test, Y_pred, beta=2, average='weighted')
    print(f"F2 Score: {f2_score:.2f}")
    # Calculating Kappa score
    kappa_score = metrics.cohen_kappa_score(Y_test, Y_pred)
    print(f"Kappa Score: {kappa_score:.2f}")