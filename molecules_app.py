import streamlit as st
import numpy as np 
import pandas as pd 
import pickle
from sklearn.ensemble import ExtraTreesRegressor
from rdkit import Chem
from rdkit.Chem import Descriptors

st.write("""
	# Molecule Solubility Prediction App

	This app predicts the **solubility** of a molecule!

	Experimental Data (Actual LogS) obtained from https://pubs.acs.org/doi/10.1021/ci034243x
	""")

st.sidebar.header("Predict Solubility")

def AromaticProportionn(m):
  aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
  aa_count = []
  for i in aromatic_atoms:
    if i==True:
      aa_count.append(1)
  AromaticAtom = sum(aa_count)
  HeavyAtom = Descriptors.HeavyAtomCount(m)
  AR = AromaticAtom/HeavyAtom
  return AR

def user_input_features():
	ChemFormula = st.sidebar.text_input('Chemical Formula (SMILES format)', 'ClCC(Cl)(Cl)Cl')
	mol = Chem.MolFromSmiles(ChemFormula)
	MolLogP = Descriptors.MolLogP(mol)
	MolWt = Descriptors.MolWt(mol)
	NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
	AromaticProportion = AromaticProportionn(mol)
	
	data = {'MolLogP': MolLogP,
			'MolWt': MolWt,
			'NumRotatableBonds':NumRotatableBonds,
			'AromaticProportion':AromaticProportion}
	features = pd.DataFrame(data, index=[ChemFormula])
	return features
input_df = user_input_features()

dataset_raw = pd.read_csv("delaney_solubility_with_descriptors.csv")
dataset = dataset_raw.drop(columns=['logS'])
df = pd.concat([input_df, dataset], axis = 0)


encode = ['MolLogP', 'MolWt', 'NumRotatableBonds', 'AromaticProportion']
df = df[:1]

st.subheader('User Input')
st.write(df)

load_clf = pickle.load(open('molecules_clf.pkl', 'rb'))

prediction = load_clf.predict(df)

st.subheader('Predicted LogS')
st.write(prediction)

st.sidebar.header("Check Actual Solubility")
formula = st.sidebar.text_input('Chemical Formula (SMILES format) ', 'ClCC(Cl)(Cl)Cl')

#Make it show the actual solubility
og = pd.read_csv('delaneycomplete.csv')
count = 0
count2 = 0
for i in og.SMILES:
	if i == formula:
		st.subheader('Actual LogS')
		for y in og['measured log(solubility:mol/L)']:
			if count == count2:
				st.write(y)
			count2+=1
	count+=1