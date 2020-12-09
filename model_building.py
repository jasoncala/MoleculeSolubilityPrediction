import pandas as pd 
from sklearn.ensemble import ExtraTreesRegressor

dataset = pd.read_csv("csv_files/delaney_solubility_with_descriptors.csv")

df = dataset.copy()
target = 'logS'
encode = ['MolLogP', 'MolWt', 'NumRotatableBonds', 'AromaticProportion']

X = df.drop('logS', axis = 1)
Y = df['logS']

final = ExtraTreesRegressor()
final.fit(X,Y)

import pickle
pickle.dump(final, open('molecules_clf.pkl', 'wb'))