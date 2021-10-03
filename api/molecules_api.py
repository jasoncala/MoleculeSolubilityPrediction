import uvicorn

import pickle

from fastapi import FastAPI 

from pydantic import BaseModel

from rdkit import Chem
from rdkit.Chem import Descriptors

class Molecule(BaseModel):
	ChemFormula: str
	#MolLogP: float
	#MolWt: float
	#NumRotatableBonds: float
	#AromaticProportion: float
app = FastAPI()

with open("molecules_clf.pkl", "rb") as f:
	model = pickle.load(f)


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

def MoleculeToFeatures(formula):
	mol = Chem.MolFromSmiles(formula)
	MolLogP = Descriptors.MolLogP(mol)
	MolWt = Descriptors.MolWt(mol)
	NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
	AromaticProportion = AromaticProportionn(mol)

	data = {'MolLogP': MolLogP,
			'MolWt': MolWt,
			'NumRotatableBonds':NumRotatableBonds,
			'AromaticProportion':AromaticProportion}

	return data

@app.get('/')
def index():
	return {'message': 'This is the homepage of the API'}

@app.post('/prediction')
def get_solubility(data: Molecule):
	received = data.dict()
	ChemFormula = received['ChemFormula']
	newDict = MoleculeToFeatures(ChemFormula)
	MolLogP = newDict['MolLogP']
	MolWt = newDict['MolWt']
	NumRotatableBonds = newDict['NumRotatableBonds']
	AromaticProportion = newDict['AromaticProportion']
	prediction = model.predict([[MolLogP, MolWt, NumRotatableBonds, AromaticProportion]]).tolist()[0] 

	return {'prediction': prediction}

if __name__ == '__main__':
	uvicorn.run(app, host='127.0.0.1', port=4000, debug=True)