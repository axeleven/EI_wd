import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("predictions.csv")

X = np.array(df["label"])
Y = np.array(df["likes"])

plt.plot(X, Y, marker='o', linestyle='-') 

plt.xlabel("score colère")
plt.ylabel("likes")
plt.title("popularité d'un truth en fonction de sa colère")
plt.grid(True)
plt.show()