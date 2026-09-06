import pandas as pd

data = pd.read_csv("data/student-mat.csv", sep=";")

print(data.head())
print(data.shape)
