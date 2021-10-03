import requests
import json

url = "http://127.0.0.1:4000/prediction"

payload = json.dumps({
	"ChemFormula": "Cc1cccc(C)c1C"
})

headers = {
	'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)