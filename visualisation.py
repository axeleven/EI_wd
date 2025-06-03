from sklearn import metrics
import matplotlib.pyplot as plt
def vizualisation(Y_test, Y_train):
    """
    Visualisation des performances du modèle.
    """
    # Plotting confusion matrix
    plt.figure(figsize=(10, 7))
    cm = metrics.confusion_matrix(Y_test, Y_train)
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.xticks(range(len(set(Y_test))), set(Y_test))
    plt.yticks(range(len(set(Y_test))), set(Y_test))
    plt.show()
    print("Confusion Matrix:")
    print(cm)
    # Plotting classification report
    print("Classification Report:")
    print(metrics.classification_report(Y_test, Y_train))