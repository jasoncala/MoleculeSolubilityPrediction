# MoleculeSolubilityPrediction
Data Science project that uses machine learning algorithms to predict the logS of an inputted molecule using a dataset and calculating 4 descriptors of the molecule.

Dataset and theory to use the 4 molecular properties of __MolLogP__, __MolWt__, __Number of Rotatable Bonds__ and __Aromatic Proportion__ come from:
https://pubs.acs.org/doi/10.1021/ci034243x

- **_create_descriptors.py_** reads the original csv file, 'delaney.csv', provided in the research paper, obtains the actual logS and SMILES format, and finds the 4 properties for each molecule in that file. This data is put into a new csv file named 'delaney_solubility_with_descriptors.csv'.

- **_model_building.py_** creates the model using the Extra Trees Regressor amd fits the data into it. This model is exported in a pkl file. The research paper talked about using Linear Regression, however using pycaret in a seperate program for testing, I learned that the Extra Trees Regressor is better for this set of data and provides an R^2 value closer to 1.

- **_molecules_app.py_** is what creates the app which displays all the information based on user inputted SMILE and displays the predicted solubility value. It also displays the actual solubility value if the molecule was part of the original dataset.

This project was done for learning purposes.
Inspired by John Delaney and Chanin Nantasenamat.
